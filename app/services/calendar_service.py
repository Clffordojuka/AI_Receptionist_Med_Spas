from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.integrations.google_calendar_client import GoogleCalendarClient


class CalendarService:
    def __init__(self) -> None:
        self.client = GoogleCalendarClient()
        self.timezone = ZoneInfo("Africa/Nairobi")

    def get_available_slots(
        self,
        *,
        service_name: str | None = None,
        date_str: str | None = None,
    ) -> list[dict]:
        base_date = self._resolve_base_date(date_str)

        providers = ["Front Desk Team", "Aesthetic Specialist"]
        hours = [9, 11, 13, 15]

        slots: list[dict] = []
        for hour in hours:
            start_dt = base_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_dt = start_dt + timedelta(minutes=60)

            slots.append(
                {
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "provider_name": providers[hour % len(providers)],
                    "service_name": service_name,
                    "available": True,
                }
            )

        return slots

    def create_calendar_booking(
        self,
        *,
        service_name: str,
        appointment_datetime: datetime,
        provider_name: str | None = None,
        lead_name: str | None = None,
    ) -> dict:
        start_dt = self._ensure_timezone(appointment_datetime)
        end_dt = start_dt + timedelta(minutes=60)

        title = f"{service_name} Appointment"
        if lead_name:
            title = f"{service_name} - {lead_name}"

        return self.client.create_event(
            title=title,
            start_time=start_dt,
            end_time=end_dt,
            description=f"Provider: {provider_name or 'TBD'}",
        )

    def _resolve_base_date(self, date_str: str | None) -> datetime:
        now = datetime.now(self.timezone)

        if date_str:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed.replace(tzinfo=self.timezone)

        next_day = now + timedelta(days=1)
        return next_day.replace(hour=0, minute=0, second=0, microsecond=0)

    def _ensure_timezone(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self.timezone)
        return dt.astimezone(self.timezone)