import streamlit as st

from components.ui_helpers import display_status


def render_lead_profile_panel(api_client, lead_id: int):
    try:
        lead = api_client.get_lead(lead_id)
    except Exception as exc:
        st.error(f"Unable to load lead profile: {exc}")
        return

    st.subheader("Lead Profile")
    st.caption("View the active lead’s current status, contact details, and operational assignment.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Contact")
        st.write(f"**Name:** {lead.get('full_name') or 'Not provided'}")
        st.write(f"**Phone:** {lead.get('phone') or 'Not provided'}")
        st.write(f"**Email:** {lead.get('email') or 'Not provided'}")

    with col2:
        st.markdown("### Service Details")
        st.write(f"**Service Interest:** {lead.get('service_interest') or 'Not specified'}")
        st.write(f"**Client Type:** {lead.get('new_or_returning') or 'Unknown'}")
        st.write(f"**Source Channel:** {lead.get('source_channel') or 'Unknown'}")

    with col3:
        st.markdown("### Workflow Status")
        st.write(f"**Lead Stage:** {display_status(lead.get('lead_status'))}")
        st.write(f"**Booking Status:** {display_status(lead.get('booking_status'))}")
        st.write(f"**Qualification:** {display_status(lead.get('qualification_status'))}")
        st.write(f"**Assigned To:** {lead.get('assigned_to') or 'Unassigned'}")
        st.write(f"**Handoff Requested:** {'Yes' if lead.get('handoff_requested') else 'No'}")