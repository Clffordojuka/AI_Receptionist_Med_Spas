import streamlit as st


def render_chat_panel(api_client, lead_id: int):
    st.subheader("Chat")

    col1, col2 = st.columns([2, 1])

    with col1:
        message = st.text_area("Message to receptionist", height=120, key=f"chat_message_{lead_id}")

    with col2:
        channel = st.selectbox("Channel", ["webchat", "sms", "whatsapp"], key=f"chat_channel_{lead_id}")

    if st.button("Send Message", key=f"send_message_{lead_id}"):
        if not message.strip():
            st.warning("Enter a message first.")
        else:
            try:
                with st.spinner("Processing message..."):
                    result = api_client.send_chat_message(
                        {
                            "lead_id": lead_id,
                            "message": message,
                            "channel": channel,
                        }
                    )
                st.success("Message processed successfully.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))

    try:
        with st.spinner("Loading chat history..."):
            history = api_client.get_chat_history(lead_id)

        messages = history.get("messages", [])
        st.markdown("### Conversation History")

        if not messages:
            st.info("No conversation history yet for this lead.")
            return

        for item in messages:
            role = item.get("message_role", "unknown").upper()
            channel_name = item.get("channel", "")
            intent = item.get("intent", "")
            text = item.get("message_text", "")
            created_at = item.get("created_at", "")

            with st.container():
                st.markdown(f"**{role}** | `{channel_name}` | intent: `{intent}` | {created_at}")
                st.write(text)
                st.divider()
    except Exception as exc:
        st.error(str(exc))