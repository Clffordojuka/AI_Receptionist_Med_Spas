from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models.faq import FAQ


class FAQRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> FAQ:
        faq = FAQ(**data)
        self.db.add(faq)
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def get_all_active(self) -> list[FAQ]:
        return (
            self.db.query(FAQ)
            .filter(FAQ.active.is_(True))
            .order_by(FAQ.id.asc())
            .all()
        )

    def search(self, query_text: str) -> list[FAQ]:
        pattern = f"%{query_text.lower()}%"
        return (
            self.db.query(FAQ)
            .filter(FAQ.active.is_(True))
            .filter(
                or_(
                    FAQ.question.ilike(pattern),
                    FAQ.answer.ilike(pattern),
                    FAQ.category.ilike(pattern),
                )
            )
            .order_by(FAQ.id.asc())
            .all()
        )