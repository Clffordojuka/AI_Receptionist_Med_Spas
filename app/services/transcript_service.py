from sqlalchemy.orm import Session

from app.db.repositories.conversation_repository import ConversationRepository


class TranscriptService:
    def __init__(self, db: Session) -> None:
        self.repo = ConversationRepository(db)

    def get_history(self, lead_id: int):
        return self.repo.get_by_lead_id(lead_id)