import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginRequest, LoginResponse


def test_login_request_accepts_valid_data() -> None:
    request = LoginRequest(
        email="ana@smartsafe.demo",
        password="SmartSafeTest123!",
    )

    assert str(request.email) == "ana@smartsafe.demo"
    assert request.password == "SmartSafeTest123!"


def test_login_request_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(
            email="invalid-email",
            password="SmartSafeTest123!",
        )


def test_login_response_uses_bearer_as_default_token_type() -> None:
    response = LoginResponse(
        access_token="test-token",
        role="CITIZEN",
    )

    assert response.access_token == "test-token"
    assert response.token_type == "bearer"
    assert response.role == "CITIZEN"


def test_login_response_accepts_operator_role() -> None:
    response = LoginResponse(
        access_token="test-token",
        role="OPERATOR",
    )

    assert response.role == "OPERATOR"