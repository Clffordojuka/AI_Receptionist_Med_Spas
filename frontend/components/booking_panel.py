import streamlit as st


def render_booking_panel(api_client, lead_id: int):
    st.subheader("Booking")

    service_name = st.text_input("Service Name", key=f"booking_service_{lead_id}")
    date = st.text_input("Preferred Date (YYYY-MM-DD)", key=f"booking_date_{lead_id}")

    if st.button("Get Available Slots", key=f"get_slots_{lead_id}"):
        try:
            with st.spinner("Fetching available slots..."):
                slots = api_client.get_slots(
                    lead_id=lead_id,
                    service_name=service_name or None,
                    date=date or None,
                )
            st.session_state[f"slots_{lead_id}"] = slots
            st.success("Slots loaded.")
        except Exception as exc:
            st.error(str(exc))

    slots = st.session_state.get(f"slots_{lead_id}", [])

    if slots:
        st.markdown("### Available Slots")
        options = []
        for idx, slot in enumerate(slots):
            label = (
                f"{idx + 1}. {slot['start_time']} to {slot['end_time']} | "
                f"{slot['provider_name']} | {slot.get('service_name') or 'N/A'}"
            )
            options.append((label, slot))

        selected_label = st.selectbox(
            "Choose Slot",
            [option[0] for option in options],
            key=f"slot_select_{lead_id}",
        )

        selected_slot = next(slot for label, slot in options if label == selected_label)
        notes = st.text_area("Booking Notes", key=f"booking_notes_{lead_id}")

        if st.button("Create Booking", key=f"create_booking_{lead_id}"):
            try:
                payload = {
                    "lead_id": lead_id,
                    "service_name": service_name or selected_slot.get("service_name") or "Consultation",
                    "appointment_datetime": selected_slot["start_time"],
                    "provider_name": selected_slot["provider_name"],
                    "notes": notes or None,
                }
                with st.spinner("Creating booking..."):
                    result = api_client.create_booking(payload)
                st.success("Booking created successfully.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))
    else:
        st.info("No slots loaded yet. Fetch available slots first.")

    try:
        with st.spinner("Loading bookings..."):
            bookings = api_client.get_lead_bookings(lead_id)

        st.markdown("### Existing Bookings")
        if bookings:
            for booking in bookings:
                st.json(booking)
        else:
            st.info("No bookings found for this lead.")
    except Exception as exc:
        st.error(str(exc))