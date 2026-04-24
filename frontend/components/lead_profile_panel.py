import streamlit as st

from components.ui_helpers import display_status, status_tone
from components.ui_theme import badge, section_header


def render_lead_profile_panel(api_client, lead_id: int):
    try:
        lead = api_client.get_lead(lead_id)
    except Exception as exc:
        st.error(f"Unable to load lead profile: {exc}")
        return

    section_header(
        "Lead Profile",
        "Review the active lead’s contact details, service context, and workflow status.",
    )

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Contact")
        st.write(f"**Name:** {lead.get('full_name') or 'Not provided'}")
        st.write(f"**Phone:** {lead.get('phone') or 'Not provided'}")
        st.write(f"**Email:** {lead.get('email') or 'Not provided'}")

    with col2:
        st.markdown("#### Service Details")
        st.write(f"**Service Interest:** {lead.get('service_interest') or 'Not specified'}")
        st.write(f"**Client Type:** {lead.get('new_or_returning') or 'Unknown'}")
        st.write(f"**Source Channel:** {lead.get('source_channel') or 'Unknown'}")

    with col3:
        st.markdown("#### Workflow Status")
        badge(display_status(lead.get("lead_status")), status_tone(lead.get("lead_status")))
        badge(display_status(lead.get("booking_status")), status_tone(lead.get("booking_status")))
        badge(display_status(lead.get("qualification_status")), status_tone(lead.get("qualification_status")))
        if lead.get("handoff_requested"):
            badge("Handoff Requested", "danger")
        st.write("")
        st.write(f"**Assigned To:** {lead.get('assigned_to') or 'Unassigned'}")

    st.markdown("</div>", unsafe_allow_html=True)