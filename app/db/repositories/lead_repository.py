from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.lead import Lead


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> Lead:
        lead = Lead(**data)
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def get_by_id(self, lead_id: int) -> Lead | None:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def update(self, lead: Lead, data: dict) -> Lead:
        for key, value in data.items():
            setattr(lead, key, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def list_leads(
        self,
        *,
        lead_status: str | None = None,
        booking_status: str | None = None,
        qualification_status: str | None = None,
        handoff_requested: bool | None = None,
        limit: int = 100,
    ) -> list[Lead]:
        query = self.db.query(Lead)

        if lead_status:
            query = query.filter(Lead.lead_status == lead_status)

        if booking_status:
            query = query.filter(Lead.booking_status == booking_status)

        if qualification_status:
            query = query.filter(Lead.qualification_status == qualification_status)

        if handoff_requested is not None:
            query = query.filter(Lead.handoff_requested == handoff_requested)

        return (
            query.order_by(Lead.updated_at.desc(), Lead.id.desc())
            .limit(limit)
            .all()
        )

    def get_dashboard_summary(self) -> dict:
        total_leads = self.db.query(func.count(Lead.id)).scalar() or 0
        booked_leads = (
            self.db.query(func.count(Lead.id))
            .filter(Lead.booking_status == "confirmed")
            .scalar()
            or 0
        )
        handoff_leads = (
            self.db.query(func.count(Lead.id))
            .filter(Lead.handoff_requested.is_(True))
            .scalar()
            or 0
        )
        pending_followup_leads = (
            self.db.query(func.count(Lead.id))
            .filter(Lead.lead_status == "pending_followup")
            .scalar()
            or 0
        )
        qualifying_leads = (
            self.db.query(func.count(Lead.id))
            .filter(Lead.lead_status == "qualifying")
            .scalar()
            or 0
        )

        return {
            "total_leads": total_leads,
            "booked_leads": booked_leads,
            "handoff_leads": handoff_leads,
            "pending_followup_leads": pending_followup_leads,
            "qualifying_leads": qualifying_leads,
        }