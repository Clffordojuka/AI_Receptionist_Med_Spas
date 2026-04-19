from sqlalchemy.orm import Session

from app.core.constants import BookingStatus, LeadStatus, QualificationStatus
from app.core.exceptions import NotFoundError, ValidationError
from app.db.repositories.appointment_repository import AppointmentRepository
from app.db.repositories.lead_repository import LeadRepository
from app.services.calendar_service import CalendarService
from app.services.followup_service import FollowUpService
from app.services.lead_service import LeadService


class BookingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.lead_service = LeadService(db)
        self.appointment_repo = AppointmentRepository(db)
        self.calendar_service = CalendarService()
        self.followup_service = FollowUpService(db)

    def get_slots(
        self,
        *,
        lead_id: int,
        service_name: str | None = None,
        date: str | None = None,
    ) -> list[dict]:
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        resolved_service = service_name or lead.service_interest
        return self.calendar_service.get_available_slots(
            service_name=resolved_service,
            date_str=date,
        )

    def create_booking(
        self,
        *,
        lead_id: int,
        service_name: str,
        appointment_datetime,
        provider_name: str | None = None,
        notes: str | None = None,
    ):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")

        if not service_name:
            raise ValidationError("service_name is required for booking.")

        calendar_result = self.calendar_service.create_calendar_booking(
            service_name=service_name,
            appointment_datetime=appointment_datetime,
            provider_name=provider_name,
            lead_name=lead.full_name,
        )

        appointment = self.appointment_repo.create(
            {
                "lead_id": lead_id,
                "service_name": service_name,
                "appointment_datetime": appointment_datetime,
                "provider_name": provider_name,
                "calendar_event_id": calendar_result.get("event_id"),
                "booking_status": BookingStatus.CONFIRMED,
                "notes": notes,
            }
        )

        self.lead_service.patch_lead_fields(
            lead_id,
            {
                "service_interest": service_name,
                "booking_status": BookingStatus.CONFIRMED,
                "lead_status": LeadStatus.BOOKED,
                "qualification_status": QualificationStatus.QUALIFIED,
            },
        )

        self.followup_service.cancel_pending_followups_for_lead(lead_id)

        return appointment

    def get_lead_bookings(self, lead_id: int):
        lead = self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")
        return self.appointment_repo.get_by_lead_id(lead_id)