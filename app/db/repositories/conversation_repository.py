from sqlalchemy.orm import Session

from app.db.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        lead_id: int,
        channel: str,
        message_role: str,
        message_text: str,
        intent: str | None = None,
        confidence_score: float | None = None,
    ) -> Conversation:
        conversation = Conversation(
            lead_id=lead_id,
            channel=channel,
            message_role=message_role,
            message_text=message_text,
            intent=intent,
            confidence_score=confidence_score,
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_lead_id(self, lead_id: int) -> list[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(Conversation.lead_id == lead_id)
            .order_by(Conversation.created_at.asc(), Conversation.id.asc())
            .all()
        )