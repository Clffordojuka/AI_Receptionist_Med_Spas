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