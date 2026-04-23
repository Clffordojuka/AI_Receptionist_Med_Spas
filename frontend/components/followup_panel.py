import streamlit as st
from datetime import datetime, timedelta, timezone

from components.ui_helpers import display_status


def _render_followup_summary(item: dict):
    with st.container():
        st.markdown("#### Follow-Up Task")
        st.write(f"**Scheduled For:** {item.get('scheduled_for') or 'Not set'}")
        st.write(f"**Attempt:** {item.get('attempt_number') or 1}")
        st.write(f"**Status:** {display_status(item.get('status'))}")
        if item.get("message_template"):
            st.write(f"**Message:** {item.get('message_template')}")
        if item.get("executed_at"):
            st.write(f"**Executed At:** {item.get('executed_at')}")
        st.divider()


def render_followup_panel(api_client, lead_id: int):
    st.subheader("Follow-Up")
    st.caption("Keep unbooked leads active with scheduled reminders and follow-up tracking.")

    if st.button("Schedule Standard Follow-Up", key=f"auto_followup_{lead_id}", type="primary"):
        try:
            with st.spinner("Scheduling follow-up..."):
                result = api_client.auto_schedule_followup(lead_id)
            if result:
                st.success("A follow-up has been scheduled for this lead.")
            else:
                st.info("No follow-up was scheduled. The lead may already have one pending or may already be booked.")
        except Exception as exc:
            st.error(f"Unable to schedule follow-up: {exc}")

    with st.expander("Create Custom Follow-Up", expanded=False):
        default_time = datetime.now(timezone.utc) + timedelta(minutes=10)

        with st.form(f"manual_followup_form_{lead_id}"):
            scheduled_for = st.text_input(
                "Follow-Up Time",
                value=default_time.isoformat(),
                help="Use ISO format, for example 2026-04-23T10:00:00+00:00",
            )
            message_template = st.text_area(
                "Custom Message",
                placeholder="Optional custom reminder message",
                height=90,
            )
            attempt_number = st.number_input(
                "Attempt Number",
                min_value=1,
                max_value=3,
                value=1,
                step=1,
            )

            submitted = st.form_submit_button("Create Follow-Up Task")
            if submitted:
                try:
                    payload = {
                        "lead_id": lead_id,
                        "scheduled_for": scheduled_for,
                        "message_template": message_template or None,
                        "attempt_number": int(attempt_number),
                    }
                    with st.spinner("Creating follow-up task..."):
                        api_client.create_followup(payload)
                    st.success("Custom follow-up created successfully.")
                except Exception as exc:
                    st.error(f"Unable to create follow-up task: {exc}")

    with st.expander("Run Due Follow-Ups", expanded=False):
        if st.button("Run Follow-Up Processor", key=f"run_followups_{lead_id}"):
            try:
                with st.spinner("Processing due follow-up tasks..."):
                    result = api_client.run_followups()
                st.success(
                    f"Processed {result['processed_jobs']} job(s): "
                    f"{result['sent_jobs']} sent, "
                    f"{result['cancelled_jobs']} cancelled, "
                    f"{result['failed_jobs']} failed."
                )
            except Exception as exc:
                st.error(f"Unable to process follow-ups: {exc}")

    with st.expander("View Follow-Up History", expanded=False):
        try:
            with st.spinner("Loading follow-up history..."):
                followups = api_client.get_lead_followups(lead_id)

            if followups:
                for item in followups:
                    _render_followup_summary(item)
            else:
                st.info("No follow-up history is available for this lead.")
        except Exception as exc:
            st.error(f"Unable to load follow-up history: {exc}")