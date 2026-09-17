from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.event_query_service import (
    EventQueryService,
)


def test_list_events_without_filters():
    event_record = SimpleNamespace(
        id="event-1",
    )

    event_type = SimpleNamespace(
        code="POTHOLE",
        module="SMART_REPORT",
    )

    events = [
        (
            event_record,
            event_type,
        )
    ]

    repository = MagicMock()

    repository.list_urban_events.return_value = (
        events
    )

    service = EventQueryService(
        repository
    )

    result = service.list_events()

    repository.list_urban_events.assert_called_once_with(
        source=None,
        event_type=None,
        status=None,
    )

    assert result == events


def test_list_events_with_filters():
    event_record = SimpleNamespace(
        id="event-1",
    )

    event_type = SimpleNamespace(
        code="POTHOLE",
        module="SMART_REPORT",
    )

    events = [
        (
            event_record,
            event_type,
        )
    ]

    repository = MagicMock()

    repository.list_urban_events.return_value = (
        events
    )

    service = EventQueryService(
        repository
    )

    result = service.list_events(
        source="SMART_REPORT",
        event_type="POTHOLE",
        status="REPORTED",
    )

    repository.list_urban_events.assert_called_once_with(
        source="SMART_REPORT",
        event_type="POTHOLE",
        status="REPORTED",
    )

    assert result == events