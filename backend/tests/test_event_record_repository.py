from types import SimpleNamespace
from unittest.mock import MagicMock

from app.repositories.event_record_repository import (
    EventRecordRepository,
)


def test_create_event_record():
    session = MagicMock()

    repository = EventRecordRepository(session)

    event = SimpleNamespace(
        id="report-1",
        photo_url=None,
    )

    result = repository.create(event)

    session.add.assert_called_once_with(event)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(event)

    assert result is event


def test_update_photo_url():
    session = MagicMock()

    repository = EventRecordRepository(session)

    event = SimpleNamespace(
        id="report-1",
        photo_url=None,
    )

    photo_url = (
        "/uploads/reports/test-photo.jpg"
    )

    result = repository.update_photo_url(
        event,
        photo_url,
    )

    assert event.photo_url == photo_url

    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(event)

    assert result is event