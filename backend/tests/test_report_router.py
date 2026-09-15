from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import (
    get_current_user,
    get_database_session,
)
from app.models.event_record import EventRecord
from app.models.user import User
from app.routers.reports import router
from app.services.report_status_service import (
    InvalidStatusTransitionError,
    ReportNotFoundError,
)


app = FastAPI()
app.include_router(router)


def override_database_session():
    yield MagicMock()


def override_current_user():
    return User(
        id="user-123",
        name="Ana",
        last_name="Perez",
        email="ana@smartsafe.demo",
        password_hash="hash",
        role="CITIZEN",
    )


def override_operator_user():
    return User(
        id="operator-123",
        name="Carlos",
        last_name="Operador",
        email="operator@smartsafe.demo",
        password_hash="hash",
        role="OPERATOR",
    )


app.dependency_overrides[
    get_database_session
] = override_database_session

app.dependency_overrides[
    get_current_user
] = override_current_user

client = TestClient(app)


def test_create_report_returns_201() -> None:
    created_event = EventRecord(
        id="event-123",
        user_id="user-123",
        event_type_id="type-123",
        description="Bache en avenida principal",
        latitude=Decimal("-13.520400"),
        longitude=Decimal("-71.975100"),
        photo_url=None,
        status="REPORTED",
        created_at=datetime.now(timezone.utc),
    )

    with patch(
        "app.routers.reports.ReportService.create_report",
        return_value=(
            created_event,
            "POTHOLE",
        ),
    ):
        response = client.post(
            "/api/v1/reports",
            json={
                "category": "POTHOLE",
                "description": (
                    "Bache en avenida principal"
                ),
                "latitude": -13.5204,
                "longitude": -71.9751,
                "photo_url": None,
            },
        )

    assert response.status_code == 201
    assert (
        response.json()["category"]
        == "POTHOLE"
    )
    assert (
        response.json()["status"]
        == "REPORTED"
    )
    assert (
        response.json()["id"]
        == "event-123"
    )


def test_create_report_rejects_invalid_category() -> None:
    response = client.post(
        "/api/v1/reports",
        json={
            "category": "INVALID_CATEGORY",
            "latitude": -13.5204,
            "longitude": -71.9751,
        },
    )

    assert response.status_code == 422


def test_create_report_rejects_invalid_latitude() -> None:
    response = client.post(
        "/api/v1/reports",
        json={
            "category": "WASTE",
            "latitude": 100,
            "longitude": -71.9751,
        },
    )

    assert response.status_code == 422


def test_update_report_status_forbidden_for_citizen() -> None:
    response = client.put(
        "/api/v1/reports/report-1",
        json={
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Solo un operador puede modificar "
        "el estado de los reportes."
    )


def test_update_report_status_success() -> None:
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    updated_report = SimpleNamespace(
        id="report-1",
        status="IN_PROGRESS",
    )

    try:
        with patch(
            "app.routers.reports."
            "ReportStatusService.update_status",
            return_value=updated_report,
        ):
            response = client.put(
                "/api/v1/reports/report-1",
                json={
                    "status": "IN_PROGRESS",
                },
            )

        assert response.status_code == 200
        assert response.json() == {
            "id": "report-1",
            "status": "IN_PROGRESS",
        }

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_current_user


def test_update_report_status_not_found() -> None:
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        with patch(
            "app.routers.reports."
            "ReportStatusService.update_status",
            side_effect=ReportNotFoundError(
                "El reporte no existe."
            ),
        ):
            response = client.put(
                "/api/v1/reports/missing-report",
                json={
                    "status": "IN_PROGRESS",
                },
            )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "El reporte no existe."
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_current_user


def test_update_report_status_invalid_transition() -> None:
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        with patch(
            "app.routers.reports."
            "ReportStatusService.update_status",
            side_effect=(
                InvalidStatusTransitionError(
                    "Transición de estado no permitida: "
                    "REPORTED -> RESOLVED."
                )
            ),
        ):
            response = client.put(
                "/api/v1/reports/report-1",
                json={
                    "status": "RESOLVED",
                },
            )

        assert response.status_code == 409
        assert (
            "REPORTED -> RESOLVED"
            in response.json()["detail"]
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_current_user


def test_update_report_status_rejects_invalid_status() -> None:
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        response = client.put(
            "/api/v1/reports/report-1",
            json={
                "status": "INVALID_STATUS",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_current_user