from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.models.lead import Lead
from app.db.repositories.lead_repository import LeadRepository
from app.integrations.twilio_client import TwilioSMSClient
from app.services.chat_service import ChatService


class MessagingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.chat_service = ChatService(db)
        self.twilio_client = TwilioSMSClient()

    def send_sms(self, *, lead_id: int | None = None, to: str, body: str) -> dict:
        if lead_id is not None:
            lead = self.lead_repo.get_by_id(lead_id)
            if not lead:
                raise NotFoundError(f"Lead with id={lead_id} not found.")

        result = self.twilio_client.send_sms(to=to, body=body)

        return {
            "message_sid": result.get("message_sid"),
            "status": result.get("status"),
            "to": result.get("to"),
            "from_": result.get("from"),
            "body": result.get("body"),
        }

    def handle_incoming_sms(
        self,
        *,
        from_number: str,
        body: str,
    ) -> dict:
        lead = self._find_or_create_lead_by_phone(from_number)

        chat_result = self.chat_service.process_message(
            lead_id=lead.id,
            message=body,
            channel="sms",
        )

        assistant_message = chat_result.get("assistant_message")

        sms_result = self.twilio_client.send_sms(
            to=from_number,
            body=assistant_message,
        )

        return {
            "status": "processed",
            "lead_id": lead.id,
            "incoming_from": from_number,
            "assistant_message": assistant_message,
            "twilio_message_sid": sms_result.get("message_sid"),
        }

    def _find_or_create_lead_by_phone(self, phone: str):
        found = self.db.query(Lead).filter(Lead.phone == phone).first()
        if found:
            return found

        payload = {
            "full_name": None,
            "phone": phone,
            "email": None,
            "source_channel": "sms",
            "service_interest": None,
            "new_or_returning": None,
        }
        return self.lead_repo.create(payload)