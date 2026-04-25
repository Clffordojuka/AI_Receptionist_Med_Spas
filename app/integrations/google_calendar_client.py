from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config import get_settings
from app.core.exceptions import IntegrationError


class GoogleCalendarClient:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self) -> None:
        settings = get_settings()

        self.calendar_id = settings.google_calendar_id
        self.credentials_path = self._resolve_credentials_path(
            settings.google_calendar_credentials_path
        )

        if not self.credentials_path:
            raise IntegrationError(
                "Google Calendar credentials file could not be found. "
                "Check GOOGLE_CALENDAR_CREDENTIALS_PATH and make sure the JSON key exists."
            )

        if not self.calendar_id:
            raise IntegrationError("GOOGLE_CALENDAR_ID is not configured.")

        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(self.credentials_path),
                scopes=self.SCOPES,
            )

            self.service = build(
                "calendar",
                "v3",
                credentials=credentials,
                cache_discovery=False,
            )
        except Exception as exc:
            raise IntegrationError(
                f"Failed to initialize Google Calendar client: {exc}"
            ) from exc

    def list_events(
        self,
        *,
        time_min: datetime,
        time_max: datetime,
    ) -> list[dict]:
        try:
            result = (
                self.service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=time_min.isoformat(),
                    timeMax=time_max.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return result.get("items", [])
        except Exception as exc:
            raise IntegrationError(f"Failed to list calendar events: {exc}") from exc

    def create_event(
        self,
        *,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: str | None = None,
    ) -> dict:
        event_body = {
            "summary": title,
            "description": description or "",
            "start": {
                "dateTime": start_time.isoformat(),
            },
            "end": {
                "dateTime": end_time.isoformat(),
            },
        }

        try:
            created_event = (
                self.service.events()
                .insert(calendarId=self.calendar_id, body=event_body)
                .execute()
            )

            return {
                "event_id": created_event.get("id"),
                "status": created_event.get("status"),
                "html_link": created_event.get("htmlLink"),
                "title": created_event.get("summary"),
            }
        except Exception as exc:
            raise IntegrationError(f"Failed to create calendar event: {exc}") from exc

    def _resolve_credentials_path(self, configured_path: str | None) -> Path | None:
        candidates: list[Path] = []

        if configured_path:
            configured = Path(configured_path)

            # 1. Use the configured path directly
            candidates.append(configured)

            # 2. If relative, resolve from project root
            if not configured.is_absolute():
                project_root = Path(__file__).resolve().parents[2]
                candidates.append(project_root / configured)

        # 3. Docker fallback
        candidates.append(Path("/app/credentials/google_service_account.json"))

        # 4. Local fallback
        project_root = Path(__file__).resolve().parents[2]
        candidates.append(project_root / "credentials" / "google_service_account.json")

        seen: set[str] = set()
        for candidate in candidates:
            resolved = candidate.resolve(strict=False)
            key = str(resolved)

            if key in seen:
                continue
            seen.add(key)

            if resolved.exists() and resolved.is_file():
                return resolved

        return None