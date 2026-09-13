from app.models.event_record import EventRecord
from app.repositories.event_record_repository import (
    EventRecordRepository,
)


class ReportNotFoundError(Exception):
    pass


class ReportQueryService:
    def __init__(
        self,
        repository: EventRecordRepository,
    ) -> None:
        self.repository = repository

    def list_user_reports(
        self,
        user_id: str,
    ) -> list[EventRecord]:
        return self.repository.list_by_user_id(
            user_id,
        )

    def get_user_report(
        self,
        report_id: str,
        user_id: str,
    ) -> EventRecord:
        report = (
            self.repository.get_by_id_and_user_id(
                report_id,
                user_id,
            )
        )

        if report is None:
            raise ReportNotFoundError(
                "El reporte solicitado no existe."
            )

        return report