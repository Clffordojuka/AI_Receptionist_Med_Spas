import streamlit as st

from components.ui_helpers import display_status
from components.ui_theme import section_header


def render_admin_panel(api_client, lead_id: int):
    section_header(
        "Staff Actions",
        "Assign ownership, add internal notes, and escalate sensitive or complex cases for review.",
    )

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    try:
        review = api_client.get_lead_review(lead_id)
    except Exception as exc:
        st.error(f"Unable to load lead review details: {exc}")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown("### Current Handling Status")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Assigned To:** {review.get('assigned_to') or 'Unassigned'}")
        st.write(f"**Lead Stage:** {display_status(review.get('lead_status'))}")
        st.write(f"**Booking Status:** {display_status(review.get('booking_status'))}")

    with col2:
        st.write(f"**Qualification:** {display_status(review.get('qualification_status'))}")
        st.write(f"**Handoff Requested:** {'Yes' if review.get('handoff_requested') else 'No'}")
        st.write(f"**Conversation Count:** {review.get('conversation_count') or 0}")

    st.write("**Internal Notes**")
    st.info(review.get("admin_notes") or "No internal notes have been added yet.")

    with st.expander("Update Assignment and Notes", expanded=True):
        with st.form(f"admin_update_form_{lead_id}"):
            assigned_to = st.text_input("Assign To")
            admin_notes = st.text_area(
                "Internal Notes",
                placeholder="Add handling notes for staff visibility.",
                height=100,
            )
            lead_status = st.selectbox(
                "Lead Stage",
                ["", "new", "qualifying", "qualified", "booked", "pending_followup", "closed"],
            )
            qualification_status = st.selectbox(
                "Qualification Status",
                ["", "unknown", "in_progress", "qualified", "not_qualified"],
            )
            booking_status = st.selectbox(
                "Booking Status",
                ["", "pending", "confirmed", "cancelled"],
            )
            handoff_requested = st.selectbox(
                "Handoff Requested",
                ["", "true", "false"],
            )

            submitted = st.form_submit_button("Save Staff Updates")
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

                    with st.spinner("Saving staff updates..."):
                        api_client.update_admin_fields(lead_id, payload)
                    st.success("Lead handling details updated successfully.")
                except Exception as exc:
                    st.error(f"Unable to update lead handling details: {exc}")

    with st.expander("Escalate for Human Review", expanded=False):
        with st.form(f"escalate_form_{lead_id}"):
            escalate_assigned_to = st.text_input("Escalate To")
            escalate_notes = st.text_area(
                "Escalation Notes",
                placeholder="Add context for the team member taking over.",
                height=90,
            )
            reason = st.text_input("Reason for Escalation")

            escalated = st.form_submit_button("Escalate Lead")
            if escalated:
                try:
                    payload = {
                        "assigned_to": escalate_assigned_to or None,
                        "admin_notes": escalate_notes or None,
                        "reason": reason or None,
                    }
                    with st.spinner("Escalating lead for review..."):
                        api_client.escalate_lead(lead_id, payload)
                    st.success("Lead escalated for human review.")
                except Exception as exc:
                    st.error(f"Unable to escalate lead: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)