from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event_record import EventRecord
from app.models.event_type import EventType


class EventRecordRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
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
        statement = select(
            EventRecord
        ).where(
            EventRecord.id == event_id
        )

        return self.session.scalar(
            statement
        )

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
        statement = (
            select(EventRecord)
            .where(
                EventRecord.id == event_id,
                EventRecord.user_id == user_id,
            )
        )

        return self.session.scalar(
            statement
        )

    def update_status(
        self,
        event: EventRecord,
        new_status: str,
    ) -> EventRecord:
        event.status = new_status

        self.session.commit()
        self.session.refresh(event)

        return event

    def update_location(
        self,
        event: EventRecord,
        latitude: Decimal,
        longitude: Decimal,
    ) -> EventRecord:
        event.latitude = latitude
        event.longitude = longitude

        self.session.commit()
        self.session.refresh(event)

        return event

    def list_smart_sos_emergencies(
        self,
    ) -> list[EventRecord]:
        statement = (
            select(EventRecord)
            .join(
                EventType,
                EventRecord.event_type_id
                == EventType.id,
            )
            .where(
                EventType.module == "SMART_SOS"
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

    def get_smart_sos_emergency_by_id(
        self,
        emergency_id: str,
    ) -> EventRecord | None:
        statement = (
            select(EventRecord)
            .join(
                EventType,
                EventRecord.event_type_id
                == EventType.id,
            )
            .where(
                EventRecord.id == emergency_id,
                EventType.module == "SMART_SOS",
            )
        )

        return self.session.scalar(
            statement
        )

    def list_urban_events(
        self,
        source: str | None = None,
        event_type: str | None = None,
        status: str | None = None,
    ) -> list[
        tuple[
            EventRecord,
            EventType,
        ]
    ]:
        statement = (
            select(
                EventRecord,
                EventType,
            )
            .join(
                EventType,
                EventRecord.event_type_id
                == EventType.id,
            )
            .where(
                EventType.module.in_(
                    [
                        "SMART_REPORT",
                        "SMART_SOS",
                    ]
                )
            )
        )

        if source is not None:
            statement = statement.where(
                EventType.module == source
            )

        if event_type is not None:
            statement = statement.where(
                EventType.code == event_type
            )

        if status is not None:
            statement = statement.where(
                EventRecord.status == status
            )

        statement = statement.order_by(
            EventRecord.created_at.desc()
        )

        return [
            (
                event_record,
                event_type_record,
            )
            for (
                event_record,
                event_type_record,
            ) in self.session.execute(
                statement
            ).all()
        ]