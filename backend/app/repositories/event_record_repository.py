from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event_record import EventRecord


class EventRecordRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        event: EventRecord,
    ) -> EventRecord:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def get_by_id(
        self,
        event_id: str,
    ) -> EventRecord | None:
        statement = select(EventRecord).where(
            EventRecord.id == event_id
        )

        return self.session.scalar(statement)

    def update_photo_url(
        self,
        event: EventRecord,
        photo_url: str,
    ) -> EventRecord:
        event.photo_url = photo_url

        self.session.commit()
        self.session.refresh(event)

        return event

    def list_by_user_id(
        self,
        user_id: str,
    ) -> list[EventRecord]:
        statement = (
            select(EventRecord)
            .where(
                EventRecord.user_id == user_id
            )
            .order_by(
                EventRecord.created_at.desc()
            )
        )

        return list(
            self.session.scalars(
                statement
            ).all()
        )

    def get_by_id_and_user_id(
        self,
        event_id: str,
        user_id: str,
    ) -> EventRecord | None:
        statement = select(
            EventRecord
        ).where(
            EventRecord.id == event_id,
            EventRecord.user_id == user_id,
        )

        return self.session.scalar(
            statement
        )