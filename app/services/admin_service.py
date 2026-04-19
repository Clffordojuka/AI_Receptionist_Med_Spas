from sqlalchemy.orm import Session

from app.core.constants import LeadStatus
from app.core.exceptions import NotFoundError
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.lead_repository import LeadRepository


class AdminService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.conversation_repo = ConversationRepository(db)

    def update_lead_admin_fields(self, lead_id: int, data: dict):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        safe_updates = {
            key: value for key, value in data.items()
            if value is not None
        }

        return self.lead_repo.update(lead, safe_updates)

    def escalate_lead(
        self,
        *,
        lead_id: int,
        assigned_to: str | None = None,
        admin_notes: str | None = None,
        reason: str | None = None,
    ):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        existing_notes = lead.admin_notes or ""
        escalation_note_parts = []

        if reason:
            escalation_note_parts.append(f"Escalation reason: {reason}")
        if admin_notes:
            escalation_note_parts.append(admin_notes)

        combined_note = existing_notes
        if escalation_note_parts:
            joined = " | ".join(escalation_note_parts)
            combined_note = f"{existing_notes}\n{joined}".strip() if existing_notes else joined

        updated_lead = self.lead_repo.update(
            lead,
            {
                "handoff_requested": True,
                "lead_status": LeadStatus.PENDING_FOLLOWUP,
                "assigned_to": assigned_to or lead.assigned_to,
                "admin_notes": combined_note,
            },
        )

        self.conversation_repo.create(
            lead_id=lead.id,
            channel="admin_handoff",
            message_role="system",
            message_text=reason or "Lead escalated for human follow-up.",
            intent="handoff",
            confidence_score=1.0,
        )

        return updated_lead

    def get_lead_review(self, lead_id: int) -> dict:
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        conversations = self.conversation_repo.get_by_lead_id(lead_id)

        return {
            "lead_id": lead.id,
            "full_name": lead.full_name,
            "phone": lead.phone,
            "email": lead.email,
            "source_channel": lead.source_channel,
            "service_interest": lead.service_interest,
            "new_or_returning": lead.new_or_returning,
            "qualification_status": lead.qualification_status,
            "booking_status": lead.booking_status,
            "lead_status": lead.lead_status,
            "assigned_to": lead.assigned_to,
            "admin_notes": lead.admin_notes,
            "handoff_requested": lead.handoff_requested,
            "conversation_count": len(conversations),
        }