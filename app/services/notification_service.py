class NotificationService:
    def build_followup_message(
        self,
        *,
        lead_name: str | None = None,
        service_interest: str | None = None,
        attempt_number: int = 1,
    ) -> str:
        greeting = f"Hi {lead_name}," if lead_name else "Hello,"

        if service_interest:
            service_line = f" regarding your interest in {service_interest}"
        else:
            service_line = ""

        if attempt_number == 1:
            return (
                f"{greeting} just following up{service_line}. "
                "If you'd like, I can help you book your appointment or answer any questions."
            )

        if attempt_number == 2:
            return (
                f"{greeting} we wanted to check in again{service_line}. "
                "If you're still interested, I can help you choose a convenient appointment time."
            )

        return (
            f"{greeting} this is a final follow-up{service_line}. "
            "Let us know if you'd still like help with booking."
        )