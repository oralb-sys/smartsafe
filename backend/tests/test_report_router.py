from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_current_user, get_database_session
from app.models.event_record import EventRecord
from app.models.user import User
from app.routers.reports import router


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


app.dependency_overrides[get_database_session] = override_database_session
app.dependency_overrides[get_current_user] = override_current_user

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
        return_value=(created_event, "POTHOLE"),
    ):
        response = client.post(
            "/api/v1/reports",
            json={
                "category": "POTHOLE",
                "description": "Bache en avenida principal",
                "latitude": -13.5204,
                "longitude": -71.9751,
                "photo_url": None,
            },
        )

    assert response.status_code == 201
    assert response.json()["category"] == "POTHOLE"
    assert response.json()["status"] == "REPORTED"
    assert response.json()["id"] == "event-123"


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
