from app.db.session import SessionLocal
from app.services.followup_service import FollowUpService


def run_followup_jobs() -> dict:
    db = SessionLocal()
    try:
        service = FollowUpService(db)
        return service.run_due_followups()
    finally:
        db.close()