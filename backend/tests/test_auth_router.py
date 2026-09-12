from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_database_session
from app.routers.auth import router
from app.models.user import User


app = FastAPI()
app.include_router(router)


def override_database_session():
    session = MagicMock()
    try:
        yield session
    finally:
        pass


app.dependency_overrides[get_database_session] = override_database_session

client = TestClient(app)


def test_login_returns_access_token_for_valid_credentials() -> None:
    user = User(
        id="user-123",
        name="Ana",
        last_name="Perez",
        email="ana@smartsafe.demo",
        password_hash="hashed-password",
        role="CITIZEN",
    )

    with (
        patch(
            "app.routers.auth.AuthService.authenticate",
            return_value=user,
        ) as mock_authenticate,
        patch(
            "app.routers.auth.AuthService.create_token",
            return_value="test-access-token",
        ) as mock_create_token,
    ):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "ana@smartsafe.demo",
                "password": "SmartSafeTest123!",
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test-access-token",
        "token_type": "bearer",
        "role": "CITIZEN",
    }

    mock_authenticate.assert_called_once_with(
        email="ana@smartsafe.demo",
        password="SmartSafeTest123!",
    )
    mock_create_token.assert_called_once_with(user)


def test_login_rejects_invalid_credentials() -> None:
    from app.services.auth_service import InvalidCredentialsError

    with patch(
        "app.routers.auth.AuthService.authenticate",
        side_effect=InvalidCredentialsError("Credenciales invalidas"),
    ):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "ana@smartsafe.demo",
                "password": "IncorrectPassword",
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Credenciales invalidas"
    }


def test_login_rejects_invalid_email_format() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-email",
            "password": "SmartSafeTest123!",
        },
    )

    assert response.status_code == 422