class LeadStatus:
    NEW = "new"
    QUALIFYING = "qualifying"
    QUALIFIED = "qualified"
    BOOKED = "booked"
    PENDING_FOLLOWUP = "pending_followup"
    CLOSED = "closed"


class BookingStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class QualificationStatus:
    UNKNOWN = "unknown"
    IN_PROGRESS = "in_progress"
    QUALIFIED = "qualified"
    NOT_QUALIFIED = "not_qualified"