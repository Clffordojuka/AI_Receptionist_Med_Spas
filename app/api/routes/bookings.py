from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.schemas.booking import BookingCreateRequest, BookingResponse, SlotResponse
from app.core.exceptions import IntegrationError, NotFoundError, ValidationError
from app.dependencies import get_db
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/slots", response_model=list[SlotResponse])
def get_available_slots(
    lead_id: int = Query(...),
    service_name: str | None = Query(None),
    date: str | None = Query(None),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    try:
        return service.get_slots(
            lead_id=lead_id,
            service_name=service_name,
            date=date,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreateRequest, db: Session = Depends(get_db)):
    service = BookingService(db)
    try:
        return service.create_booking(
            lead_id=payload.lead_id,
            service_name=payload.service_name,
            appointment_datetime=payload.appointment_datetime,
            provider_name=payload.provider_name,
            notes=payload.notes,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/lead/{lead_id}", response_model=list[BookingResponse])
def get_lead_bookings(lead_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    try:
        return service.get_lead_bookings(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc