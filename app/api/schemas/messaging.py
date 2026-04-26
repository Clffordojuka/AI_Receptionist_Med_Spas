from pydantic import BaseModel


class SMSOutboundRequest(BaseModel):
    lead_id: int | None = None
    to: str
    body: str


class SMSOutboundResponse(BaseModel):
    message_sid: str | None = None
    status: str | None = None
    to: str | None = None
    from_: str | None = None
    body: str | None = None


class SMSWebhookResponse(BaseModel):
    status: str
    lead_id: int | None = None
    incoming_from: str | None = None
    assistant_message: str | None = None