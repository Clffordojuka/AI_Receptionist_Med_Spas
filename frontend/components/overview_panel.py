import streamlit as st


def render_overview_panel(api_client):
    st.subheader("Operations Overview")
    st.caption("Monitor lead volume, booking progress, follow-up workload, and escalation activity.")

    try:
        summary = api_client.get_dashboard_summary()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Leads", summary["total_leads"])
        c2.metric("Booked", summary["booked_leads"])
        c3.metric("Handoffs", summary["handoff_leads"])
        c4.metric("Pending Follow-Up", summary["pending_followup_leads"])
        c5.metric("Qualifying", summary["qualifying_leads"])
    except Exception as exc:
        st.error(f"Unable to load overview metrics: {exc}")