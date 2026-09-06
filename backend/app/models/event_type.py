import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class EventType(Base):
    __tablename__ = "event_types"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    module: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    events: Mapped[list["EventRecord"]] = relationship(
        "EventRecord",
        back_populates="event_type",
    )