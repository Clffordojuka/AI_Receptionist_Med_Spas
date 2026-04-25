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

        candidate_hours = [9, 11, 13, 15]
        duration = timedelta(minutes=60)

        day_start = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = base_date.replace(hour=23, minute=59, second=59, microsecond=0)

        existing_events = self.client.list_events(
            time_min=day_start,
            time_max=day_end,
        )

        busy_ranges = []
        for event in existing_events:
            start = event.get("start", {}).get("dateTime")
            end = event.get("end", {}).get("dateTime")
            if start and end:
                busy_ranges.append(
                    (
                        datetime.fromisoformat(start),
                        datetime.fromisoformat(end),
                    )
                )

        slots = []
        for hour in candidate_hours:
            start_dt = base_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_dt = start_dt + duration

            if self._is_slot_available(start_dt, end_dt, busy_ranges):
                slots.append(
                    {
                        "start_time": start_dt,
                        "end_time": end_dt,
                        "provider_name": "Med Spa Team",
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

    def _is_slot_available(
        self,
        start_dt: datetime,
        end_dt: datetime,
        busy_ranges: list[tuple[datetime, datetime]],
    ) -> bool:
        for busy_start, busy_end in busy_ranges:
            if start_dt < busy_end and end_dt > busy_start:
                return False
        return True