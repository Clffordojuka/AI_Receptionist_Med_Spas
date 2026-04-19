from datetime import datetime
from pydantic import BaseModel, Field


class FollowUpCreateRequest(BaseModel):
    lead_id: int
    scheduled_for: datetime
    message_template: str | None = None
    attempt_number: int = Field(default=1, ge=1)


class FollowUpResponse(BaseModel):
    id: int
    lead_id: int
    scheduled_for: datetime
    status: str
    message_template: str | None = None
    attempt_number: int
    executed_at: datetime | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class FollowUpExecutionResponse(BaseModel):
    processed_jobs: int
    sent_jobs: int
    cancelled_jobs: int
    failed_jobs: int