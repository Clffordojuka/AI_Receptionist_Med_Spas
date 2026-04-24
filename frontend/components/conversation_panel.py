import streamlit as st

from components.ui_theme import section_header


def _role_label(role: str) -> tuple[str, str]:
    if role == "user":
        return "Lead", "chat-user"
    if role == "assistant":
        return "Receptionist", "chat-assistant"
    return "System", "chat-system"


def render_conversation_panel(api_client, lead_id: int):
    section_header(
        "Conversation",
        "Continue the interaction and review the conversation history in a cleaner operator timeline.",
    )

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        message = st.text_area(
            "New Message",
            height=110,
            placeholder="Type the next message here.",
            key=f"chat_message_{lead_id}",
        )

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
                with st.spinner("Updating conversation..."):
                    api_client.send_chat_message(
                        {
                            "lead_id": lead_id,
                            "message": message,
                            "channel": channel,
                        }
                    )
                st.success("Conversation updated successfully.")
            except Exception as exc:
                st.error(f"Unable to send message: {exc}")

    try:
        with st.spinner("Loading conversation history..."):
            history = api_client.get_chat_history(lead_id)

        messages = history.get("messages", [])

        if not messages:
            st.info("No conversation history is available for this lead yet.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

        for item in messages:
            role = item.get("message_role", "unknown")
            label, bubble_class = _role_label(role)
            text = item.get("message_text", "")
            intent = item.get("intent", "")
            created_at = item.get("created_at", "")
            channel_name = item.get("channel", "")

            meta = label
            if created_at:
                meta += f" · {created_at}"
            if channel_name:
                meta += f" · {channel_name}"
            if intent:
                meta += f" · {intent}"

            st.markdown(f'<div class="chat-meta">{meta}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="chat-bubble {bubble_class}">{text}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as exc:
        st.error(f"Unable to load conversation history: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)