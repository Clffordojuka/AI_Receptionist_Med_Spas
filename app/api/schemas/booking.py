from datetime import datetime
from pydantic import BaseModel, Field


class SlotResponse(BaseModel):
    start_time: datetime
    end_time: datetime
    provider_name: str
    service_name: str | None = None
    available: bool = True


class BookingSlotsRequest(BaseModel):
    lead_id: int
    service_name: str | None = None
    date: str | None = None


class BookingCreateRequest(BaseModel):
    lead_id: int
    service_name: str = Field(..., min_length=1)
    appointment_datetime: datetime
    provider_name: str | None = None
    notes: str | None = None


class BookingResponse(BaseModel):
    id: int
    lead_id: int
    service_name: str | None
    appointment_datetime: datetime | None
    provider_name: str | None
    calendar_event_id: str | None
    booking_status: str
    notes: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }