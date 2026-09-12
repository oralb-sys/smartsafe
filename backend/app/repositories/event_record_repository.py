from sqlalchemy.orm import Session

from app.models.event_record import EventRecord


class EventRecordRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, event: EventRecord) -> EventRecord:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event
