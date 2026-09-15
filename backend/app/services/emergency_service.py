from app.models.event_record import EventRecord
from app.repositories.event_record_repository import (
    EventRecordRepository,
)
from app.repositories.event_type_repository import (
    EventTypeRepository,
)


class EmergencyTypeNotFoundError(Exception):
    pass


class EmergencyService:
    def __init__(
        self,
        event_type_repository: EventTypeRepository,
        event_record_repository: EventRecordRepository,
    ) -> None:
        self.event_type_repository = event_type_repository
        self.event_record_repository = event_record_repository

    def create_emergency(
        self,
        user_id: str,
    ) -> EventRecord:
        event_type = (
            self.event_type_repository
            .get_smart_sos_type_by_code("SOS")
        )

        if event_type is None:
            raise EmergencyTypeNotFoundError(
                "El tipo inicial SOS no está configurado."
            )

        emergency = EventRecord(
            user_id=user_id,
            event_type_id=event_type.id,
            description=None,
            latitude=None,
            longitude=None,
            photo_url=None,
            status="ACTIVE",
        )

        return self.event_record_repository.create(
            emergency
        )