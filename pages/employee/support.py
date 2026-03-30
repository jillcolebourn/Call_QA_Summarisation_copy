"""
Employee Portal - Support Page
Documentation and help resources for compliance officers
"""
import streamlit as st
from utils.sidebar import render_employee_sidebar

# Render sidebar
render_employee_sidebar()

st.title("💬 Support & Documentation")

st.markdown("""
### 📚 Employee Resources

This section contains documentation and support resources for compliance officers
using the mortgage arrears capitalization system.
""")

st.markdown("---")

# System Overview
with st.expander("📋 System Overview", expanded=True):
    st.markdown("""
    ### Agentic AI Workflow System

    This system uses **LangGraph's supervisor pattern** to autonomously process
    mortgage arrears capitalization requests through specialized AI agents:

    - **DataGatherer Agent** 📊 - Retrieves customer and account data
    - **DecisionMaker Agent** ⚖️ - Performs eligibility and affordability assessments
    - **ActionOrchestrator Agent** 📝 - Generates proposals and executes system updates
    - **Supervisor Agent** 🎯 - Coordinates workflow and makes routing decisions

    #### Human-in-the-Loop (HITL)

    Critical operations require compliance officer approval:
    - Proposal finalization
    - Income verification discrepancies
    - System account updates
    """)

# Policy Thresholds
with st.expander("⚖️ Policy Thresholds"):
    st.markdown("""
    ### FCA-Mandated Thresholds

    **Pre-Qualification Criteria:**
    - Loan-to-Value (LTV): ≤ 95%
    - Arrears Strikes: < 4 recent strikes
    - Eligible Products: Standard repayment mortgages

    **Affordability Assessment:**
    - Loan-to-Income (LTI): ≤ 4.5
    - Net Disposable Income (NDI): ≥ 40% of gross income

    These thresholds are configured in `config.yml` and should only be modified
    with regulatory approval.
    """)

# Workflow Steps
with st.expander("📋 Workflow Steps"):
    st.markdown("""
    ### Typical Workflow Execution

    1. **Initiation** - Customer or employee starts capitalization request
    2. **Data Gathering** - System retrieves account and customer financial data
    3. **Pre-Qualification** - Checks LTV, strikes, and product eligibility
    4. **Affordability Assessment** - Calculates LTI and NDI ratios
    5. **Income Verification** (if documents available) - Cross-checks income sources
    6. **Proposal Generation** - Creates customer proposal document
    7. **HITL Approval** - Compliance officer reviews and approves
    8. **Customer Acceptance** (future) - Customer reviews and accepts terms
    9. **System Update** - Account details updated with new terms

    Each step is autonomous - the Supervisor Agent decides when to proceed,
    retry, or terminate based on assessment results.
    """)

# Troubleshooting
with st.expander("🔧 Troubleshooting"):
    st.markdown("""
    ### Common Issues

    **Workflow stuck in "Processing"**
    - Refresh the page
    - Check backend logs for errors
    - Verify OpenAI API key is valid

    **HITL approval not processing**
    - Wait 2-3 seconds after submission
    - Refresh the page
    - Check workflow status via API

    **Backend connection errors**
    - Ensure FastAPI backend is running: `uvicorn api_backend:app --reload`
    - Check port 8000 is not blocked
    - Verify `.env` file contains required credentials

    **Agent errors or failures**
    - Review agent reasoning in workflow expander
    - Check tool execution results
    - Verify CSV data files are present in `data/` directory
    """)

# Contact Information
st.markdown("---")
st.markdown("""
### 📞 Technical Support

For technical issues or questions about the system:

- **Email**: support@natwest-ai.example.com
- **Internal Wiki**: [Link to documentation]
- **Slack Channel**: #mortgage-ai-support

### 🔒 Compliance Questions

For regulatory or compliance-related questions:

- **Email**: compliance@natwest.example.com
- **Phone**: Extension 5432
""")
