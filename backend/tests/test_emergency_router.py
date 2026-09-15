from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import (
    get_current_user,
    get_database_session,
)
from app.routers.emergencies import router
from app.services.emergency_service import (
    EmergencyTypeNotFoundError,
)


app = FastAPI()
app.include_router(router)


def override_database_session():
    yield MagicMock()


def override_citizen_user():
    return SimpleNamespace(
        id="user-123",
        role="CITIZEN",
    )


def override_operator_user():
    return SimpleNamespace(
        id="operator-123",
        role="OPERATOR",
    )


app.dependency_overrides[
    get_database_session
] = override_database_session

app.dependency_overrides[
    get_current_user
] = override_citizen_user

client = TestClient(app)


def test_create_emergency_returns_201():
    emergency = SimpleNamespace(
        id="emergency-1",
        status="ACTIVE",
        created_at=datetime.now(timezone.utc),
    )

    with patch(
        "app.routers.emergencies."
        "EmergencyService.create_emergency",
        return_value=emergency,
    ):
        response = client.post(
            "/api/v1/emergencies"
        )

    assert response.status_code == 201
    assert response.json()["id"] == "emergency-1"
    assert response.json()["status"] == "ACTIVE"


def test_create_emergency_forbidden_for_operator():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        response = client.post(
            "/api/v1/emergencies"
        )

        assert response.status_code == 403
        assert response.json()["detail"] == (
            "Solo un ciudadano puede activar "
            "una alerta SOS."
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_citizen_user


def test_create_emergency_returns_500_if_sos_type_missing():
    with patch(
        "app.routers.emergencies."
        "EmergencyService.create_emergency",
        side_effect=EmergencyTypeNotFoundError(
            "El tipo inicial SOS no está configurado."
        ),
    ):
        response = client.post(
            "/api/v1/emergencies"
        )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "El tipo inicial SOS no está configurado."
    )