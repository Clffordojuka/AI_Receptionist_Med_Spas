from sqlalchemy.orm import Session

from app.ai.handoff_detector import HandoffDetector
from app.ai.intent_router import IntentRouter
from app.ai.qualification_agent import QualificationAgent
from app.ai.response_generator import ResponseGenerator
from app.core.constants import LeadStatus, QualificationStatus
from app.core.exceptions import NotFoundError
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.lead_repository import LeadRepository
from app.services.faq_service import FAQService
from app.services.followup_service import FollowUpService
from app.services.lead_service import LeadService


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.lead_service = LeadService(db)
        self.conversation_repo = ConversationRepository(db)
        self.response_generator = ResponseGenerator()
        self.faq_service = FAQService(db)
        self.followup_service = FollowUpService(db)

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

        extracted_fields = QualificationAgent.extract_fields(message)
        lead_update_payload = dict(extracted_fields)

        if extracted_fields:
            if lead.qualification_status == QualificationStatus.UNKNOWN:
                lead_update_payload["qualification_status"] = QualificationStatus.IN_PROGRESS
            if lead.lead_status == LeadStatus.NEW:
                lead_update_payload["lead_status"] = LeadStatus.QUALIFYING

            self.lead_service.patch_lead_fields(lead_id, lead_update_payload)

        history_objects = self.conversation_repo.get_by_lead_id(lead_id)
        history_payload = [
            {
                "role": item.message_role,
                "content": item.message_text,
            }
            for item in history_objects
        ]

        should_handoff = HandoffDetector.should_handoff(
            message=message,
            detected_intent=detected_intent,
            confidence_score=confidence,
        )

        faq_answer = None
        if detected_intent == "faq" and not should_handoff:
            faq_match = self.faq_service.find_best_match(message)
            if faq_match:
                faq_answer = faq_match.answer

        if should_handoff:
            self.lead_service.patch_lead_fields(
                lead_id,
                {
                    "handoff_requested": True,
                    "lead_status": LeadStatus.PENDING_FOLLOWUP,
                },
            )
            assistant_message = (
                "I understand. I’m flagging this for a team member to review and follow up with you. "
                "Please share any extra details you’d like the staff to see."
            )
        else:
            assistant_message = self.response_generator.generate(
                user_message=message,
                detected_intent=detected_intent,
                conversation_history=history_payload,
                faq_answer=faq_answer,
            )

        self.conversation_repo.create(
            lead_id=lead_id,
            channel=channel,
            message_role="assistant",
            message_text=assistant_message,
            intent="handoff" if should_handoff else detected_intent,
            confidence_score=confidence,
        )

        updated_lead = self.lead_repo.get_by_id(lead_id)

        if updated_lead and updated_lead.lead_status != LeadStatus.BOOKED and not updated_lead.handoff_requested:
            if detected_intent in {"qualification", "booking", "general_inquiry", "faq"}:
                self.followup_service.auto_schedule_initial_followup(lead_id)

        return {
            "lead_id": lead_id,
            "user_message": message,
            "assistant_message": assistant_message,
            "detected_intent": "handoff" if should_handoff else detected_intent,
            "confidence_score": confidence,
            "channel": channel,
            "lead_snapshot": {
                "full_name": updated_lead.full_name,
                "phone": updated_lead.phone,
                "email": updated_lead.email,
                "service_interest": updated_lead.service_interest,
                "new_or_returning": updated_lead.new_or_returning,
                "qualification_status": updated_lead.qualification_status,
                "lead_status": updated_lead.lead_status,
            },
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