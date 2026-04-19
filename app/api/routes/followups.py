from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.followup import (
    FollowUpCreateRequest,
    FollowUpExecutionResponse,
    FollowUpResponse,
)
from app.core.exceptions import NotFoundError, ValidationError
from app.dependencies import get_db
from app.services.followup_service import FollowUpService

router = APIRouter(prefix="/followups", tags=["FollowUps"])


@router.post("", response_model=FollowUpResponse, status_code=status.HTTP_201_CREATED)
def create_followup(payload: FollowUpCreateRequest, db: Session = Depends(get_db)):
    service = FollowUpService(db)
    try:
        return service.create_followup(
            lead_id=payload.lead_id,
            scheduled_for=payload.scheduled_for,
            message_template=payload.message_template,
            attempt_number=payload.attempt_number,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/auto/{lead_id}", response_model=FollowUpResponse | None)
def auto_schedule_followup(lead_id: int, db: Session = Depends(get_db)):
    service = FollowUpService(db)
    try:
        return service.auto_schedule_initial_followup(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/run", response_model=FollowUpExecutionResponse)
def run_due_followups(db: Session = Depends(get_db)):
    service = FollowUpService(db)
    return service.run_due_followups()


@router.get("/lead/{lead_id}", response_model=list[FollowUpResponse])
def get_lead_followups(lead_id: int, db: Session = Depends(get_db)):
    service = FollowUpService(db)
    try:
        return service.get_lead_followups(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc