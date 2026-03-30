import streamlit as st
import json
import logging
from src.workflow.graph_qa import build_qa_workflow
from pathlib import Path
import os
import base64

logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(page_title="AI Coach", page_icon="🎓", layout="wide")

st.title("🎓 Agentic QA & Coaching")
st.markdown("### Post-Call Quality Assurance & Personalized Coaching")
st.info("This autonomous workflow assesses call quality against the framework and generates a personalized coaching plan based on the agent's historical profile.")

# Load Mock Data
try:
    with open("data/qa_agent_profiles.json", "r") as f:
        AGENT_PROFILES = json.load(f)
except FileNotFoundError:
    st.error("Agent profiles not found. Please check data/qa_agent_profiles.json")
    st.stop()
    
# Layout: Sidebar for Inputs
with st.sidebar:
    st.header("Input Configuration")
    
    selected_agent = st.selectbox(
        "Select Agent Profile",
        options=list(AGENT_PROFILES.keys())
    )
    
    # Display Profile Info
    profile = AGENT_PROFILES[selected_agent]
    with st.expander("View Agent Profile", expanded=True):
        st.write(f"**Role:** {profile['role']}")
        st.write(f"**Tenure:** {profile['tenure']}")
    
    # Load the rubric from the external JSON file
    RUBRIC_PATH = "data/assessment_framework.json"
    try:
        with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
            RUBRIC = json.load(f)
    except FileNotFoundError:
        st.error(f"Assessment framework not found at {RUBRIC_PATH}")
        st.stop()
    
    st.write("---")
    st.caption("Agent and Rubric settings are configured here. Upload and analyze transcripts on the main page.")

# --- HELPER: RENDER RESULTS ---
def render_analysis_results(agent_name="Agent"):
    """Renders the QA, Coaching, and Gold Standard results in tabs."""
    if "qa_result" not in st.session_state or not st.session_state["qa_result"]:
        return

    tab_qa, tab_coach, tab_gold = st.tabs(["📊 QA Scorecard", "🧘 Coaching Plan", "✨ Gold Standard"])
    
    with tab_qa:
        res = st.session_state["qa_result"]
        # Overall Score
        overall_score = res.get('overall_score', 'N/A')
        applicable = res.get('applicable_categories', 9)
        
        col_score, col_cats = st.columns(2)
        with col_score:
            if isinstance(overall_score, (int, float)):
                st.metric("Overall Score", f"{overall_score:.1f} / 4")
            else:
                st.metric("Overall Score", overall_score)
        with col_cats:
            st.metric("Categories Assessed", f"{applicable} / 9")
        
        st.divider()
        st.markdown(f"**Summary:** {res.get('overall_summary', 'N/A')}")
        
        col_s, col_i = st.columns(2)
        with col_s:
            st.markdown("**Strengths:**")
            for s in res.get("key_strengths", []):
                st.write(f"✅ {s}")
        with col_i:
            st.markdown("**Areas to Improve:**")
            for i in res.get("areas_for_improvement", []):
                st.write(f"🎯 {i}")
        
        st.divider()
        st.markdown("#### Category Breakdown")
        scores = res.get("scores", {})
        for category, details in scores.items():
            score = details.get("score", 0)
            if score == "N/A" or score == 0:
                label = f"{category} (N/A)"
                icon = "⚪"
            else:
                label = f"{category} ({score}/4)"
                icon = "🟢" if score >= 3 else "🟡" if score == 2 else "🔴"
            
            with st.expander(f"{icon} {label}"):
                st.caption(f"**Reasoning:** {details.get('reason')}")
                if details.get('evidence'):
                    st.markdown(f"_\"{details.get('evidence')}\"_")
    
    with tab_coach:
        plan = st.session_state.get("coaching_plan")
        if not plan:
            st.info("Coaching plan is being prepared...")
        elif "error" in plan:
            st.error(plan["error"])
        else:
            st.subheader(f"Coaching for {agent_name.split(' ')[0]}")
            st.markdown(f"_{plan.get('summary_feedback')}_")
            st.divider()
            st.markdown("#### ✅ Win of the Day")
            st.info(plan.get("positive_reinforcement"))
            st.divider()
            st.markdown("#### 🎯 Focus Areas")
            for area in plan.get("focus_areas", []):
                st.write(f"**Category:** {area.get('category')}")
                st.write(f"**Goal:** {area.get('current_score')} ➔ {area.get('target_score')}")
                st.warning(f"**Advice:** {area.get('advice')}")
                with st.expander("See Example Script"):
                    st.code(area.get('example_script'), language=None)
    
    with tab_gold:
        gold_transcript = st.session_state.get("gold_standard_transcript")
        if not gold_transcript:
            st.info("✨ Gold standard transcript will appear here shortly...")
        else:
            st.markdown("### ✨ Gold Standard Transcript")
            st.caption("Shows the ideal conversation with improved agent responses.")
            st.divider()
            clean_gold = gold_transcript.replace("\\n", "\n")
            st.text_area(
                "Ideal Conversation", 
                value=clean_gold, 
                height=500, 
                disabled=True,
                key="gold_transcript_area"
            )
            st.download_button(
                "📥 Download Gold Transcript", 
                data=clean_gold, 
                file_name="gold_standard.txt", 
                mime="text/plain",
                key="gold_download_btn"
            )


# Main Area: Transcript Selection
st.subheader("📞 Transcript Selection")
DATA_DIR = "data/call_transcripts"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

transcripts = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
selected_file = st.selectbox("Select a Demo Transcript", ["Upload New..."] + transcripts)

final_transcript = ""
if selected_file == "Upload New...":
    uploaded_file = st.file_uploader("Upload a call transcript", type=["txt"])
    if uploaded_file:
        final_transcript = uploaded_file.read().decode("utf-8")
elif selected_file:
    with open(os.path.join(DATA_DIR, selected_file), "r", encoding="utf-8") as f:
        final_transcript = f.read()

st.session_state["transcript"] = final_transcript

if final_transcript:
    with st.expander("View Transcript Preview", expanded=False):
        st.markdown(f'''
            <div style="background-color: #262626; color: white; padding: 1.5rem; border-radius: 12px; max-height: 400px; overflow-y: auto; font-family: 'Inter', sans-serif; line-height: 1.6;">
                {final_transcript.replace('\n', '<br>')}
            </div>
        ''', unsafe_allow_html=True)

st.write("---")

# --- BUTTON & RESULTS ---
# We use session state to track if analysis is currently happening to manage UI state
if "analysis_running" not in st.session_state:
    st.session_state["analysis_running"] = False

# Layout: Button first, then results
col_btn, col_status = st.columns([1, 2])
with col_btn:
    # Disable button if analysis is running
    run_btn = st.button(
        "Run Agent Analysis", 
        type="primary", 
        disabled=st.session_state["analysis_running"] or not final_transcript
    )

with col_status:
    status_placeholder = st.empty()

# Persistent Results Reservoir
results_placeholder = st.empty()

if run_btn:
    st.session_state["analysis_running"] = True
    # Reset previous results
    st.session_state["qa_result"] = None
    st.session_state["coaching_plan"] = None
    st.session_state["gold_standard_transcript"] = None
    
    with status_placeholder.status("Agents are working...", expanded=True) as status:
        try:
            workflow = build_qa_workflow()
            inputs = {
                "transcript": final_transcript,
                "agent_profile": profile,
                "rubric": RUBRIC,
                "messages": []
            }
            
            for update in workflow.stream(inputs):
                for node, state_update in update.items():
                    if node == "quality_analyst":
                        st.session_state["qa_result"] = state_update.get("qa_result")
                        status.update(label="✅ Call Analysis Complete...")
                    elif node == "coaching_strategist":
                        st.session_state["coaching_plan"] = state_update.get("coaching_plan")
                        status.update(label="✅ Coaching Feedback Ready...")
                    elif node == "gold_standard_generator":
                        st.session_state["gold_standard_transcript"] = state_update.get("gold_standard_transcript")
                        status.update(label="✨ Gold Standard Transcript Ready...")
                    
                    # Update the UI incrementally
                    with results_placeholder.container():
                        render_analysis_results(selected_agent)
            
            status.update(label="🏁 All Checks Completed!", state="complete")
            st.session_state["analysis_running"] = False
            # No st.rerun() here to keep the status expanded and results visible
            
        except Exception as e:
            status.update(label="❌ Workflow Failed", state="error")
            st.error(f"Workflow Failed: {str(e)}")
            logger.error(f"QA Workflow Error: {e}", exc_info=True)
            st.session_state["analysis_running"] = False

# Final persistent render (shows results if they exist in state and NOT currently in the block above)
# If run_btn is active, the block above already handles rendering.
if not run_btn and "qa_result" in st.session_state and st.session_state["qa_result"]:
    with results_placeholder.container():
        render_analysis_results(selected_agent)
