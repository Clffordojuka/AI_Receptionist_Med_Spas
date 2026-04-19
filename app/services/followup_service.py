from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.constants import BookingStatus, FollowUpStatus, LeadStatus
from app.core.exceptions import NotFoundError, ValidationError
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.followup_repository import FollowUpRepository
from app.db.repositories.lead_repository import LeadRepository
from app.services.notification_service import NotificationService


class FollowUpService:
    MAX_ATTEMPTS = 3

    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.followup_repo = FollowUpRepository(db)
        self.conversation_repo = ConversationRepository(db)
        self.notification_service = NotificationService()

    def create_followup(
        self,
        *,
        lead_id: int,
        scheduled_for: datetime,
        message_template: str | None = None,
        attempt_number: int = 1,
    ):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        if lead.booking_status == BookingStatus.CONFIRMED or lead.lead_status == LeadStatus.BOOKED:
            raise ValidationError("Cannot create follow-up for a lead that has already booked.")

        if attempt_number > self.MAX_ATTEMPTS:
            raise ValidationError(f"Maximum follow-up attempts is {self.MAX_ATTEMPTS}.")

        if scheduled_for.tzinfo is None:
            scheduled_for = scheduled_for.replace(tzinfo=timezone.utc)

        if lead.lead_status == LeadStatus.NEW:
            self.lead_repo.update(lead, {"lead_status": LeadStatus.PENDING_FOLLOWUP})

        return self.followup_repo.create(
            {
                "lead_id": lead_id,
                "scheduled_for": scheduled_for,
                "status": FollowUpStatus.PENDING,
                "message_template": message_template,
                "attempt_number": attempt_number,
            }
        )

    def auto_schedule_initial_followup(self, lead_id: int, hours_ahead: int = 24):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        if lead.booking_status == BookingStatus.CONFIRMED or lead.lead_status == LeadStatus.BOOKED:
            return None

        existing_pending = self.followup_repo.get_active_pending_for_lead(lead_id)
        if existing_pending:
            return existing_pending[0]

        scheduled_for = datetime.now(timezone.utc) + timedelta(hours=hours_ahead)

        if lead.lead_status in {LeadStatus.NEW, LeadStatus.QUALIFYING, LeadStatus.QUALIFIED}:
            self.lead_repo.update(lead, {"lead_status": LeadStatus.PENDING_FOLLOWUP})

        return self.followup_repo.create(
            {
                "lead_id": lead_id,
                "scheduled_for": scheduled_for,
                "status": FollowUpStatus.PENDING,
                "message_template": None,
                "attempt_number": 1,
            }
        )

    def cancel_pending_followups_for_lead(self, lead_id: int) -> int:
        pending_jobs = self.followup_repo.get_active_pending_for_lead(lead_id)
        cancelled_count = 0

        for job in pending_jobs:
            self.followup_repo.update(job, {"status": FollowUpStatus.CANCELLED})
            cancelled_count += 1

        return cancelled_count

    def get_lead_followups(self, lead_id: int):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")
        return self.followup_repo.get_by_lead_id(lead_id)

    def run_due_followups(self) -> dict:
        due_jobs = self.followup_repo.get_pending_due_jobs()

        processed = 0
        sent = 0
        cancelled = 0
        failed = 0

        for job in due_jobs:
            processed += 1
            lead = self.lead_repo.get_by_id(job.lead_id)

            if not lead:
                self.followup_repo.update(job, {"status": FollowUpStatus.FAILED})
                failed += 1
                continue

            if lead.booking_status == BookingStatus.CONFIRMED or lead.lead_status == LeadStatus.BOOKED:
                self.followup_repo.update(job, {"status": FollowUpStatus.CANCELLED})
                cancelled += 1
                continue

            try:
                message = job.message_template or self.notification_service.build_followup_message(
                    lead_name=lead.full_name,
                    service_interest=lead.service_interest,
                    attempt_number=job.attempt_number,
                )

                self.conversation_repo.create(
                    lead_id=lead.id,
                    channel="system_followup",
                    message_role="assistant",
                    message_text=message,
                    intent="follow_up",
                    confidence_score=1.0,
                )

                self.followup_repo.update(
                    job,
                    {
                        "status": FollowUpStatus.SENT,
                        "executed_at": datetime.now(timezone.utc),
                    },
                )
                sent += 1

                if job.attempt_number < self.MAX_ATTEMPTS:
                    self.followup_repo.create(
                        {
                            "lead_id": lead.id,
                            "scheduled_for": datetime.now(timezone.utc) + timedelta(hours=24),
                            "status": FollowUpStatus.PENDING,
                            "message_template": None,
                            "attempt_number": job.attempt_number + 1,
                        }
                    )

            except Exception:
                self.followup_repo.update(job, {"status": FollowUpStatus.FAILED})
                failed += 1

        return {
            "processed_jobs": processed,
            "sent_jobs": sent,
            "cancelled_jobs": cancelled,
            "failed_jobs": failed,
        }