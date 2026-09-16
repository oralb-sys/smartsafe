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
from app.routers.emergencies import router
from app.services.emergency_service import (
    EmergencyNotActiveError,
    EmergencyNotFoundError,
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
        created_at=datetime.now(
            timezone.utc
        ),
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
    assert (
        response.json()["id"]
        == "emergency-1"
    )
    assert (
        response.json()["status"]
        == "ACTIVE"
    )


def test_create_emergency_forbidden_for_operator():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        response = client.post(
            "/api/v1/emergencies"
        )

        assert response.status_code == 403

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


def test_update_emergency_location_returns_200():
    emergency = SimpleNamespace(
        id="emergency-1",
        status="ACTIVE",
        latitude=Decimal("-13.5204"),
        longitude=Decimal("-71.9751"),
    )

    with patch(
        "app.routers.emergencies."
        "EmergencyService.update_location",
        return_value=emergency,
    ):
        response = client.put(
            "/api/v1/emergencies/"
            "emergency-1/location",
            json={
                "latitude": -13.5204,
                "longitude": -71.9751,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "emergency-1"
    assert data["status"] == "ACTIVE"

    assert str(
        data["latitude"]
    ) == "-13.5204"

    assert str(
        data["longitude"]
    ) == "-71.9751"


def test_update_emergency_location_forbidden_for_operator():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        response = client.put(
            "/api/v1/emergencies/"
            "emergency-1/location",
            json={
                "latitude": -13.5204,
                "longitude": -71.9751,
            },
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_citizen_user


def test_update_emergency_location_returns_404():
    with patch(
        "app.routers.emergencies."
        "EmergencyService.update_location",
        side_effect=EmergencyNotFoundError(
            "La emergencia no existe."
        ),
    ):
        response = client.put(
            "/api/v1/emergencies/"
            "missing/location",
            json={
                "latitude": -13.5204,
                "longitude": -71.9751,
            },
        )

    assert response.status_code == 404


def test_update_emergency_location_returns_409():
    with patch(
        "app.routers.emergencies."
        "EmergencyService.update_location",
        side_effect=EmergencyNotActiveError(
            "La emergencia no está activa."
        ),
    ):
        response = client.put(
            "/api/v1/emergencies/"
            "emergency-1/location",
            json={
                "latitude": -13.5204,
                "longitude": -71.9751,
            },
        )

    assert response.status_code == 409


def test_update_emergency_location_invalid_coordinates_returns_422():
    response = client.put(
        "/api/v1/emergencies/"
        "emergency-1/location",
        json={
            "latitude": 100,
            "longitude": -71.9751,
        },
    )

    assert response.status_code == 422


def test_list_emergencies_returns_200_for_operator():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    emergencies = [
        SimpleNamespace(
            id="emergency-1",
            status="ACTIVE",
            latitude=Decimal(
                "-13.5204"
            ),
            longitude=Decimal(
                "-71.9751"
            ),
            created_at=datetime.now(
                timezone.utc
            ),
        ),
        SimpleNamespace(
            id="emergency-2",
            status="ACTIVE",
            latitude=None,
            longitude=None,
            created_at=datetime.now(
                timezone.utc
            ),
        ),
    ]

    try:
        with patch(
            "app.routers.emergencies."
            "EmergencyService.list_emergencies",
            return_value=emergencies,
        ):
            response = client.get(
                "/api/v1/emergencies"
            )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2

        assert (
            data[0]["id"]
            == "emergency-1"
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_citizen_user


def test_list_emergencies_forbidden_for_citizen():
    response = client.get(
        "/api/v1/emergencies"
    )

    assert response.status_code == 403


def test_get_emergency_detail_returns_200_for_operator():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    emergency = SimpleNamespace(
        id="emergency-1",
        user_id="user-123",
        status="ACTIVE",
        latitude=Decimal(
            "-13.5204"
        ),
        longitude=Decimal(
            "-71.9751"
        ),
        created_at=datetime.now(
            timezone.utc
        ),
    )

    try:
        with patch(
            "app.routers.emergencies."
            "EmergencyService.get_emergency",
            return_value=emergency,
        ):
            response = client.get(
                "/api/v1/emergencies/"
                "emergency-1"
            )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["id"]
            == "emergency-1"
        )

        assert (
            data["user_id"]
            == "user-123"
        )

        assert (
            data["status"]
            == "ACTIVE"
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_citizen_user


def test_get_emergency_detail_returns_404():
    app.dependency_overrides[
        get_current_user
    ] = override_operator_user

    try:
        with patch(
            "app.routers.emergencies."
            "EmergencyService.get_emergency",
            side_effect=EmergencyNotFoundError(
                "La emergencia no existe."
            ),
        ):
            response = client.get(
                "/api/v1/emergencies/"
                "missing"
            )

        assert response.status_code == 404

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_citizen_user


def test_get_emergency_detail_forbidden_for_citizen():
    response = client.get(
        "/api/v1/emergencies/"
        "emergency-1"
    )

    assert response.status_code == 403