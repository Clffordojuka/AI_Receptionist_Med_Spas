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

    if st.button("Refresh Chat History", key=f"refresh_chat_{lead_id}"):
        pass

    try:
        history = api_client.get_chat_history(lead_id)
        st.markdown("### Conversation History")
        for item in history.get("messages", []):
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