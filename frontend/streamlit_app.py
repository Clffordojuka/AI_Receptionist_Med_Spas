import streamlit as st

from frontend.components.api_client import APIClient
from frontend.components.leads_panel import (
    render_create_lead_panel,
    render_dashboard_summary,
    render_lead_list_panel,
    render_load_lead_panel,
)
from frontend.components.chat_panel import render_chat_panel
from frontend.components.booking_panel import render_booking_panel
from frontend.components.followup_panel import render_followup_panel
from frontend.components.admin_panel import render_admin_panel


st.set_page_config(
    page_title="AI Receptionist Dashboard",
    page_icon="💬",
    layout="wide",
)

st.title("AI Receptionist Dashboard")
st.caption("Receptionist console for lead intake, chat, booking, follow-up, and escalation.")

default_api_url = st.session_state.get("api_base_url", "http://127.0.0.1:8000")

with st.sidebar:
    st.header("Backend Connection")
    api_base_url = st.text_input("FastAPI Base URL", value=default_api_url)
    st.session_state["api_base_url"] = api_base_url
    api_client = APIClient(api_base_url)

    if st.button("Check API Health"):
        try:
            result = api_client.health()
            st.success("Backend connected.")
            st.json(result)
        except Exception as exc:
            st.error(str(exc))

    st.divider()
    st.info("Start FastAPI before opening the workspace.")

overview_tab, workspace_tab = st.tabs(["Overview", "Receptionist Workspace"])

with overview_tab:
    render_dashboard_summary(api_client)

    col1, col2 = st.columns([1, 1])
    with col1:
        render_create_lead_panel(api_client)
    with col2:
        render_load_lead_panel(api_client)

    st.divider()
    render_lead_list_panel(api_client)

selected_lead_id = st.session_state.get("selected_lead_id")

with workspace_tab:
    if not selected_lead_id:
        st.warning("Select a lead from the Overview tab first.")
    else:
        st.markdown(f"## Working on Lead ID: {selected_lead_id}")

        top_left, top_right = st.columns(2)
        bottom_left, bottom_right = st.columns(2)

        with top_left:
            render_chat_panel(api_client, selected_lead_id)

        with top_right:
            render_booking_panel(api_client, selected_lead_id)

        with bottom_left:
            render_followup_panel(api_client, selected_lead_id)

        with bottom_right:
            render_admin_panel(api_client, selected_lead_id)