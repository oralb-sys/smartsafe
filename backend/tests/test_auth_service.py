from unittest.mock import MagicMock, patch

import pytest

from app.models.user import User
from app.services.auth_service import AuthService, InvalidCredentialsError
from app.shared.security import hash_password


def create_test_user(role: str = "CITIZEN") -> User:
    return User(
        id="user-123",
        name="Ana",
        last_name="Perez",
        email="ana@smartsafe.demo",
        password_hash=hash_password("SmartSafeTest123!"),
        role=role,
    )


def test_authenticate_accepts_valid_credentials() -> None:
    repository = MagicMock()
    user = create_test_user()
    repository.get_by_email.return_value = user

    service = AuthService(repository)
    result = service.authenticate(
        "ana@smartsafe.demo",
        "SmartSafeTest123!",
    )

    assert result is user
    repository.get_by_email.assert_called_once_with("ana@smartsafe.demo")


def test_authenticate_rejects_unknown_email() -> None:
    repository = MagicMock()
    repository.get_by_email.return_value = None

    service = AuthService(repository)

    with pytest.raises(
        InvalidCredentialsError,
        match="Credenciales invalidas",
    ):
        service.authenticate(
            "missing@smartsafe.demo",
            "SmartSafeTest123!",
        )


def test_authenticate_rejects_invalid_password() -> None:
    repository = MagicMock()
    repository.get_by_email.return_value = create_test_user()

    service = AuthService(repository)

    with pytest.raises(
        InvalidCredentialsError,
        match="Credenciales invalidas",
    ):
        service.authenticate(
            "ana@smartsafe.demo",
            "IncorrectPassword",
        )


@pytest.mark.parametrize("role", ["CITIZEN", "OPERATOR"])
def test_create_token_includes_user_id_and_role(role: str) -> None:
    repository = MagicMock()
    user = create_test_user(role=role)
    service = AuthService(repository)

    with patch(
        "app.services.auth_service.create_access_token",
        return_value="test-access-token",
    ) as mock_create_token:
        token = service.create_token(user)

    assert token == "test-access-token"
    mock_create_token.assert_called_once_with(
        user_id="user-123",
        role=role,
    )