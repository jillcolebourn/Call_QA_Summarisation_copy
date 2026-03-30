"""
Sidebar component for employee portal
Provides workflow management controls
"""
import streamlit as st
from utils.api_client import get_workflow_stats, delete_workflow


def render_employee_sidebar():
    """Render sidebar with workflow management controls"""

    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎯 Workflow Management")

        # Get workflow stats
        try:
            stats = get_workflow_stats()
            if stats and stats.get('recent_workflows'):
                workflows = stats['recent_workflows']

                # Get the most recent workflow (any status)
                if workflows:
                    latest = workflows[0]
                    workflow_id = latest['workflow_id']
                    workflow_status = latest.get('status', 'unknown')
                    workflow_client = latest.get('client_id', 'N/A')

                    # Show different styling based on status
                    if workflow_status == 'completed':
                        st.success(f"**Latest Workflow: Completed** ✅")
                    elif workflow_status == 'failed':
                        st.error(f"**Latest Workflow: Failed** ❌")
                    elif workflow_status in ['awaiting_approval', 'awaiting_customer_approval']:
                        st.warning(f"**Active Workflow: Awaiting Approval** ⏳")
                    else:
                        st.info(f"**Active Workflow: In Progress** 🔄")

                    st.write(f"Client: **{workflow_client}**")
                    st.write(f"ID: `{workflow_id[:16]}...`")
                    st.write(f"Status: **{workflow_status.replace('_', ' ').title()}**")

                    # Clear workflow button (shown for all workflows)
                    st.markdown("---")
                    if st.button("🗑️ Clear Workflow & Start New", type="secondary", use_container_width=True):
                        if delete_workflow(workflow_id):
                            st.success("✅ Workflow cleared!")
                            # Clear all workflow-related session state
                            keys_to_delete = [key for key in list(st.session_state.keys())
                                            if 'approval_pending' in key]
                            for key in keys_to_delete:
                                del st.session_state[key]
                            st.rerun()
                        else:
                            st.error("Failed to clear workflow")
                else:
                    # No workflows exist (expected after clearing)
                    st.info("✨ **Ready for New Workflow**")
                    st.caption("Go to Workflow Management → Start new workflow")
            else:
                # No workflows exist (expected after clearing)
                st.info("✨ **Ready for New Workflow**")
                st.caption("Go to Workflow Management → Start new workflow")
        except Exception as e:
            # Only show error if it's not a simple "no workflows" case
            st.error(f"⚠️ Error fetching workflows: {str(e)}")
