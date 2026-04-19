class HandoffDetector:
    KEYWORDS = [
        "human",
        "real person",
        "speak to someone",
        "talk to someone",
        "staff",
        "call me",
        "complaint",
        "issue",
        "problem",
        "not happy",
        "frustrated",
        "angry",
        "unsafe",
    ]

    @classmethod
    def should_handoff(cls, message: str, detected_intent: str, confidence_score: float | None) -> bool:
        text = message.lower().strip()

        if detected_intent == "handoff_request":
            return True

        for keyword in cls.KEYWORDS:
            if keyword in text:
                return True

        if confidence_score is not None and confidence_score < 0.45:
            return True

        return False