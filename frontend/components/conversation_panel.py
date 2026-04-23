import streamlit as st


def render_conversation_panel(api_client, lead_id: int):
    st.subheader("Conversation")
    st.caption("Review the conversation history and continue the receptionist interaction.")

    col1, col2 = st.columns([3, 1])
    with col1:
        message = st.text_area("New Message", height=100, key=f"chat_message_{lead_id}")
    with col2:
        channel = st.selectbox(
            "Channel",
            ["webchat", "sms", "whatsapp"],
            key=f"chat_channel_{lead_id}",
        )

    if st.button("Send Message", key=f"send_message_{lead_id}", type="primary"):
        if not message.strip():
            st.warning("Enter a message before sending.")
        else:
            try:
                with st.spinner("Processing conversation..."):
                    api_client.send_chat_message(
                        {
                            "lead_id": lead_id,
                            "message": message,
                            "channel": channel,
                        }
                    )
                st.success("Message processed successfully.")
            except Exception as exc:
                st.error(f"Unable to send message: {exc}")

    try:
        history = api_client.get_chat_history(lead_id)
        messages = history.get("messages", [])

        if not messages:
            st.info("No conversation history yet for this lead.")
            return

        for item in messages:
            role = item.get("message_role", "unknown")
            text = item.get("message_text", "")
            intent = item.get("intent", "")
            created_at = item.get("created_at", "")

            if role == "user":
                st.markdown(f"**Lead** · {created_at}")
            elif role == "assistant":
                st.markdown(f"**Receptionist** · {created_at}")
            else:
                st.markdown(f"**System** · {created_at}")

            if intent:
                st.caption(f"Intent: {intent}")

            st.write(text)
            st.divider()

    except Exception as exc:
        st.error(f"Unable to load conversation history: {exc}")