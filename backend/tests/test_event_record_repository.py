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

def test_list_by_user_id():
    session = MagicMock()

    report_1 = SimpleNamespace(id="report-1")
    report_2 = SimpleNamespace(id="report-2")

    scalar_result = MagicMock()
    scalar_result.all.return_value = [
        report_1,
        report_2,
    ]

    session.scalars.return_value = scalar_result

    repository = EventRecordRepository(
        session,
    )

    result = repository.list_by_user_id(
        "user-1",
    )

    session.scalars.assert_called_once()

    assert result == [
        report_1,
        report_2,
    ]


def test_get_by_id_and_user_id():
    session = MagicMock()

    report = SimpleNamespace(
        id="report-1",
        user_id="user-1",
    )

    session.scalar.return_value = report

    repository = EventRecordRepository(
        session,
    )

    result = repository.get_by_id_and_user_id(
        "report-1",
        "user-1",
    )

    session.scalar.assert_called_once()
    assert result is report