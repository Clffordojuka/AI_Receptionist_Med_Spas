import re


class QualificationAgent:
    SERVICE_KEYWORDS = [
        "botox", "filler", "facial", "chemical peel", "microneedling",
        "consultation", "laser", "skin treatment", "lip filler",
    ]

    @classmethod
    def extract_fields(cls, message: str) -> dict:
        text = message.strip()
        lowered = text.lower()

        extracted: dict = {}

        service = cls._extract_service(lowered)
        if service:
            extracted["service_interest"] = service

        client_status = cls._extract_client_status(lowered)
        if client_status:
            extracted["new_or_returning"] = client_status

        phone = cls._extract_phone(text)
        if phone:
            extracted["phone"] = phone

        email = cls._extract_email(text)
        if email:
            extracted["email"] = email

        full_name = cls._extract_name(text)
        if full_name:
            extracted["full_name"] = full_name

        return extracted

    @classmethod
    def _extract_service(cls, lowered: str) -> str | None:
        for service in cls.SERVICE_KEYWORDS:
            if service in lowered:
                return service.title()
        return None

    @staticmethod
    def _extract_client_status(lowered: str) -> str | None:
        if "new client" in lowered or "first time" in lowered or "new here" in lowered:
            return "new"
        if "returning" in lowered or "existing client" in lowered:
            return "returning"
        return None

    @staticmethod
    def _extract_phone(text: str) -> str | None:
        match = re.search(r"(\+?\d[\d\-\s]{7,}\d)", text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_email(text: str) -> str | None:
        match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_name(text: str) -> str | None:
        patterns = [
            r"(?:my name is|i am|i'm)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None