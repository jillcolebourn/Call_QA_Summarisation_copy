import logging
import json
import os
import yaml
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from src.utils.template_loader import TemplateLoader
from src.config.config_loader import LLM_CONFIG

logger = logging.getLogger(__name__)

# ============================================================================
# STATE DEFINITION
# ============================================================================

class QAState(TypedDict):
    """
    State for the QA & Coaching Workflow.
    """
    transcript: str
    agent_profile: Dict[str, Any]  # Historical data
    rubric: Dict[str, str]         # The assessment framework
    
    # Outputs
    qa_result: Optional[Dict[str, Any]]
    coaching_plan: Optional[Dict[str, Any]]
    gold_standard_transcript: Optional[str]
    
    # Internal
    messages: List[BaseMessage]

# ============================================================================
# AGENT NODES
# ============================================================================

def get_llm():
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    llm_config = config.get("llm", {})
    if not llm_config:
        raise RuntimeError("config.yml missing 'llm' section")

    if os.path.exists(".env"):
        # Local development — use .env variables
        load_dotenv()
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=llm_config.get("temperature", 0),
            max_tokens=llm_config.get("max_tokens", 2000),
        )
    else:
        # Azure deployment — fetch secrets from Key Vault via Managed Identity
        credential = DefaultAzureCredential()
        secret_client = SecretClient(
            vault_url=llm_config["KEY_VAULT_URL"],
            credential=credential
        )
        return AzureChatOpenAI(
            azure_endpoint=secret_client.get_secret(llm_config["ENDPOINT_SECRET_NAME"]).value,
            api_key=secret_client.get_secret(llm_config["KEY_SECRET_NAME"]).value,
            azure_deployment=llm_config["deployment_name"],
            api_version=llm_config["api_version"],
            temperature=llm_config.get("temperature", 0),
            max_tokens=llm_config.get("max_tokens", 2000),
        )



def quality_analyst_node(state: QAState) -> Dict[str, Any]:
    """
    Agent 1: Scores the transcript against the rubric.
    """
    logger.info("🕵️ Quality Analyst starting analysis...")
    
    llm = get_llm()
    
    # Load Prompt
    rubric_str = json.dumps(state['rubric'], indent=2)
    prompt_template = TemplateLoader.load_template('prompts/qa_analyst.txt', rubric=rubric_str)
    
    messages = [
        SystemMessage(content=prompt_template),
        HumanMessage(content=f"Analyze this transcript:\n\n{state['transcript']}")
    ]
    
    # Invoke LLM
    response = llm.invoke(messages)
    
    try:
        # Simple JSON parsing (in prod, use OutputParsers for robustness)
        # Handle Potential Markdown wrapping
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        qa_result = json.loads(content)
        return {"qa_result": qa_result}
        
    except Exception as e:
        logger.error(f"Failed to parse QA output: {e}")
        return {"qa_result": {"error": "Failed to parse analysis"}}

def coaching_strategist_node(state: QAState) -> Dict[str, Any]:
    """
    Agent 2: Generates coaching based on QA result + Profile. (Fast)
    """
    logger.info("🎓 Coaching Strategist preparing feedback...")
    
    llm = get_llm()
    qa_result = state.get('qa_result')
    
    if not qa_result or "error" in qa_result:
        return {"coaching_plan": {"error": "Cannot coach without valid QA result"}}
    
    # Load Prompt
    prompt_template = TemplateLoader.load_template('prompts/coaching_strategist.txt')
    
    # Prepare Input
    context = json.dumps({
        "qa_result": qa_result,
        "agent_profile": state['agent_profile']
    }, indent=2)
    
    messages = [
        SystemMessage(content=prompt_template),
        HumanMessage(content=f"Create a coaching plan based on this context:\n\n{context}")
    ]
    
    # Invoke LLM
    response = llm.invoke(messages)
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        plan = json.loads(content)
        return {"coaching_plan": plan}
        
    except Exception as e:
        logger.error(f"Failed to parse Coaching output: {e}")
        return {"coaching_plan": {"error": "Failed to parse coaching plan"}}

def gold_standard_node(state: QAState) -> Dict[str, Any]:
    """
    Agent 3: Generates the ideal transcript. (Slow)
    """
    logger.info("✨ Gold Standard Generator starting...")
    
    llm = get_llm()
    qa_result = state.get('qa_result')
    
    if not qa_result or "error" in qa_result:
        return {"gold_standard_transcript": ""}
    
    # Load Prompt
    prompt_template = TemplateLoader.load_template('prompts/gold_standard_generator.txt')
    
    # Prepare Input
    human_message = f"""Create the gold standard transcript based on this context:

QA Analysis: {json.dumps(qa_result, indent=2)}

Original Transcript:
{state['transcript']}"""
    
    messages = [
        SystemMessage(content=prompt_template),
        HumanMessage(content=human_message)
    ]
    
    # Invoke LLM
    response = llm.invoke(messages)
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        result = json.loads(content)
        return {"gold_standard_transcript": result.get("gold_standard_transcript", "")}
        
    except Exception as e:
        logger.error(f"Failed to parse Gold Standard output: {e}")
        return {"gold_standard_transcript": "Error generating gold standard."}

# ============================================================================
# GRAPH BUILDER
# ============================================================================

def build_qa_workflow():
    """
    Build the QA Workflow with Parallel Coaching: 
    Analyst -> (Coaching Strategist + Gold Standard) -> End
    """
    workflow = StateGraph(QAState)
    
    # Add Nodes
    workflow.add_node("quality_analyst", quality_analyst_node)
    workflow.add_node("coaching_strategist", coaching_strategist_node)
    workflow.add_node("gold_standard_generator", gold_standard_node)
    
    # Define Entry Point
    workflow.set_entry_point("quality_analyst")
    
    # Define Edges (Parallel branch after Analyst)
    workflow.add_edge("quality_analyst", "coaching_strategist")
    workflow.add_edge("quality_analyst", "gold_standard_generator")
    
    # Finish when BOTH parallel nodes end
    workflow.add_edge("coaching_strategist", END)
    workflow.add_edge("gold_standard_generator", END)
    
    return workflow.compile()
