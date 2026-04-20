from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.dashboard import DashboardSummaryResponse
from app.dependencies import get_db
from app.services.lead_service import LeadService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    service = LeadService(db)
    return service.get_dashboard_summary()