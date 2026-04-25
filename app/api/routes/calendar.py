from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas.booking import SlotResponse
from app.api.schemas.calendar import (
    CalendarEventResponse,
    CalendarHealthResponse,
    CalendarTestEventRequest,
    CalendarTestEventResponse,
)
from app.core.exceptions import IntegrationError
from app.services.calendar_debug_service import CalendarDebugService

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/health", response_model=CalendarHealthResponse)
def calendar_health():
    try:
        service = CalendarDebugService()
        return service.health()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/events", response_model=list[CalendarEventResponse])
def list_calendar_events(date: str | None = Query(None, description="Date in YYYY-MM-DD format")):
    try:
        service = CalendarDebugService()
        return service.list_events(date_str=date)
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/slots", response_model=list[SlotResponse])
def list_calendar_slots(
    service_name: str | None = Query(None),
    date: str | None = Query(None, description="Date in YYYY-MM-DD format"),
):
    try:
        service = CalendarDebugService()
        return service.get_slots(service_name=service_name, date_str=date)
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-event", response_model=CalendarTestEventResponse, status_code=status.HTTP_201_CREATED)
def create_calendar_test_event(payload: CalendarTestEventRequest):
    try:
        service = CalendarDebugService()
        return service.create_test_event(
            title=payload.title,
            start_time=payload.start_time,
            end_time=payload.end_time,
            description=payload.description,
        )
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc