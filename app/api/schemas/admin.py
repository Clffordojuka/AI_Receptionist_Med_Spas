from pydantic import BaseModel


class LeadAdminUpdateRequest(BaseModel):
    assigned_to: str | None = None
    admin_notes: str | None = None
    lead_status: str | None = None
    qualification_status: str | None = None
    booking_status: str | None = None
    handoff_requested: bool | None = None


class LeadEscalationRequest(BaseModel):
    assigned_to: str | None = None
    admin_notes: str | None = None
    reason: str | None = None


class LeadReviewResponse(BaseModel):
    lead_id: int
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    source_channel: str
    service_interest: str | None = None
    new_or_returning: str | None = None
    qualification_status: str
    booking_status: str
    lead_status: str
    assigned_to: str | None = None
    admin_notes: str | None = None
    handoff_requested: bool
    conversation_count: int