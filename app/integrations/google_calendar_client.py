class GoogleCalendarClient:
    def create_event(
        self,
        *,
        title: str,
        start_time,
        end_time,
        description: str | None = None,
    ) -> dict:
        """
        Placeholder for future Google Calendar integration.
        For now, this returns a mock calendar event response.
        """
        return {
            "event_id": None,
            "status": "mocked",
            "title": title,
        }