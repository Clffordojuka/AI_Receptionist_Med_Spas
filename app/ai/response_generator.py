import logging

from openai import OpenAI

from app.config import get_settings
from app.ai.prompt_manager import PromptManager

logger = logging.getLogger(__name__)
settings = get_settings()


class ResponseGenerator:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def generate(
        self,
        *,
        user_message: str,
        detected_intent: str,
        conversation_history: list[dict],
    ) -> str:
        if self.client:
            try:
                return self._generate_with_openai(
                    user_message=user_message,
                    conversation_history=conversation_history,
                )
            except Exception as exc:
                logger.exception("OpenAI generation failed. Falling back to rule-based response. Error: %s", exc)

        return self._generate_fallback(
            user_message=user_message,
            detected_intent=detected_intent,
        )

    def _generate_with_openai(
        self,
        *,
        user_message: str,
        conversation_history: list[dict],
    ) -> str:
        prompt = PromptManager.build_contextual_prompt(
            user_message=user_message,
            conversation_history=conversation_history,
        )

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text.strip()

    def _generate_fallback(self, *, user_message: str, detected_intent: str) -> str:
        if detected_intent == "greeting":
            return (
                "Hello and welcome. I’m the AI receptionist for our med spa. "
                "How can I help you today with services, appointments, or general questions?"
            )

        if detected_intent == "faq":
            return (
                "I’d be happy to help with that. "
                "Could you tell me which service or detail you’d like to know more about?"
            )

        if detected_intent == "booking":
            return (
                "I can help with booking. "
                "Please share the service you’re interested in and your preferred day or time."
            )

        if detected_intent == "qualification":
            return (
                "I’d be glad to help. "
                "Could you tell me which treatment or service you’re interested in, and whether you’re a new or returning client?"
            )

        if detected_intent == "handoff_request":
            return (
                "Of course. I can help route this to a team member. "
                "Please share your name and preferred contact details, and someone can follow up with you."
            )

        return (
            "Thanks for reaching out. "
            "I’d be happy to help with appointments, services, or general questions. "
            "Could you tell me a little more about what you need?"
        )