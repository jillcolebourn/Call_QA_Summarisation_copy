import streamlit as st
import pandas as pd
import json
import os
from src.call_summarisation import CallSummariser
from utils.styles import apply_custom_css

# Apply custom CSS
apply_custom_css()

# Logo Definition
import base64
svg_logo = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="47" viewBox="0 0 266 62" style="max-width: 100%;"><defs><linearGradient id="a" x1="24.974%" x2="75.006%" y1="41.659%" y2="58.329%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.65%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.33%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.05%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="99.97%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient><linearGradient id="b" x1="71.105%" x2="36.235%" y1="35.476%" y2="59.474%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.66%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.34%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.07%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="100%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient><linearGradient id="c" x1="42.455%" x2="63.784%" y1="29.336%" y2="70.663%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.66%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.34%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.07%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="100%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient></defs><g fill="none"><circle cx="31" cy="31" r="31" fill="#ffffff"/><path fill="#ffffff" d="M62 31c0 28.75-2.25 31-31 31S0 59.75 0 31 2.25 0 31 0s31 2.25 31 31"/><path fill="#BF5CFF" d="M40.26 37.815H27.922l6.164 10.69H46.43zm-3.09-26.712H24.831l-6.165 10.68h12.336zm-15.424 26.71 6.165-10.679H15.574L9.41 37.814l-.004.004z"/><path fill="#8F52D1" d="m46.426 27.136 6.169 10.683-6.166 10.685-6.17-10.69zm-15.423-5.354 6.169 10.688 6.166-10.682-6.169-10.685zm-3.088 26.722H15.574L9.405 37.818l.004-.005h12.337z"/><path fill="url(#a)" d="m40.25 27.136-3.078 5.333h-6.17l-3.08 5.346h12.337l6.167-10.68z"/><path fill="url(#b)" d="M21.764 27.134h6.147l3.09 5.335h6.171l-6.17-10.687H18.667z"/><path fill="url(#c)" d="m30.997 43.147-3.076-5.332 3.08-5.346-3.09-5.335-6.165 10.68 6.168 10.69z"/><path fill="#ffffff" d="M204.35 29.966v9.967a9.47 9.47 0 0 1-1.716.8c-.639.229-1.304.424-1.991.586-.688.161-1.386.28-2.094.357-.708.076-1.372.114-1.991.114-1.745 0-3.3-.285-4.667-.857-1.366-.57-2.52-1.342-3.46-2.313a9.931 9.931 0 0 1-2.151-3.384 11.242 11.242 0 0 1-.742-4.07c0-1.504.267-2.904.8-4.199a10.346 10.346 0 0 1 2.21-3.37c.94-.952 2.069-1.699 3.387-2.242 1.318-.543 2.762-.814 4.333-.814 1.9 0 3.45.233 4.651.7 1.202.467 2.21 1.11 3.025 1.928l-1.978 2.085c-.853-.8-1.754-1.357-2.704-1.671a9.472 9.472 0 0 0-2.994-.472c-1.183 0-2.25.214-3.199.643a7.591 7.591 0 0 0-2.442 1.727 7.584 7.584 0 0 0-1.57 2.557 8.811 8.811 0 0 0-.553 3.127c0 1.142.204 2.204.61 3.184.407.982.97 1.833 1.687 2.557a7.773 7.773 0 0 0 2.53 1.7c.969.41 2.025.614 3.17.614a13.9 13.9 0 0 0 2.805-.272c.882-.18 1.632-.442 2.254-.785v-5.626h-4.566v-2.57h7.355v-.001Zm3.915-2.228h2.617v2.085h.059a3.67 3.67 0 0 1 .698-.985c.29-.295.615-.547.974-.757.359-.21.75-.376 1.177-.5a4.564 4.564 0 0 1 1.28-.186c.426 0 .814.058 1.163.172l-.117 2.77a7.61 7.61 0 0 0-.639-.142 3.635 3.635 0 0 0-.64-.058c-1.279 0-2.258.353-2.936 1.057-.679.704-1.018 1.799-1.018 3.284v6.797h-2.617V27.738Zm9.553 6.769c0-.99.19-1.914.567-2.77a7.225 7.225 0 0 1 1.556-2.258 7.293 7.293 0 0 1 2.326-1.528 7.412 7.412 0 0 1 2.878-.557 7.42 7.42 0 0 1 2.879.557c.89.371 1.667.881 2.326 1.528a7.22 7.22 0 0 1 1.556 2.257c.378.857.567 1.78.567 2.77s-.19 1.919-.567 2.785a6.996 6.996 0 0 1-1.556 2.256 7.394 7.394 0 0 1-2.326 1.514 7.415 7.415 0 0 1-2.879.556 7.41 7.41 0 0 1-2.878-.556 7.394 7.394 0 0 1-2.326-1.514 6.996 6.996 0 0 1-1.556-2.256 6.887 6.887 0 0 1-.567-2.784Zm2.792 0c0 .685.106 1.318.32 1.9.213.58.513 1.075.902 1.484.387.41.862.734 1.424.971.562.238 1.192.358 1.89.358s1.328-.119 1.89-.358a4.172 4.172 0 0 0 1.425-.97c.388-.41.688-.905.902-1.486.212-.58.32-1.214.32-1.9 0-.685-.107-1.318-.32-1.899a4.287 4.287 0 0 0-.902-1.485 4.183 4.183 0 0 0-1.425-.97c-.562-.24-1.192-.358-1.89-.358s-1.328.119-1.89.357a4.175 4.175 0 0 0-1.424.97c-.388.41-.688.905-.902 1.486a5.462 5.462 0 0 0-.32 1.9Zm26.61 6.768h-2.617V39.19h-.058c-.33.724-.902 1.31-1.716 1.757-.814.447-1.755.671-2.82.671-.68 0-1.319-.1-1.92-.3a4.32 4.32 0 0 1-1.584-.928c-.455-.42-.82-.957-1.09-1.614-.272-.657-.408-1.432-.408-2.328v-8.71h2.617v7.996c0 .628.087 1.167.261 1.614.175.447.408.81.698 1.085.29.276.625.476 1.003.6.378.123.77.185 1.177.185.543 0 1.047-.086 1.512-.257a3.15 3.15 0 0 0 1.221-.814c.35-.371.62-.843.815-1.414.193-.572.29-1.247.29-2.028v-6.969h2.617v13.54h.001Zm3.267-13.537h2.617v1.942h.058c.504-.723 1.197-1.285 2.079-1.685.882-.4 1.788-.6 2.719-.6 1.066 0 2.03.182 2.893.543.862.362 1.6.867 2.21 1.514a6.784 6.784 0 0 1 1.41 2.27 7.78 7.78 0 0 1 .494 2.785 7.86 7.86 0 0 1-.494 2.814c-.33.866-.8 1.618-1.41 2.256a6.5 6.5 0 0 1-2.21 1.5c-.863.361-1.827.543-2.893.543a6.495 6.495 0 0 1-2.792-.614c-.872-.41-1.54-.966-2.006-1.671h-.058v9.995h-2.617V27.738Zm7.153 2.056c-.698 0-1.328.119-1.89.357a4.175 4.175 0 0 0-1.425.97c-.387.41-.688.905-.901 1.486a5.462 5.462 0 0 0-.32 1.9c0 .685.106 1.318.32 1.9.212.58.513 1.075.901 1.484.388.41.862.734 1.425.971.562.238 1.192.358 1.89.358s1.327-.119 1.89-.358a4.172 4.172 0 0 0 1.425-.97c.387-.41.688-.905.901-1.486.213-.58.32-1.214.32-1.9 0-.685-.106-1.318-.32-1.899a4.287 4.287 0 0 0-.901-1.485 4.183 4.183 0 0 0-1.425-.97c-.563-.24-1.193-.358-1.89-.358Zm-139.294-4.306v3.077H114.6v8.017c0 1.43.677 1.708 1.928 1.708.73 0 1.28-.14 1.54-.221l.28-.088v3.084l-.156.039c-1.052.267-1.931.355-3.228.355-.898 0-3.825-.296-3.825-4.139v-8.755h-2.2v-.207a313.79 313.79 0 0 1 0-2.192v-.678h2.2v-3.946l3.462-1.213v5.159h3.746Zm23.248-5.03-4.145 20.67h-3.517l-3.662-14.393-3.722 14.392h-3.46l-4.333-20.669h3.613l2.808 14.024 3.49-14.024h3.367c.334 1.31 3.497 13.851 3.538 14.007.025-.168 2.487-13.549 2.574-14.007h3.449Zm3.588 11.23c.089-1.474 1.13-3.398 3.331-3.398 2.39 0 3.117 2.11 3.197 3.399h-6.528Zm3.487-6.48c-2.64 0-7.095 1.72-7.095 8.174 0 7.685 6.112 8.077 7.337 8.077 2.595 0 3.755-.541 4.894-1.074l.124-.059v-3.27l-.329.199c-.827.516-2.429 1.097-4.225 1.097-3.634 0-4.147-2.599-4.193-3.693h9.988l.02-.177c.316-2.156.005-5.177-1.767-7.233-1.17-1.352-2.773-2.041-4.754-2.041m19.318 11.567c0 2.345-2.039 4.715-5.92 4.715-1.703 0-3.584-.423-4.935-1.075l-.122-.06v-3.357l.32.175c1.125.605 2.926 1.247 4.645 1.247 1.568 0 2.47-.56 2.47-1.544 0-.923-.553-1.207-1.917-1.81l-.538-.23a89.103 89.103 0 0 1-2.187-.976c-.912-.41-3.04-1.37-3.04-4.225 0-1.535 1.178-4.422 5.599-4.422 1.824 0 3.629.493 4.34.837l.127.062v3.297l-.32-.15c-1.412-.699-2.65-1.022-4.024-1.022-.506 0-2.177.1-2.177 1.27 0 .886 1.052 1.351 1.903 1.733l.163.07c.613.27 1.095.495 1.51.659l.445.19c2.662 1.166 3.658 2.41 3.658 4.616M89.798 20.458h3.378v20.67h-3.284l-9.018-14.396v14.395H77.5V20.458h3.37l8.93 14.505V20.458h-.002Zm84.19 8.107v8.017c0 1.437.676 1.708 1.933 1.708.713 0 1.259-.14 1.535-.215l.282-.094v3.084l-.178.039c-1.035.267-1.913.355-3.213.355-.898 0-3.81-.296-3.81-4.139v-8.755h-2.211v-.207a89.658 89.658 0 0 1 0-2.192v-.678h2.212v-3.946l3.45-1.213v5.159h3.75v3.077h-3.75ZM104.5 36.563c-.398.49-1.64 1.782-3.577 1.782-1.488 0-2.44-.855-2.44-2.178 0-1.357 1.086-2.138 2.975-2.138h3.04v2.534h.002Zm-2.665-11.403c-1.757 0-3.463.306-4.664.828l-.137.05v3.184l.313-.157c.812-.394 2.756-.752 3.975-.752 3.036 0 3.17 1.156 3.18 2.66h-3.247c-4.299 0-6.255 2.695-6.255 5.194 0 3.483 2.77 5.293 5.52 5.293 1.873 0 3.053-.702 4.003-1.545v1.213h3.425V30.56c-.002-4.874-4.278-5.4-6.113-5.4"/></g></svg>"""
logo_base64 = base64.b64encode(svg_logo.encode()).decode()

# Page config
st.markdown(f"""
    <div class="dashboard-header">
        <img src="data:image/svg+xml;base64,{logo_base64}" class="header-logo">
        <h1>Call Transcript Summarisation</h1>
        <p>End-of-call wrap-up & Flagging</p>
    </div>
""", unsafe_allow_html=True)


# Initialize summariser using environment variables
@st.cache_resource
def get_summariser():
    return CallSummariser()

summariser = get_summariser()

# Data folder path
DATA_DIR = "data/call_transcripts"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Selection of transcripts
transcripts = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
selected_file = st.selectbox("Select a Demo Transcript", ["Upload New..."] + transcripts)

transcript_text = ""
base_filename = "transcript"
if selected_file == "Upload New...":
    uploaded_file = st.file_uploader("Upload a call transcript", type=["txt"])
    if uploaded_file:
        transcript_text = uploaded_file.read().decode("utf-8")
        base_filename = uploaded_file.name.replace(".txt", "")
elif selected_file:
    with open(os.path.join(DATA_DIR, selected_file), "r", encoding="utf-8") as f:
        transcript_text = f.read()
    base_filename = selected_file.replace(".txt", "")

if transcript_text:
    with st.expander("View Transcript"):
        st.markdown(f'<div class="transcript-box">{transcript_text}</div>', unsafe_allow_html=True)
    
    if st.button("Generate Summary", type="primary"):
        with st.spinner("Analyzing transcript..."):
            try:
                result = summariser.summarise(transcript_text)
                st.session_state["summary_result"] = result
            except Exception as e:
                st.error(f"Error: {e}")

if "summary_result" in st.session_state:
    res = st.session_state["summary_result"]
    
    st.markdown("---")
    st.subheader("Results Analysis")
    
    
    # Download options
    _, col_dl1, spacer, col_dl2, _ = st.columns([2.5, 1.5, 0.2, 1.5, 2.5], gap="medium")
    with col_dl1:
        # JSON Download
        json_data = res.model_dump_json(indent=4)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"summary_{base_filename}.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )
    with col_dl2:
        # CSV Download (flattened)
        # Create a simplified version for CSV
        csv_data = {
            "Category": res.primary_category,
            "Urgency": res.urgency,
            "Sentiment": res.sentiment,
            "Call Outcome": res.call_outcome,
            "Initial Reason for Contact": res.initial_contact_reason,
            "Customer Journey": " -> ".join(res.customer_journey),
            "Customer Requests": ", ".join([i.replace('.', '') for i in res.customer_requested]),
            "Actions Taken": ", ".join([i.replace('.', '') for i in res.actions_taken]),
            "Follow-up Needed": res.follow_up_needed,
            "Next Team": res.next_team,
            "Next Steps": ", ".join([i.replace('.', '') for i in res.next_steps]),
            "Profile Flags": ", ".join([i.replace('.', '') for i in res.profile_flags]),
            "Key Point Summary": res.summary
        }
        df_csv = pd.DataFrame([csv_data])
        st.download_button(
            label="Download CSV",
            data=df_csv.to_csv(index=False),
            file_name=f"summary_{base_filename}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )
    
    # Key Highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="summary-card">
                <h3>Category</h3>
                <p class="value">{res.primary_category.replace('_', ' ').title()}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="summary-card">
                <h3>Urgency</h3>
                <p class="value">{res.urgency.title()}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="summary-card">
                <h3>Sentiment</h3>
                <p class="value">{res.sentiment.replace('_', ' ').title()}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Important Columns Table
    # Important Columns Table - Restored to static HTML
    important_data = {
        "Call Outcome": [res.call_outcome.replace('_', ' ').title()],
        "Initial Contact Reason": [res.initial_contact_reason.replace('_', ' ').title()],
        "Customer Journey": [" → ".join([i.replace('_', ' ').title() for i in res.customer_journey])],
        "Customer Requests": [", ".join([i.replace('.', '') for i in res.customer_requested])],
        "Actions Taken": [", ".join([i.replace('.', '') for i in res.actions_taken])],
        "Follow-up Needed": [res.follow_up_needed],
        "Next Team": [res.next_team.replace('_', ' ').title()],
        "Next Steps": [", ".join([i.replace('.', '') for i in res.next_steps])]
    }
    
    df_outcomes = pd.DataFrame(important_data).T.rename(columns={0: "Details"})
    
    st.markdown(f'''
        <div class="table-header">Key Outcomes</div>
        <div class="summary-table">{df_outcomes.to_html(classes="summary-table-inner")}</div>
    ''', unsafe_allow_html=True)

    # Accept button for Key Outcomes
    st.markdown('<div class="accept-container">', unsafe_allow_html=True)
    if st.button("Accept", key="accept_outcomes", help="Confirm the Key Outcomes"):
        st.success("Key Outcomes confirmed!")
    st.markdown('</div>', unsafe_allow_html=True)

    
    # Summary Narrative - Restored to static HTML
    st.markdown(f'''
        <div class="table-header">Key Point Summary</div>
        <div class="summary-narrative">{res.summary}</div>
    ''', unsafe_allow_html=True)

    # Accept button for Key Point Summary
    st.markdown('<div class="accept-container">', unsafe_allow_html=True)
    if st.button("Accept", key="accept_summary", help="Confirm the Key Point Summary"):
        st.success("Key Point Summary confirmed!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Profile Flags Table - Restored to static HTML
    from src.call_summarisation.schema import ProfileFlag
    try:
        from typing import get_args
        all_profile_flags = get_args(ProfileFlag)
    except ImportError:
        all_profile_flags = []

    if all_profile_flags:
        flags_data = []
        current_flags = set(res.profile_flags)
        
        for flag in all_profile_flags:
            flags_data.append({
                "Flag Name": flag.replace('_', ' ').title(),
                "Active": True if flag in current_flags else False
            })
            
        df_flags = pd.DataFrame(flags_data)
        
        st.markdown(f'''
            <div class="table-header">Profile Flags</div>
            <div class="summary-table">{df_flags.to_html(index=False, classes="summary-table-inner")}</div>
        ''', unsafe_allow_html=True)

        # Accept button for Profile Flags
        st.markdown('<div class="accept-container">', unsafe_allow_html=True)
        if st.button("Accept", key="accept_flags", help="Confirm the Profile Flags"):
            st.success("Profile Flags confirmed!")
        st.markdown('</div>', unsafe_allow_html=True)

    
    
    # Full Details
    with st.expander("View All Parameters (JSON)"):
        st.json(res.model_dump())
