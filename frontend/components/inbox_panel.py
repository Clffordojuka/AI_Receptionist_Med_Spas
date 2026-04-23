import streamlit as st

from components.ui_helpers import prepare_lead_inbox_dataframe


def render_inbox_panel(api_client):
    st.subheader("Lead Inbox")
    st.caption("Review incoming and active leads, apply filters, and open a lead workspace.")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        lead_status = st.selectbox(
            "Lead Stage",
            ["", "new", "qualifying", "qualified", "booked", "pending_followup", "closed"],
            key="lead_status_filter",
        )
    with col2:
        booking_status = st.selectbox(
            "Booking Status",
            ["", "pending", "confirmed", "cancelled"],
            key="booking_status_filter",
        )
    with col3:
        qualification_status = st.selectbox(
            "Qualification",
            ["", "unknown", "in_progress", "qualified", "not_qualified"],
            key="qualification_status_filter",
        )
    with col4:
        handoff_choice = st.selectbox(
            "Handoff",
            ["", "true", "false"],
            key="handoff_filter",
        )
    with col5:
        limit = st.number_input("Rows", min_value=1, max_value=500, value=50, step=10)

    handoff_requested = None
    if handoff_choice == "true":
        handoff_requested = True
    elif handoff_choice == "false":
        handoff_requested = False

    try:
        leads = api_client.list_leads(
            lead_status=lead_status or None,
            booking_status=booking_status or None,
            qualification_status=qualification_status or None,
            handoff_requested=handoff_requested,
            limit=int(limit),
        )

        if not leads:
            st.info("No leads match the current filters.")
            return

        df = prepare_lead_inbox_dataframe(leads)
        st.dataframe(df, use_container_width=True, hide_index=True)

        lead_ids = [lead["id"] for lead in leads]
        selected_id = st.selectbox(
            "Open Lead Workspace",
            lead_ids,
            index=0,
            key="lead_selector_from_list",
        )

        if st.button("Open Lead", type="primary"):
            st.session_state["selected_lead_id"] = selected_id
            st.success(f"Lead {selected_id} is now active in the workspace.")

    except Exception as exc:
        st.error(f"Unable to load lead inbox: {exc}")