from sqlalchemy.orm import Session

from app.ai.intent_router import IntentRouter
from app.ai.response_generator import ResponseGenerator
from app.core.exceptions import NotFoundError
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.lead_repository import LeadRepository


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.conversation_repo = ConversationRepository(db)
        self.response_generator = ResponseGenerator()

    def process_message(self, *, lead_id: int, message: str, channel: str):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        detected_intent, confidence = IntentRouter.detect_intent(message)

        self.conversation_repo.create(
            lead_id=lead_id,
            channel=channel,
            message_role="user",
            message_text=message,
            intent=detected_intent,
            confidence_score=confidence,
        )

        history_objects = self.conversation_repo.get_by_lead_id(lead_id)
        history_payload = [
            {
                "role": item.message_role,
                "content": item.message_text,
            }
            for item in history_objects
        ]

        assistant_message = self.response_generator.generate(
            user_message=message,
            detected_intent=detected_intent,
            conversation_history=history_payload,
        )

        self.conversation_repo.create(
            lead_id=lead_id,
            channel=channel,
            message_role="assistant",
            message_text=assistant_message,
            intent=detected_intent,
            confidence_score=confidence,
        )

        return {
            "lead_id": lead_id,
            "user_message": message,
            "assistant_message": assistant_message,
            "detected_intent": detected_intent,
            "confidence_score": confidence,
            "channel": channel,
        }

    def get_conversation_history(self, lead_id: int):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        messages = self.conversation_repo.get_by_lead_id(lead_id)
        return {
            "lead_id": lead_id,
            "messages": messages,
        }