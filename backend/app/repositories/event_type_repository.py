from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event_type import EventType


class EventTypeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_smart_report_type_by_code(self, code: str) -> EventType | None:
        statement = select(EventType).where(
            EventType.code == code,
            EventType.module == "SMART_REPORT",
        )
        return self.session.scalar(statement)
