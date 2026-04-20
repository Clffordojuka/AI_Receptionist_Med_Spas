import streamlit as st
from datetime import datetime, timedelta, timezone


def render_followup_panel(api_client, lead_id: int):
    st.subheader("Follow-Up Automation")

    if st.button("Auto Schedule Follow-Up", key=f"auto_followup_{lead_id}"):
        try:
            result = api_client.auto_schedule_followup(lead_id)
            if result:
                st.success("Follow-up scheduled.")
                st.json(result)
            else:
                st.info("No follow-up scheduled.")
        except Exception as exc:
            st.error(str(exc))

    default_time = datetime.now(timezone.utc) + timedelta(minutes=1)

    with st.form(f"manual_followup_form_{lead_id}"):
        scheduled_for = st.text_input(
            "Manual Follow-Up Time (ISO format)",
            value=default_time.isoformat(),
        )
        message_template = st.text_area("Custom Message Template")
        attempt_number = st.number_input("Attempt Number", min_value=1, max_value=3, value=1, step=1)

        submitted = st.form_submit_button("Create Manual Follow-Up")
        if submitted:
            try:
                payload = {
                    "lead_id": lead_id,
                    "scheduled_for": scheduled_for,
                    "message_template": message_template or None,
                    "attempt_number": int(attempt_number),
                }
                result = api_client.create_followup(payload)
                st.success("Manual follow-up created.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))

    if st.button("Run Due Follow-Ups", key=f"run_followups_{lead_id}"):
        try:
            result = api_client.run_followups()
            st.success("Follow-up runner executed.")
            st.json(result)
        except Exception as exc:
            st.error(str(exc))

    try:
        followups = api_client.get_lead_followups(lead_id)
        st.markdown("### Follow-Up Jobs")
        if followups:
            for item in followups:
                st.json(item)
        else:
            st.info("No follow-up jobs found.")
    except Exception as exc:
        st.error(str(exc))