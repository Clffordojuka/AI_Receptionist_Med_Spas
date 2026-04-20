import pandas as pd
import streamlit as st


def render_dashboard_summary(api_client):
    st.subheader("Dashboard Summary")

    try:
        summary = api_client.get_dashboard_summary()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Leads", summary["total_leads"])
        c2.metric("Booked", summary["booked_leads"])
        c3.metric("Handoffs", summary["handoff_leads"])
        c4.metric("Pending Follow-Up", summary["pending_followup_leads"])
        c5.metric("Qualifying", summary["qualifying_leads"])
    except Exception as exc:
        st.error(str(exc))


def render_create_lead_panel(api_client):
    st.subheader("Create Lead")

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
                st.success(f"Lead created successfully with ID {result['id']}")
                st.session_state["selected_lead_id"] = result["id"]
            except Exception as exc:
                st.error(str(exc))


def render_lead_list_panel(api_client):
    st.subheader("Lead Inbox")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        lead_status = st.selectbox(
            "Lead Status",
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
        limit = st.number_input("Limit", min_value=1, max_value=500, value=50, step=10)

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
            st.info("No leads found for the selected filters.")
            return

        df = pd.DataFrame(leads)

        display_columns = [
            "id",
            "full_name",
            "phone",
            "email",
            "source_channel",
            "service_interest",
            "qualification_status",
            "booking_status",
            "lead_status",
            "assigned_to",
            "handoff_requested",
            "updated_at",
        ]
        available_columns = [col for col in display_columns if col in df.columns]
        st.dataframe(df[available_columns], use_container_width=True)

        lead_ids = [lead["id"] for lead in leads]
        selected_id = st.selectbox(
            "Open Lead in Workspace",
            lead_ids,
            index=0,
            key="lead_selector_from_list",
        )

        if st.button("Open Selected Lead"):
            st.session_state["selected_lead_id"] = selected_id
            st.success(f"Lead {selected_id} loaded into workspace.")

    except Exception as exc:
        st.error(str(exc))


def render_load_lead_panel(api_client):
    st.subheader("Load Lead by ID")

    lead_id = st.number_input(
        "Lead ID",
        min_value=1,
        step=1,
        value=st.session_state.get("selected_lead_id", 1),
    )
    if st.button("Load Lead by ID"):
        st.session_state["selected_lead_id"] = int(lead_id)

    selected_lead_id = st.session_state.get("selected_lead_id")
    if selected_lead_id:
        try:
            lead = api_client.get_lead(selected_lead_id)
            st.markdown("### Selected Lead Snapshot")
            st.json(lead)
        except Exception as exc:
            st.error(str(exc))