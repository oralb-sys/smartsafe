from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.services.report_status_service import (
    InvalidStatusTransitionError,
    ReportNotFoundError,
    ReportStatusService,
)


def test_update_status_from_reported_to_in_progress():
    report = SimpleNamespace(
        id="report-1",
        status="REPORTED",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = report
    repository.update_status.return_value = report

    service = ReportStatusService(repository)

    result = service.update_status(
        "report-1",
        "IN_PROGRESS",
    )

    repository.get_by_id.assert_called_once_with(
        "report-1"
    )

    repository.update_status.assert_called_once_with(
        report,
        "IN_PROGRESS",
    )

    assert result is report


def test_update_status_from_in_progress_to_resolved():
    report = SimpleNamespace(
        id="report-1",
        status="IN_PROGRESS",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = report
    repository.update_status.return_value = report

    service = ReportStatusService(repository)

    result = service.update_status(
        "report-1",
        "RESOLVED",
    )

    repository.update_status.assert_called_once_with(
        report,
        "RESOLVED",
    )

    assert result is report


def test_update_status_report_not_found():
    repository = MagicMock()
    repository.get_by_id.return_value = None

    service = ReportStatusService(repository)

    with pytest.raises(
        ReportNotFoundError,
        match="El reporte no existe",
    ):
        service.update_status(
            "missing-report",
            "IN_PROGRESS",
        )


def test_invalid_transition_reported_to_resolved():
    report = SimpleNamespace(
        id="report-1",
        status="REPORTED",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = report

    service = ReportStatusService(repository)

    with pytest.raises(
        InvalidStatusTransitionError,
        match="REPORTED -> RESOLVED",
    ):
        service.update_status(
            "report-1",
            "RESOLVED",
        )

    repository.update_status.assert_not_called()


def test_invalid_transition_resolved_to_in_progress():
    report = SimpleNamespace(
        id="report-1",
        status="RESOLVED",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = report

    service = ReportStatusService(repository)

    with pytest.raises(
        InvalidStatusTransitionError,
        match="RESOLVED -> IN_PROGRESS",
    ):
        service.update_status(
            "report-1",
            "IN_PROGRESS",
        )

    repository.update_status.assert_not_called()