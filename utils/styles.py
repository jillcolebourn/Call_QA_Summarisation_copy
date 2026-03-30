"""
Shared CSS styles and branding for the application
"""
import streamlit as st

# NatWest Brand Colors
COLORS = {
    "dark_purple": "#42145F",
    "bright_magenta": "#FF006E",
    "light_lavender": "#E6D9F2",
    "light_gray": "#F5F5F5",
    "white": "#FFFFFF",
    "red": "#E60028",
    "light_red": "#FFE6E6",
    "green": "#00A577",
    "blue": "#0073C1"
}

def apply_custom_css(colors=COLORS):
    """Apply custom CSS styling to the app"""
    st.markdown(f"""
<style>
    /* Sidebar styling - dark purple gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {colors['dark_purple']} 0%, #2D0E42 100%);
        padding: 2rem 1rem;
    }}

    [data-testid="stSidebar"] .element-container {{
        color: white;
    }}

    /* Logo container */
    .logo-container {{
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }}

    /* Main content background - light gray */
    .main .block-container {{
        background-color: {colors['light_gray']};
        padding: 2rem;
        max-width: 100%;
    }}

    /* Header styling - clean white card */
    .dashboard-header {{
        background: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}

    .dashboard-header h1 {{
        color: {colors['dark_purple']};
        font-size: 2rem;
        margin: 0 0 0.3rem 0;
        font-weight: 700;
    }}

    .dashboard-header p {{
        color: #666;
        margin: 0;
        font-size: 0.95rem;
    }}

    /* Summary cards - subtle lavender gradient */
    .summary-card {{
        background: linear-gradient(135deg, #F0E6F6 0%, #E9DAF5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid rgba(66, 20, 95, 0.1);
        transition: transform 0.2s ease;
    }}

    .summary-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}

    .summary-card h3 {{
        color: #5E2750;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }}

    .summary-card .value {{
        color: {colors['dark_purple']};
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }}

    .summary-card .subtitle {{
        color: #666;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }}

    /* Table styling - clean white */
    .payment-table {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}

    .table-header {{
        color: {colors['dark_purple']};
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }}

    /* Summary Table styling - clean white */
    .summary-table {{
        background-color: #262626;
        padding: 1.5rem;
        border-radius: 0 0 12px 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: #FFFFFF;
    }}

    .summary-table table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .summary-table th {{
        color: {colors['light_lavender']} !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        text-align: left;
        padding: 12px;
        border-bottom: 1px solid #444;
        background-color: #333;
    }}

    .summary-table td {{
        padding: 12px;
        border-bottom: 1px solid #444;
        color: #FFFFFF !important;
        font-size: 0.95rem;
    }}

    /* Narrative Summary Card - Dark grey with white text */
    .summary-narrative {{
        background-color: #262626;
        padding: 1.5rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: #FFFFFF !important;
        line-height: 1.6;
        font-size: 1rem;
        margin-bottom: 2rem;
    }}

    /* Editable Table Container - Dark grey to match static tables */
    .summary-table-editor {{
        background-color: #262626;
        padding: 1rem;
        border-radius: 0 0 12px 12px;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}

    /* Adjusting data editor inside our container */
    .summary-table-editor [data-testid="stDataEditor"] {{
        background-color: transparent !important;
    }}

    /* Accept Button Styling - Right Aligned Green Button */
    .accept-container {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 2rem;
    }}

    .stButton > button.accept-btn {{
        background-color: {colors['green']} !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 4px rgba(0, 165, 119, 0.2) !important;
    }}

    .stButton > button.accept-btn:hover {{
        background-color: #008f68 !important;
        box-shadow: 0 4px 8px rgba(0, 165, 119, 0.3) !important;
        transform: translateY(-1px);
    }}

    /* Transcript Box */
    .transcript-box {{
        background-color: #262626;
        color: #FFFFFF !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: inherit;
        line-height: 1.5;
        border: 1px solid #444;
    }}

    .table-header {{
        background-color: {colors['dark_purple']};
        color: #FFFFFF !important;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 1.5rem;
        border-radius: 12px 12px 0 0;
        margin-top: 1rem;
        margin-bottom: 0; /* Sit flush with table */
    }}

    .header-standalone {{
        background-color: {colors['dark_purple']};
        color: #FFFFFF !important;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }}

    .section-header {{
        background-color: {colors['dark_purple']};
        color: #FFFFFF !important;
        font-size: 1.8rem;
        font-weight: 700;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }}

    /* Status badges - clean design */
    .status-paid {{
        background: #E8F5E9;
        color: #2E7D32;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    .status-missed {{
        background: #FFEBEE;
        color: #C62828;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    .status-pending {{
        background: #FFF3E0;
        color: #E65100;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    /* Urgent notice box - stronger visual */
    .urgent-notice {{
        background: linear-gradient(135deg, #FFF5F5 0%, #FFEBEE 100%);
        border: 2px solid #EF5350;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(239, 83, 80, 0.15);
    }}

    .urgent-notice h3 {{
        color: #C62828;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .urgent-notice p {{
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
    }}

    .urgent-notice strong {{
        color: #D32F2F;
        font-size: 1.2rem;
    }}

    /* Support card - clean white */
    .support-card {{
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}

    .support-card h3 {{
        color: {colors['dark_purple']};
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }}

    .support-card p, .support-card ul {{
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
    }}

    /* Workflow stage indicator - clean cards */
    .workflow-stage {{
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }}

    .workflow-stage.active {{
        border-left-color: {colors['bright_magenta']};
        background: linear-gradient(135deg, #FFF5FC 0%, #FFE6F5 100%);
        box-shadow: 0 4px 8px rgba(255, 0, 110, 0.15);
    }}

    .workflow-stage.completed {{
        border-left-color: {colors['green']};
        background: #F5F5F5;
    }}

    .workflow-stage strong {{
        color: {colors['dark_purple']};
        font-size: 1rem;
    }}

    .workflow-stage span {{
        color: #666;
        font-size: 0.85rem;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, {colors['blue']} 0%, #0052A3 100%);
        border: none;
    }}

    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(90deg, #0052A3 0%, #003D7A 100%);
        box-shadow: 0 4px 12px rgba(0, 115, 193, 0.3);
        transform: translateY(-1px);
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Responsive design */
    @media (max-width: 768px) {{
        .dashboard-header h1 {{
            font-size: 1.5rem;
        }}
        .summary-card .value {{
            font-size: 1.5rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)


NATWEST_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="47" viewBox="0 0 266 62" style="max-width: 100%;"><defs><linearGradient id="a" x1="24.974%" x2="75.006%" y1="41.659%" y2="58.329%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.65%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.33%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.05%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="99.97%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient><linearGradient id="b" x1="71.105%" x2="36.235%" y1="35.476%" y2="59.474%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.66%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.34%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.07%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="100%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient><linearGradient id="c" x1="42.455%" x2="63.784%" y1="29.336%" y2="70.663%"><stop offset="0%" stop-color="#5A287D" stop-opacity="0"/><stop offset="1.42%" stop-color="#5C297F" stop-opacity=".013"/><stop offset="34.66%" stop-color="#863FB6" stop-opacity=".312"/><stop offset="63.34%" stop-color="#A54FDE" stop-opacity=".57"/><stop offset="86.07%" stop-color="#B858F6" stop-opacity=".775"/><stop offset="100%" stop-color="#BF5CFF" stop-opacity=".9"/></linearGradient></defs><g fill="none"><circle cx="31" cy="31" r="31" fill="#ffffff"/><path fill="#ffffff" d="M62 31c0 28.75-2.25 31-31 31S0 59.75 0 31 2.25 0 31 0s31 2.25 31 31"/><path fill="#BF5CFF" d="M40.26 37.815H27.922l6.164 10.69H46.43zm-3.09-26.712H24.831l-6.165 10.68h12.336zm-15.424 26.71 6.165-10.679H15.574L9.41 37.814l-.004.004z"/><path fill="#8F52D1" d="m46.426 27.136 6.169 10.683-6.166 10.685-6.17-10.69zm-15.423-5.354 6.169 10.688 6.166-10.682-6.169-10.685zm-3.088 26.722H15.574L9.405 37.818l.004-.005h12.337z"/><path fill="url(#a)" d="m40.25 27.136-3.078 5.333h-6.17l-3.08 5.346h12.337l6.167-10.68z"/><path fill="url(#b)" d="M21.764 27.134h6.147l3.09 5.335h6.171l-6.17-10.687H18.667z"/><path fill="url(#c)" d="m30.997 43.147-3.076-5.332 3.08-5.346-3.09-5.335-6.165 10.68 6.168 10.69z"/><path fill="#ffffff" d="M204.35 29.966v9.967a9.47 9.47 0 0 1-1.716.8c-.639.229-1.304.424-1.991.586-.688.161-1.386.28-2.094.357-.708.076-1.372.114-1.991.114-1.745 0-3.3-.285-4.667-.857-1.366-.57-2.52-1.342-3.46-2.313a9.931 9.931 0 0 1-2.151-3.384 11.242 11.242 0 0 1-.742-4.07c0-1.504.267-2.904.8-4.199a10.346 10.346 0 0 1 2.21-3.37c.94-.952 2.069-1.699 3.387-2.242 1.318-.543 2.762-.814 4.333-.814 1.9 0 3.45.233 4.651.7 1.202.467 2.21 1.11 3.025 1.928l-1.978 2.085c-.853-.8-1.754-1.357-2.704-1.671a9.472 9.472 0 0 0-2.994-.472c-1.183 0-2.25.214-3.199.643a7.591 7.591 0 0 0-2.442 1.727 7.584 7.584 0 0 0-1.57 2.557 8.811 8.811 0 0 0-.553 3.127c0 1.142.204 2.204.61 3.184.407.982.97 1.833 1.687 2.557a7.773 7.773 0 0 0 2.53 1.7c.969.41 2.025.614 3.17.614a13.9 13.9 0 0 0 2.805-.272c.882-.18 1.632-.442 2.254-.785v-5.626h-4.566v-2.57h7.355v-.001Zm3.915-2.228h2.617v2.085h.059a3.67 3.67 0 0 1 .698-.985c.29-.295.615-.547.974-.757.359-.21.75-.376 1.177-.5a4.564 4.564 0 0 1 1.28-.186c.426 0 .814.058 1.163.172l-.117 2.77a7.61 7.61 0 0 0-.639-.142 3.635 3.635 0 0 0-.64-.058c-1.279 0-2.258.353-2.936 1.057-.679.704-1.018 1.799-1.018 3.284v6.797h-2.617V27.738Zm9.553 6.769c0-.99.19-1.914.567-2.77a7.225 7.225 0 0 1 1.556-2.258 7.293 7.293 0 0 1 2.326-1.528 7.412 7.412 0 0 1 2.878-.557 7.42 7.42 0 0 1 2.879.557c.89.371 1.667.881 2.326 1.528a7.22 7.22 0 0 1 1.556 2.257c.378.857.567 1.78.567 2.77s-.19 1.919-.567 2.785a6.996 6.996 0 0 1-1.556 2.256 7.394 7.394 0 0 1-2.326 1.514 7.415 7.415 0 0 1-2.879.556 7.41 7.41 0 0 1-2.878-.556 7.394 7.394 0 0 1-2.326-1.514 6.996 6.996 0 0 1-1.556-2.256 6.887 6.887 0 0 1-.567-2.784Zm2.792 0c0 .685.106 1.318.32 1.9.213.58.513 1.075.902 1.484.387.41.862.734 1.424.971.562.238 1.192.358 1.89.358s1.328-.119 1.89-.358a4.172 4.172 0 0 0 1.425-.97c.388-.41.688-.905.902-1.486.212-.58.32-1.214.32-1.9 0-.685-.107-1.318-.32-1.899a4.287 4.287 0 0 0-.902-1.485 4.183 4.183 0 0 0-1.425-.97c-.562-.24-1.192-.358-1.89-.358s-1.328.119-1.89.357a4.175 4.175 0 0 0-1.424.97c-.388.41-.688.905-.902 1.486a5.462 5.462 0 0 0-.32 1.9Zm26.61 6.768h-2.617V39.19h-.058c-.33.724-.902 1.31-1.716 1.757-.814.447-1.755.671-2.82.671-.68 0-1.319-.1-1.92-.3a4.32 4.32 0 0 1-1.584-.928c-.455-.42-.82-.957-1.09-1.614-.272-.657-.408-1.432-.408-2.328v-8.71h2.617v7.996c0 .628.087 1.167.261 1.614.175.447.408.81.698 1.085.29.276.625.476 1.003.6.378.123.77.185 1.177.185.543 0 1.047-.086 1.512-.257a3.15 3.15 0 0 0 1.221-.814c.35-.371.62-.843.815-1.414.193-.572.29-1.247.29-2.028v-6.969h2.617v13.54h.001Zm3.267-13.537h2.617v1.942h.058c.504-.723 1.197-1.285 2.079-1.685.882-.4 1.788-.6 2.719-.6 1.066 0 2.03.182 2.893.543.862.362 1.6.867 2.21 1.514a6.784 6.784 0 0 1 1.41 2.27 7.78 7.78 0 0 1 .494 2.785 7.86 7.86 0 0 1-.494 2.814c-.33.866-.8 1.618-1.41 2.256a6.5 6.5 0 0 1-2.21 1.5c-.863.361-1.827.543-2.893.543a6.495 6.495 0 0 1-2.792-.614c-.872-.41-1.54-.966-2.006-1.671h-.058v9.995h-2.617V27.738Zm7.153 2.056c-.698 0-1.328.119-1.89.357a4.175 4.175 0 0 0-1.425.97c-.387.41-.688.905-.901 1.486a5.462 5.462 0 0 0-.32 1.9c0 .685.106 1.318.32 1.9.212.58.513 1.075.901 1.484.388.41.862.734 1.425.971.562.238 1.192.358 1.89.358s1.327-.119 1.89-.358a4.172 4.172 0 0 0 1.425-.97c.387-.41.688-.905.901-1.486.213-.58.32-1.214.32-1.9 0-.685-.106-1.318-.32-1.899a4.287 4.287 0 0 0-.901-1.485 4.183 4.183 0 0 0-1.425-.97c-.563-.24-1.193-.358-1.89-.358Zm-139.294-4.306v3.077H114.6v8.017c0 1.43.677 1.708 1.928 1.708.73 0 1.28-.14 1.54-.221l.28-.088v3.084l-.156.039c-1.052.267-1.931.355-3.228.355-.898 0-3.825-.296-3.825-4.139v-8.755h-2.2v-.207a313.79 313.79 0 0 1 0-2.192v-.678h2.2v-3.946l3.462-1.213v5.159h3.746Zm23.248-5.03-4.145 20.67h-3.517l-3.662-14.393-3.722 14.392h-3.46l-4.333-20.669h3.613l2.808 14.024 3.49-14.024h3.367c.334 1.31 3.497 13.851 3.538 14.007.025-.168 2.487-13.549 2.574-14.007h3.449Zm3.588 11.23c.089-1.474 1.13-3.398 3.331-3.398 2.39 0 3.117 2.11 3.197 3.399h-6.528Zm3.487-6.48c-2.64 0-7.095 1.72-7.095 8.174 0 7.685 6.112 8.077 7.337 8.077 2.595 0 3.755-.541 4.894-1.074l.124-.059v-3.27l-.329.199c-.827.516-2.429 1.097-4.225 1.097-3.634 0-4.147-2.599-4.193-3.693h9.988l.02-.177c.316-2.156.005-5.177-1.767-7.233-1.17-1.352-2.773-2.041-4.754-2.041m19.318 11.567c0 2.345-2.039 4.715-5.92 4.715-1.703 0-3.584-.423-4.935-1.075l-.122-.06v-3.357l.32.175c1.125.605 2.926 1.247 4.645 1.247 1.568 0 2.47-.56 2.47-1.544 0-.923-.553-1.207-1.917-1.81l-.538-.23a89.103 89.103 0 0 1-2.187-.976c-.912-.41-3.04-1.37-3.04-4.225 0-1.535 1.178-4.422 5.599-4.422 1.824 0 3.629.493 4.34.837l.127.062v3.297l-.32-.15c-1.412-.699-2.65-1.022-4.024-1.022-.506 0-2.177.1-2.177 1.27 0 .886 1.052 1.351 1.903 1.733l.163.07c.613.27 1.095.495 1.51.659l.445.19c2.662 1.166 3.658 2.41 3.658 4.616M89.798 20.458h3.378v20.67h-3.284l-9.018-14.396v14.395H77.5V20.458h3.37l8.93 14.505V20.458h-.002Zm84.19 8.107v8.017c0 1.437.676 1.708 1.933 1.708.713 0 1.259-.14 1.535-.215l.282-.094v3.084l-.178.039c-1.035.267-1.913.355-3.213.355-.898 0-3.81-.296-3.81-4.139v-8.755h-2.211v-.207a89.658 89.658 0 0 1 0-2.192v-.678h2.212v-3.946l3.45-1.213v5.159h3.75v3.077h-3.75ZM104.5 36.563c-.398.49-1.64 1.782-3.577 1.782-1.488 0-2.44-.855-2.44-2.178 0-1.357 1.086-2.138 2.975-2.138h3.04v2.534h.002Zm-2.665-11.403c-1.757 0-3.463.306-4.664.828l-.137.05v3.184l.313-.157c.812-.394 2.756-.752 3.975-.752 3.036 0 3.17 1.156 3.18 2.66h-3.247c-4.299 0-6.255 2.695-6.255 5.194 0 3.483 2.77 5.293 5.52 5.293 1.873 0 3.053-.702 4.003-1.545v1.213h3.425V30.56c-.002-4.874-4.278-5.4-6.113-5.4"/></g></svg>
"""
