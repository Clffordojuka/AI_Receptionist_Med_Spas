from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import get_settings
from app.integrations.google_calendar_client import GoogleCalendarClient
from app.services.calendar_service import CalendarService


class CalendarDebugService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = GoogleCalendarClient()
        self.calendar_service = CalendarService()
        self.timezone = ZoneInfo("Africa/Nairobi")

    def health(self) -> dict:
        return {
            "status": "ok",
            "calendar_id": self.settings.google_calendar_id,
            "credentials_path": str(self.client.credentials_path),
        }

    def list_events(self, date_str: str | None = None) -> list[dict]:
        base_date = self._resolve_base_date(date_str)

        time_min = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = base_date.replace(hour=23, minute=59, second=59, microsecond=0)

        events = self.client.list_events(time_min=time_min, time_max=time_max)

        cleaned = []
        for event in events:
            cleaned.append(
                {
                    "id": event.get("id"),
                    "summary": event.get("summary"),
                    "status": event.get("status"),
                    "start": event.get("start", {}).get("dateTime") or event.get("start", {}).get("date"),
                    "end": event.get("end", {}).get("dateTime") or event.get("end", {}).get("date"),
                    "html_link": event.get("htmlLink"),
                }
            )
        return cleaned

    def get_slots(self, service_name: str | None = None, date_str: str | None = None) -> list[dict]:
        return self.calendar_service.get_available_slots(
            service_name=service_name,
            date_str=date_str,
        )

    def create_test_event(
        self,
        *,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: str | None = None,
    ) -> dict:
        return self.client.create_event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )

    def _resolve_base_date(self, date_str: str | None) -> datetime:
        now = datetime.now(self.timezone)

        if date_str:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed.replace(tzinfo=self.timezone)

        return now