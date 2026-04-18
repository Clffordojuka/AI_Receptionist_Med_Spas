from datetime import datetime
from pydantic import BaseModel, EmailStr


class LeadCreate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    source_channel: str = "webchat"
    service_interest: str | None = None
    new_or_returning: str | None = None


class LeadUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    source_channel: str | None = None
    service_interest: str | None = None
    new_or_returning: str | None = None
    qualification_status: str | None = None
    booking_status: str | None = None
    lead_status: str | None = None


class LeadResponse(BaseModel):
    id: int
    full_name: str | None
    phone: str | None
    email: EmailStr | None
    source_channel: str
    service_interest: str | None
    new_or_returning: str | None
    qualification_status: str
    booking_status: str
    lead_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }