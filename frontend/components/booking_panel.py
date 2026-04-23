import streamlit as st

from components.ui_helpers import display_status


def _render_booking_summary(booking: dict):
    with st.container():
        st.markdown("#### Confirmed Appointment")
        st.write(f"**Service:** {booking.get('service_name') or 'Not specified'}")
        st.write(f"**Scheduled Time:** {booking.get('appointment_datetime') or 'Not scheduled'}")
        st.write(f"**Provider:** {booking.get('provider_name') or 'Not assigned'}")
        st.write(f"**Status:** {display_status(booking.get('booking_status'))}")
        if booking.get("notes"):
            st.write(f"**Notes:** {booking.get('notes')}")
        st.divider()


def render_booking_panel(api_client, lead_id: int):
    st.subheader("Booking")
    st.caption("Check availability and confirm the next appointment for this lead.")

    service_name = st.text_input(
        "Requested Service",
        key=f"booking_service_{lead_id}",
        placeholder="e.g. Botox consultation",
    )
    date = st.text_input(
        "Preferred Date",
        key=f"booking_date_{lead_id}",
        placeholder="YYYY-MM-DD",
    )

    if st.button("Check Availability", key=f"get_slots_{lead_id}", type="primary"):
        try:
            with st.spinner("Checking appointment availability..."):
                slots = api_client.get_slots(
                    lead_id=lead_id,
                    service_name=service_name or None,
                    date=date or None,
                )
            st.session_state[f"slots_{lead_id}"] = slots
            if slots:
                st.success("Available appointment options loaded.")
            else:
                st.info("No appointment options were returned for the selected request.")
        except Exception as exc:
            st.error(f"Unable to load availability: {exc}")

    slots = st.session_state.get(f"slots_{lead_id}", [])

    if slots:
        st.markdown("### Available Options")

        labels = []
        for idx, slot in enumerate(slots):
            labels.append(
                f"Option {idx + 1} · {slot['start_time']} · {slot['provider_name']}"
            )

        selected_label = st.selectbox(
            "Select Appointment Option",
            labels,
            key=f"slot_select_{lead_id}",
        )
        selected_index = labels.index(selected_label)
        selected_slot = slots[selected_index]

        notes = st.text_area(
            "Booking Notes",
            key=f"booking_notes_{lead_id}",
            placeholder="Add any preparation details or scheduling notes.",
            height=90,
        )

        if st.button("Confirm Appointment", key=f"create_booking_{lead_id}"):
            try:
                payload = {
                    "lead_id": lead_id,
                    "service_name": service_name or selected_slot.get("service_name") or "Consultation",
                    "appointment_datetime": selected_slot["start_time"],
                    "provider_name": selected_slot["provider_name"],
                    "notes": notes or None,
                }
                with st.spinner("Confirming appointment..."):
                    api_client.create_booking(payload)
                st.success("Appointment confirmed successfully.")
                st.session_state.pop(f"slots_{lead_id}", None)
            except Exception as exc:
                st.error(f"Unable to confirm appointment: {exc}")
    else:
        st.info("No availability loaded yet.")

    with st.expander("View Appointment History", expanded=False):
        try:
            with st.spinner("Loading appointment history..."):
                bookings = api_client.get_lead_bookings(lead_id)

            if bookings:
                for booking in bookings:
                    _render_booking_summary(booking)
            else:
                st.info("No appointment history is available for this lead.")
        except Exception as exc:
            st.error(f"Unable to load appointment history: {exc}")