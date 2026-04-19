import re
from sqlalchemy.orm import Session

from app.db.repositories.faq_repository import FAQRepository


class FAQService:
    def __init__(self, db: Session) -> None:
        self.repo = FAQRepository(db)

    def create_faq(self, payload):
        return self.repo.create(payload.model_dump())

    def find_best_match(self, user_message: str):
        faqs = self.repo.get_all_active()
        if not faqs:
            return None

        message_tokens = self._tokenize(user_message)
        if not message_tokens:
            return None

        best_faq = None
        best_score = 0

        for faq in faqs:
            faq_text = f"{faq.question} {faq.answer} {faq.category or ''}"
            faq_tokens = self._tokenize(faq_text)

            overlap = message_tokens.intersection(faq_tokens)
            score = len(overlap)

            if score > best_score:
                best_score = score
                best_faq = faq

        if best_score >= 2:
            return best_faq

        return None

    def _tokenize(self, text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())
        stop_words = {
            "the", "is", "a", "an", "and", "or", "to", "for", "of", "in",
            "on", "at", "do", "does", "i", "you", "we", "me", "my", "our",
            "what", "when", "where", "how", "are", "your",
        }
        return {word for word in words if word not in stop_words}