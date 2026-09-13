from types import SimpleNamespace

import pytest

from app.services.report_query_service import (
    ReportNotFoundError,
    ReportQueryService,
)


class FakeRepository:
    def __init__(
        self,
        reports=None,
        report=None,
    ):
        self.reports = reports or []
        self.report = report
        self.list_user_id = None
        self.get_report_id = None
        self.get_user_id = None

    def list_by_user_id(
        self,
        user_id: str,
    ):
        self.list_user_id = user_id
        return self.reports

    def get_by_id_and_user_id(
        self,
        report_id: str,
        user_id: str,
    ):
        self.get_report_id = report_id
        self.get_user_id = user_id
        return self.report


def test_list_user_reports():
    reports = [
        SimpleNamespace(id="report-1"),
        SimpleNamespace(id="report-2"),
    ]

    repository = FakeRepository(
        reports=reports,
    )

    service = ReportQueryService(
        repository,
    )

    result = service.list_user_reports(
        "user-1",
    )

    assert result == reports
    assert repository.list_user_id == "user-1"


def test_get_user_report():
    report = SimpleNamespace(
        id="report-1",
        user_id="user-1",
    )

    repository = FakeRepository(
        report=report,
    )

    service = ReportQueryService(
        repository,
    )

    result = service.get_user_report(
        "report-1",
        "user-1",
    )

    assert result is report
    assert repository.get_report_id == "report-1"
    assert repository.get_user_id == "user-1"


def test_get_user_report_not_found():
    repository = FakeRepository(
        report=None,
    )

    service = ReportQueryService(
        repository,
    )

    with pytest.raises(
        ReportNotFoundError,
        match="El reporte solicitado no existe",
    ):
        service.get_user_report(
            "missing-report",
            "user-1",
        )