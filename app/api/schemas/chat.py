from datetime import datetime
from pydantic import BaseModel, Field


class LeadSnapshotResponse(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    service_interest: str | None = None
    new_or_returning: str | None = None
    qualification_status: str | None = None
    lead_status: str | None = None


class ChatMessageRequest(BaseModel):
    lead_id: int
    message: str = Field(..., min_length=1)
    channel: str = "webchat"


class ChatMessageResponse(BaseModel):
    lead_id: int
    user_message: str
    assistant_message: str
    detected_intent: str
    confidence_score: float | None = None
    channel: str
    lead_snapshot: LeadSnapshotResponse


class ConversationMessageResponse(BaseModel):
    id: int
    lead_id: int
    channel: str
    message_role: str
    message_text: str
    intent: str | None = None
    confidence_score: float | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ConversationHistoryResponse(BaseModel):
    lead_id: int
    messages: list[ConversationMessageResponse]