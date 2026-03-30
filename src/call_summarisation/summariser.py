import os
import yaml
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .schema import CallSummary, CallDataExtraction
from .prompts import SYSTEM_PROMPT, SUMMARISATION_PROMPT, EXTRACTION_PROMPT

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load environment variables
load_dotenv()

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


"""
INTENTIONALLY COMMENTED OUT - FUNCTIONAL AND SIMPLE WORKING CODE BUT NEW CODE USES ALTERNATIVE MCP FUNCTIONA
class CallSummariser:
    def __init__(
        self, 
        deployment_name: str = "gpt-4o", 
        temperature: float = 0,
        azure_endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        # Initialize the Azure LLM
        llm = AzureChatOpenAI(
            azure_deployment=deployment_name,
            temperature=temperature,
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
        )
        
        # --- Chain 1: Data Extraction ---
        # Uses EXTRACTION_PROMPT as system message and transcript as human message
        # and outputs a structured CallDataExtraction object.
        self.extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", EXTRACTION_PROMPT + "{transcript}")
        ])
        self.extraction_chain = self.extraction_prompt | llm.with_structured_output(CallDataExtraction)

        # --- Chain 2: Summarization ---
        # Uses the SYSTEM_PROMPT plus the specific SUMMARISATION_PROMPT instructions.
        # We append the transcript to the user message.
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", SUMMARISATION_PROMPT + "{transcript}")
        ])
        self.summary_chain = self.summary_prompt | llm | StrOutputParser()

    def summarise(self, transcript: str) -> CallSummary:
        # Summarizes a call transcript into a structured CallSummary object by running extraction and summarization separately.
        
        try:
            # Run chains
            # Note: In a production async environment, these could run in parallel.
            extraction_data: CallDataExtraction = self.extraction_chain.invoke({"transcript": transcript})
            summary_text: str = self.summary_chain.invoke({"transcript": transcript})

            # Combine results
            # CallSummary inherits from CallDataExtraction, so we can unpack the extraction data
            # and add the summary field.
            return CallSummary(
                summary=summary_text,
                **extraction_data.model_dump()
            )

        except Exception as e:
            # Simple retry logic (naive retry for the whole block)
            print(f"Error during summarization: {e}. Retrying...")
            try:
                extraction_data = self.extraction_chain.invoke({"transcript": transcript})
                summary_text = self.summary_chain.invoke({"transcript": transcript})
                return CallSummary(summary=summary_text, **extraction_data.model_dump())
            except Exception as retry_e:
                print(f"Retry failed: {retry_e}")
                raise retry_e
""" 
# --- New Implementation using LCEL Primitives ---
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

class CallSummariser:
    def __init__(self):
        # Initialize the Azure LLM (uses .env locally, Key Vault in Azure)
        llm = get_llm()
        
        # --- Chain 1: Data Extraction ---
        # Input: {"transcript": str}
        # Output: CallDataExtraction
        self.extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", EXTRACTION_PROMPT + "{transcript}")
        ])
        extraction_chain = self.extraction_prompt | llm.with_structured_output(CallDataExtraction)

        # --- Chain 2: Summarization ---
        # Input: {"transcript": str}
        # Output: str
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", SUMMARISATION_PROMPT + "{transcript}")
        ])
        summary_chain = self.summary_prompt | llm | StrOutputParser()

        # Helper function to merge results
        def merge_results(inputs: dict) -> CallSummary:
            extraction: CallDataExtraction = inputs["extraction"]
            summary: str = inputs["summary"]
            # Combine them: unpack extraction data and add summary
            return CallSummary(summary=summary, **extraction.model_dump())

        # --- The Main Runnable Pipeline ---
        # 1. Inputs: receives 'transcript' string.
        # 2. RunnablePassthrough: converts string input to dict {"transcript": input}
        # 3. RunnableParallel: runs extraction and summary in parallel
        # 4. RunnableLambda: merges the dictionary result into CallSummary object
        self.chain = (
            {"transcript": RunnablePassthrough()} 
            | RunnableParallel(
                extraction=extraction_chain,
                summary=summary_chain
            )
            | RunnableLambda(merge_results)
        )

    def summarise(self, transcript: str) -> CallSummary:
        """
        Summarizes a call transcript using an LCEL pipeline.
        """
        try:
            # The chain now handles everything from string -> CallSummary
            return self.chain.invoke(transcript)
        except Exception as e:
            print(f"Error during summarization: {e}. Retrying...")
            return self.chain.invoke(transcript)