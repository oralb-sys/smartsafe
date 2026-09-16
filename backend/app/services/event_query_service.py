from app.models.event_record import EventRecord
from app.models.event_type import EventType
from app.repositories.event_record_repository import (
    EventRecordRepository,
)


class EventQueryService:
    def __init__(
        self,
        event_record_repository: EventRecordRepository,
    ) -> None:
        self.event_record_repository = (
            event_record_repository
        )

    def list_events(
        self,
    ) -> list[
        tuple[
            EventRecord,
            EventType,
        ]
    ]:
        return (
            self.event_record_repository
            .list_urban_events()
        )