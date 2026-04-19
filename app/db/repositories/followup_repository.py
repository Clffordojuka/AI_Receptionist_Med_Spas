from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.followup_job import FollowUpJob


class FollowUpRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> FollowUpJob:
        job = FollowUpJob(**data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_id(self, followup_id: int) -> FollowUpJob | None:
        return (
            self.db.query(FollowUpJob)
            .filter(FollowUpJob.id == followup_id)
            .first()
        )

    def get_by_lead_id(self, lead_id: int) -> list[FollowUpJob]:
        return (
            self.db.query(FollowUpJob)
            .filter(FollowUpJob.lead_id == lead_id)
            .order_by(FollowUpJob.scheduled_for.asc(), FollowUpJob.id.asc())
            .all()
        )

    def get_pending_due_jobs(self) -> list[FollowUpJob]:
        now = datetime.now(timezone.utc)
        return (
            self.db.query(FollowUpJob)
            .filter(FollowUpJob.status == "pending")
            .filter(FollowUpJob.scheduled_for <= now)
            .order_by(FollowUpJob.scheduled_for.asc(), FollowUpJob.id.asc())
            .all()
        )

    def get_active_pending_for_lead(self, lead_id: int) -> list[FollowUpJob]:
        return (
            self.db.query(FollowUpJob)
            .filter(FollowUpJob.lead_id == lead_id)
            .filter(FollowUpJob.status == "pending")
            .order_by(FollowUpJob.scheduled_for.asc(), FollowUpJob.id.asc())
            .all()
        )

    def update(self, job: FollowUpJob, data: dict) -> FollowUpJob:
        for key, value in data.items():
            setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return job