from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies import get_current_user
from app.models.user import User


def test_get_current_user_returns_authenticated_user() -> None:
    session = MagicMock()

    user = User(
        id="user-123",
        name="Ana",
        last_name="Perez",
        email="ana@smartsafe.demo",
        password_hash="hash",
        role="CITIZEN",
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="valid-token",
    )

    with (
        patch(
            "app.dependencies.decode_access_token",
            return_value={"sub": "user-123"},
        ),
        patch(
            "app.dependencies.UserRepository.get_by_id",
            return_value=user,
        ),
    ):
        result = get_current_user(credentials, session)

    assert result is user


def test_get_current_user_requires_token() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(None, MagicMock())

    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_invalid_token() -> None:
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    with patch(
        "app.dependencies.decode_access_token",
        side_effect=ValueError("Token de acceso invalido"),
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, MagicMock())

    assert exc_info.value.status_code == 401
