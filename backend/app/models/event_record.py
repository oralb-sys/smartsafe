import uuid
from datetime import datetime, timezone

from sqlalchemy import DECIMAL, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from decimal import Decimal

class EventRecord(Base):
    __tablename__ = "event_records"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
    )
    event_type_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("event_types.id"),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    latitude: Mapped[Decimal] = mapped_column(
        DECIMAL(9, 6),
        nullable=False,
    )
    longitude: Mapped[Decimal] = mapped_column(
        DECIMAL(9, 6),
        nullable=False,
    )
    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
    "User",
    back_populates="events",
    )
    event_type: Mapped["EventType"] = relationship(
    "EventType",
    back_populates="events",
    )