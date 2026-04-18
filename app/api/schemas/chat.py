from datetime import datetime
from pydantic import BaseModel, Field


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