from decimal import Decimal

from app.models.event_record import EventRecord
from app.repositories.event_record_repository import EventRecordRepository
from app.repositories.event_type_repository import EventTypeRepository


class InvalidReportCategoryError(Exception):
    pass


class ReportService:
    def __init__(
        self,
        event_type_repository: EventTypeRepository,
        event_record_repository: EventRecordRepository,
    ) -> None:
        self.event_type_repository = event_type_repository
        self.event_record_repository = event_record_repository

    def create_report(
        self,
        *,
        user_id: str,
        category: str,
        description: str | None,
        latitude: Decimal,
        longitude: Decimal,
        photo_url: str | None,
    ) -> tuple[EventRecord, str]:
        event_type = self.event_type_repository.get_smart_report_type_by_code(
            category
        )

        if event_type is None:
            raise InvalidReportCategoryError(
                "Categoria de incidencia no disponible"
            )

        event = EventRecord(
            user_id=user_id,
            event_type_id=event_type.id,
            description=description,
            latitude=latitude,
            longitude=longitude,
            photo_url=photo_url,
            status="REPORTED",
        )

        created_event = self.event_record_repository.create(event)

        return created_event, event_type.code
