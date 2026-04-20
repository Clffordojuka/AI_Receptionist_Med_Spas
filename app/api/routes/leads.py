from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.schemas.lead import LeadCreate, LeadListItemResponse, LeadResponse, LeadUpdate
from app.dependencies import get_db
from app.services.lead_service import LeadService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    service = LeadService(db)
    return service.create_lead(payload)


@router.get("", response_model=list[LeadListItemResponse])
def list_leads(
    lead_status: str | None = Query(None),
    booking_status: str | None = Query(None),
    qualification_status: str | None = Query(None),
    handoff_requested: bool | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    service = LeadService(db)
    return service.list_leads(
        lead_status=lead_status,
        booking_status=booking_status,
        qualification_status=qualification_status,
        handoff_requested=handoff_requested,
        limit=limit,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    service = LeadService(db)
    try:
        return service.get_lead(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db)):
    service = LeadService(db)
    try:
        return service.update_lead(lead_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc