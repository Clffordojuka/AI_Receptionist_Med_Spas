import streamlit as st


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


def render_load_lead_panel(api_client):
    st.subheader("Load Lead")

    lead_id = st.number_input("Lead ID", min_value=1, step=1, value=st.session_state.get("selected_lead_id", 1))
    if st.button("Load Lead"):
        st.session_state["selected_lead_id"] = int(lead_id)

    selected_lead_id = st.session_state.get("selected_lead_id")
    if selected_lead_id:
        try:
            lead = api_client.get_lead(selected_lead_id)
            st.markdown("### Lead Snapshot")
            st.json(lead)
        except Exception as exc:
            st.error(str(exc))