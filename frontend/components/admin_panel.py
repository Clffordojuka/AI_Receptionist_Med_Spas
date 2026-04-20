import streamlit as st


def render_admin_panel(api_client, lead_id: int):
    st.subheader("Admin Controls")

    with st.form(f"admin_update_form_{lead_id}"):
        assigned_to = st.text_input("Assigned To")
        admin_notes = st.text_area("Admin Notes")
        lead_status = st.text_input("Lead Status")
        qualification_status = st.text_input("Qualification Status")
        booking_status = st.text_input("Booking Status")
        handoff_requested = st.selectbox("Handoff Requested", ["", "true", "false"])

        submitted = st.form_submit_button("Update Admin Fields")
        if submitted:
            try:
                payload = {}

                if assigned_to:
                    payload["assigned_to"] = assigned_to
                if admin_notes:
                    payload["admin_notes"] = admin_notes
                if lead_status:
                    payload["lead_status"] = lead_status
                if qualification_status:
                    payload["qualification_status"] = qualification_status
                if booking_status:
                    payload["booking_status"] = booking_status
                if handoff_requested == "true":
                    payload["handoff_requested"] = True
                elif handoff_requested == "false":
                    payload["handoff_requested"] = False

                result = api_client.update_admin_fields(lead_id, payload)
                st.success("Admin fields updated.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))

    with st.form(f"escalate_form_{lead_id}"):
        escalate_assigned_to = st.text_input("Escalate To")
        escalate_notes = st.text_area("Escalation Notes")
        reason = st.text_input("Escalation Reason")

        escalated = st.form_submit_button("Escalate Lead")
        if escalated:
            try:
                payload = {
                    "assigned_to": escalate_assigned_to or None,
                    "admin_notes": escalate_notes or None,
                    "reason": reason or None,
                }
                result = api_client.escalate_lead(lead_id, payload)
                st.success("Lead escalated successfully.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))

    if st.button("Refresh Lead Review", key=f"lead_review_{lead_id}"):
        pass

    try:
        review = api_client.get_lead_review(lead_id)
        st.markdown("### Lead Review Summary")
        st.json(review)
    except Exception as exc:
        st.error(str(exc))