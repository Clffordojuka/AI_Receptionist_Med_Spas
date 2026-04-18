import re


class IntentRouter:
    FAQ_KEYWORDS = [
        "price", "cost", "location", "hours", "open", "service",
        "treatment", "consultation", "botox", "filler", "facial",
    ]
    BOOKING_KEYWORDS = [
        "book", "appointment", "schedule", "available", "slot",
        "calendar", "tomorrow", "today", "next week",
    ]
    QUALIFICATION_KEYWORDS = [
        "new client", "returning", "interested", "looking for",
        "want to", "need", "help me",
    ]
    HUMAN_HANDOFF_KEYWORDS = [
        "human", "person", "someone", "speak to staff", "real person",
        "call me", "complaint",
    ]

    @classmethod
    def detect_intent(cls, message: str) -> tuple[str, float]:
        text = message.lower().strip()

        if not text:
            return "unknown", 0.0

        for keyword in cls.HUMAN_HANDOFF_KEYWORDS:
            if keyword in text:
                return "handoff_request", 0.95

        for keyword in cls.BOOKING_KEYWORDS:
            if keyword in text:
                return "booking", 0.90

        for keyword in cls.FAQ_KEYWORDS:
            if keyword in text:
                return "faq", 0.85

        for keyword in cls.QUALIFICATION_KEYWORDS:
            if keyword in text:
                return "qualification", 0.80

        if re.search(r"\b(hi|hello|hey|good morning|good afternoon)\b", text):
            return "greeting", 0.90

        return "general_inquiry", 0.60