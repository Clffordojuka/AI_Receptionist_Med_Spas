class PromptManager:
    @staticmethod
    def get_system_prompt() -> str:
        return (
            "You are an AI receptionist for a med spa. "
            "Your role is to respond warmly, professionally, and clearly. "
            "You help leads understand services, answer common business questions, "
            "collect booking-related details, and guide them toward scheduling. "
            "Do not give unsafe medical advice. "
            "Do not invent prices, availability, or policies if not provided. "
            "Be concise, helpful, and conversion-focused without sounding pushy."
        )

    @staticmethod
    def build_contextual_prompt(user_message: str, conversation_history: list[dict]) -> str:
        history_lines: list[str] = []

        for item in conversation_history[-6:]:
            role = item.get("role", "unknown").capitalize()
            content = item.get("content", "")
            history_lines.append(f"{role}: {content}")

        history_text = "\n".join(history_lines).strip()

        if history_text:
            return (
                f"{PromptManager.get_system_prompt()}\n\n"
                f"Recent conversation:\n{history_text}\n\n"
                f"Latest user message:\n{user_message}\n\n"
                f"Respond as the receptionist."
            )

        return (
            f"{PromptManager.get_system_prompt()}\n\n"
            f"Latest user message:\n{user_message}\n\n"
            f"Respond as the receptionist."
        )