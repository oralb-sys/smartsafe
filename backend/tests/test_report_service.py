from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.models.event_record import EventRecord
from app.models.event_type import EventType
from app.services.report_service import (
    InvalidReportCategoryError,
    ReportService,
)


def test_create_report_sets_reported_status() -> None:
    event_type = EventType(
        id="type-123",
        code="POTHOLE",
        name="Bache",
        module="SMART_REPORT",
    )

    type_repository = MagicMock()
    type_repository.get_smart_report_type_by_code.return_value = event_type

    record_repository = MagicMock()
    record_repository.create.side_effect = lambda event: event

    service = ReportService(type_repository, record_repository)

    event, category = service.create_report(
        user_id="user-123",
        category="POTHOLE",
        description="Bache profundo",
        latitude=Decimal("-13.520400"),
        longitude=Decimal("-71.975100"),
        photo_url=None,
    )

    assert event.user_id == "user-123"
    assert event.event_type_id == "type-123"
    assert event.status == "REPORTED"
    assert category == "POTHOLE"
    record_repository.create.assert_called_once_with(event)


def test_create_report_rejects_unknown_event_type() -> None:
    type_repository = MagicMock()
    type_repository.get_smart_report_type_by_code.return_value = None

    record_repository = MagicMock()

    service = ReportService(type_repository, record_repository)

    with pytest.raises(
        InvalidReportCategoryError,
        match="Categoria de incidencia no disponible",
    ):
        service.create_report(
            user_id="user-123",
            category="POTHOLE",
            description=None,
            latitude=Decimal("-13.520400"),
            longitude=Decimal("-71.975100"),
            photo_url=None,
        )

    record_repository.create.assert_not_called()
