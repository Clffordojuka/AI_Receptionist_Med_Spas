import streamlit as st

from components.ui_helpers import prepare_lead_inbox_dataframe


def render_dashboard_summary(api_client):
    st.subheader("Operations Overview")
    st.caption("Track lead volume, booking progress, follow-up demand, and escalation workload.")

    try:
        summary = api_client.get_dashboard_summary()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Leads", summary["total_leads"])
        c2.metric("Booked", summary["booked_leads"])
        c3.metric("Handoffs", summary["handoff_leads"])
        c4.metric("Pending Follow-Up", summary["pending_followup_leads"])
        c5.metric("Qualifying", summary["qualifying_leads"])
    except Exception as exc:
        st.error(f"Unable to load dashboard summary: {exc}")


def render_create_lead_panel(api_client):
    st.subheader("Create Lead")
    st.caption("Add a new lead record to begin conversation handling and workflow tracking.")

    with st.form("create_lead_form"):
        full_name = st.text_input("Full Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        source_channel = st.selectbox("Source Channel", ["webchat", "sms", "whatsapp", "instagram", "facebook"])
        service_interest = st.text_input("Service Interest")
        new_or_returning = st.selectbox("Client Type", ["", "new", "returning"])

        submitted = st.form_submit_button("Create Lead")

        if submitted:
            try:
                payload = {
                    "full_name": full_name or None,
                    "phone": phone or None,
                    "email": email or None,
                    "source_channel": source_channel,
                    "service_interest": service_interest or None,
                    "new_or_returning": new_or_returning or None,
                }
                result = api_client.create_lead(payload)
                st.success(f"Lead created successfully. Lead ID: {result['id']}")
                st.session_state["selected_lead_id"] = result["id"]
            except Exception as exc:
                st.error(f"Unable to create lead: {exc}")


def render_lead_list_panel(api_client):
    st.subheader("Lead Inbox")
    st.caption("Review active leads, apply workflow filters, and open a lead workspace.")

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
            st.info("No leads match the selected filters.")
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


def render_load_lead_panel(api_client):
    st.subheader("Open Lead by ID")
    st.caption("Jump directly to a known lead record when you already have the lead ID.")

    lead_id = st.number_input(
        "Lead ID",
        min_value=1,
        step=1,
        value=st.session_state.get("selected_lead_id", 1),
    )
    if st.button("Open Lead by ID"):
        st.session_state["selected_lead_id"] = int(lead_id)
        st.success(f"Lead {lead_id} is now active in the workspace.")