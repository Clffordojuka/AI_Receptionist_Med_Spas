from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.admin import (
    LeadAdminUpdateRequest,
    LeadEscalationRequest,
    LeadReviewResponse,
)
from app.api.schemas.lead import LeadResponse
from app.core.exceptions import NotFoundError
from app.dependencies import get_db
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.patch("/leads/{lead_id}", response_model=LeadResponse)
def update_lead_admin_fields(
    lead_id: int,
    payload: LeadAdminUpdateRequest,
    db: Session = Depends(get_db),
):
    service = AdminService(db)
    try:
        return service.update_lead_admin_fields(lead_id, payload.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/escalate", response_model=LeadResponse)
def escalate_lead(
    lead_id: int,
    payload: LeadEscalationRequest,
    db: Session = Depends(get_db),
):
    service = AdminService(db)
    try:
        return service.escalate_lead(
            lead_id=lead_id,
            assigned_to=payload.assigned_to,
            admin_notes=payload.admin_notes,
            reason=payload.reason,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/review", response_model=LeadReviewResponse)
def get_lead_review(lead_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    try:
        return service.get_lead_review(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc