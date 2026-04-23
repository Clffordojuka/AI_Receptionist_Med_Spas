import os
import streamlit as st

from components.api_client import APIClient
from components.overview_panel import render_overview_panel
from components.inbox_panel import render_inbox_panel
from components.lead_profile_panel import render_lead_profile_panel
from components.conversation_panel import render_conversation_panel
from components.booking_panel import render_booking_panel
from components.followup_panel import render_followup_panel
from components.admin_panel import render_admin_panel


st.set_page_config(
    page_title="AI Receptionist Workspace",
    page_icon="💬",
    layout="wide",
)

api_base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
api_client = APIClient(api_base_url)

st.title("AI Receptionist Workspace")
st.caption(
    "A privacy-aware lead operations workspace for conversations, bookings, follow-ups, and staff handoff."
)

overview_tab, workspace_tab = st.tabs(["Operations Overview", "Lead Workspace"])

with overview_tab:
    render_overview_panel(api_client)
    st.divider()
    render_inbox_panel(api_client)

selected_lead_id = st.session_state.get("selected_lead_id")

with workspace_tab:
    if not selected_lead_id:
        st.info("Select a lead from the Operations Overview tab to open the workspace.")
    else:
        st.markdown("## Lead Workspace")
        st.caption("Review the active lead, continue the conversation, and complete the next operational action.")

        # Lead summary header
        render_lead_profile_panel(api_client, selected_lead_id)

        st.divider()

        # Main working area
        main_col, action_col = st.columns([1.6, 1], gap="large")

        with main_col:
            render_conversation_panel(api_client, selected_lead_id)

        with action_col:
            st.markdown("### Action Center")
            st.caption("Use the sections below to move the lead forward.")
            render_booking_panel(api_client, selected_lead_id)
            st.divider()
            render_followup_panel(api_client, selected_lead_id)
            st.divider()
            render_admin_panel(api_client, selected_lead_id)