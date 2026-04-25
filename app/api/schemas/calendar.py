from datetime import datetime
from pydantic import BaseModel


class CalendarHealthResponse(BaseModel):
    status: str
    calendar_id: str
    credentials_path: str


class CalendarEventResponse(BaseModel):
    id: str | None = None
    summary: str | None = None
    status: str | None = None
    start: str | None = None
    end: str | None = None
    html_link: str | None = None


class CalendarTestEventRequest(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    description: str | None = None


class CalendarTestEventResponse(BaseModel):
    event_id: str | None = None
    status: str | None = None
    html_link: str | None = None
    title: str | None = None