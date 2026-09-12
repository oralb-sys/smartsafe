from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.shared.jwt_service import create_access_token, decode_access_token


TEST_JWT_SECRET_KEY = "test-secret-key-for-jwt-32-bytes-minimum"


@pytest.fixture
def jwt_test_config(monkeypatch) -> None:
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_JWT_SECRET_KEY)
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")


def test_create_access_token_contains_user_id_and_role(
    jwt_test_config,
) -> None:
    token = create_access_token("user-123", "CITIZEN")

    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert payload["role"] == "CITIZEN"
    assert "exp" in payload


def test_create_access_token_has_configured_expiration(
    jwt_test_config,
) -> None:
    before = datetime.now(timezone.utc)
    token = create_access_token("user-123", "OPERATOR")
    after = datetime.now(timezone.utc)

    payload = decode_access_token(token)
    expires_at = datetime.fromtimestamp(payload["exp"], timezone.utc)

    assert before + timedelta(minutes=30, seconds=-1) <= expires_at
    assert expires_at <= after + timedelta(minutes=30)


def test_decode_access_token_rejects_invalid_token(
    jwt_test_config,
) -> None:
    with pytest.raises(ValueError, match="Token de acceso invalido"):
        decode_access_token("invalid.token.value")


def test_decode_access_token_rejects_expired_token(
    jwt_test_config,
) -> None:
    expired_token = jwt.encode(
        {
            "sub": "user-123",
            "role": "CITIZEN",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        TEST_JWT_SECRET_KEY,
        algorithm="HS256",
    )

    with pytest.raises(ValueError, match="Token de acceso invalido"):
        decode_access_token(expired_token)


def test_decode_access_token_rejects_modified_signature(
    jwt_test_config,
) -> None:
    token = create_access_token("user-123", "CITIZEN")
    modified_token = token + "invalid"

    with pytest.raises(ValueError, match="Token de acceso invalido"):
        decode_access_token(modified_token)