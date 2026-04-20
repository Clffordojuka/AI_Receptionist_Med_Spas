import streamlit as st

from frontend.components.api_client import APIClient
from frontend.components.leads_panel import render_create_lead_panel, render_load_lead_panel
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
st.caption("Demo frontend for lead handling, chat, booking, follow-up, and admin workflow.")

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
    st.info("Make sure FastAPI is running before using the dashboard.")

tab1, tab2 = st.tabs(["Lead Management", "Receptionist Workspace"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        render_create_lead_panel(api_client)
    with col2:
        render_load_lead_panel(api_client)

selected_lead_id = st.session_state.get("selected_lead_id")

with tab2:
    if not selected_lead_id:
        st.warning("Create or load a lead first.")
    else:
        st.markdown(f"## Working on Lead ID: {selected_lead_id}")

        section1, section2 = st.columns(2)
        section3, section4 = st.columns(2)

        with section1:
            render_chat_panel(api_client, selected_lead_id)

        with section2:
            render_booking_panel(api_client, selected_lead_id)

        with section3:
            render_followup_panel(api_client, selected_lead_id)

        with section4:
            render_admin_panel(api_client, selected_lead_id)