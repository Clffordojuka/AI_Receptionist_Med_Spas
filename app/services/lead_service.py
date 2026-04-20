from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.repositories.lead_repository import LeadRepository
from app.api.schemas.lead import LeadCreate, LeadUpdate


class LeadService:
    def __init__(self, db: Session) -> None:
        self.repo = LeadRepository(db)

    def create_lead(self, payload: LeadCreate):
        return self.repo.create(payload.model_dump())

    def get_lead(self, lead_id: int):
        lead = self.repo.get_by_id(lead_id)
        if not lead:
            raise NotFoundError(f"Lead with id={lead_id} not found.")
        return lead

    def update_lead(self, lead_id: int, payload: LeadUpdate):
        lead = self.get_lead(lead_id)
        update_data = payload.model_dump(exclude_unset=True)
        return self.repo.update(lead, update_data)

    def patch_lead_fields(self, lead_id: int, update_data: dict):
        lead = self.get_lead(lead_id)

        safe_updates = {
            key: value for key, value in update_data.items()
            if value is not None and value != ""
        }

        if not safe_updates:
            return lead

        return self.repo.update(lead, safe_updates)

    def list_leads(
        self,
        *,
        lead_status: str | None = None,
        booking_status: str | None = None,
        qualification_status: str | None = None,
        handoff_requested: bool | None = None,
        limit: int = 100,
    ):
        return self.repo.list_leads(
            lead_status=lead_status,
            booking_status=booking_status,
            qualification_status=qualification_status,
            handoff_requested=handoff_requested,
            limit=limit,
        )

    def get_dashboard_summary(self):
        return self.repo.get_dashboard_summary()