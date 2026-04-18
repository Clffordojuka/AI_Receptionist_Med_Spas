from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.core.constants import LeadStatus, QualificationStatus, BookingStatus


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=False)
    source_channel: Mapped[str] = mapped_column(String(100), default="webchat", nullable=False)
    service_interest: Mapped[str | None] = mapped_column(String(255), nullable=True)
    new_or_returning: Mapped[str | None] = mapped_column(String(50), nullable=True)

    qualification_status: Mapped[str] = mapped_column(
        String(50),
        default=QualificationStatus.UNKNOWN,
        nullable=False,
    )
    booking_status: Mapped[str] = mapped_column(
        String(50),
        default=BookingStatus.PENDING,
        nullable=False,
    )
    lead_status: Mapped[str] = mapped_column(
        String(50),
        default=LeadStatus.NEW,
        nullable=False,
    )

    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )