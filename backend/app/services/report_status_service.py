from app.models.event_record import EventRecord
from app.repositories.event_record_repository import (
    EventRecordRepository,
)


class ReportNotFoundError(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    pass


class ReportStatusService:
    VALID_TRANSITIONS = {
        "REPORTED": "IN_PROGRESS",
        "IN_PROGRESS": "RESOLVED",
    }

    def __init__(
        self,
        repository: EventRecordRepository,
    ) -> None:
        self.repository = repository

    def update_status(
        self,
        report_id: str,
        new_status: str,
    ) -> EventRecord:
        report = self.repository.get_by_id(
            report_id,
        )

        if report is None:
            raise ReportNotFoundError(
                "El reporte no existe."
            )

        expected_status = (
            self.VALID_TRANSITIONS.get(
                report.status
            )
        )

        if expected_status != new_status:
            raise InvalidStatusTransitionError(
                (
                    "Transición de estado no permitida: "
                    f"{report.status} -> {new_status}."
                )
            )

        return self.repository.update_status(
            report,
            new_status,
        )