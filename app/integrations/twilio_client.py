from twilio.rest import Client

from app.config import get_settings
from app.core.exceptions import IntegrationError


class TwilioSMSClient:
    def __init__(self) -> None:
        settings = get_settings()

        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.phone_number = settings.twilio_phone_number

        if not self.account_sid:
            raise IntegrationError("TWILIO_ACCOUNT_SID is not configured.")
        if not self.auth_token:
            raise IntegrationError("TWILIO_AUTH_TOKEN is not configured.")
        if not self.phone_number:
            raise IntegrationError("TWILIO_PHONE_NUMBER is not configured.")

        try:
            self.client = Client(self.account_sid, self.auth_token)
        except Exception as exc:
            raise IntegrationError(f"Failed to initialize Twilio client: {exc}") from exc

    def send_sms(self, *, to: str, body: str) -> dict:
        try:
            message = self.client.messages.create(
                body=body,
                from_=self.phone_number,
                to=to,
            )
            return {
                "message_sid": message.sid,
                "status": message.status,
                "to": message.to,
                "from": message.from_,
                "body": message.body,
            }
        except Exception as exc:
            raise IntegrationError(f"Failed to send SMS via Twilio: {exc}") from exc