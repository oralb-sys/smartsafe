import pytest

from app.shared.auth_config import (
    get_jwt_access_token_expire_minutes,
    get_jwt_algorithm,
    get_jwt_secret_key,
)


def test_get_jwt_secret_key_returns_configured_value(monkeypatch) -> None:
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key")

    assert get_jwt_secret_key() == "test-secret-key"


def test_get_jwt_secret_key_requires_configuration(monkeypatch) -> None:
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(
        RuntimeError,
        match="JWT_SECRET_KEY no esta configurada",
    ):
        get_jwt_secret_key()


def test_get_jwt_algorithm_returns_configured_value(monkeypatch) -> None:
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")

    assert get_jwt_algorithm() == "HS256"


def test_get_jwt_algorithm_uses_default(monkeypatch) -> None:
    monkeypatch.delenv("JWT_ALGORITHM", raising=False)

    assert get_jwt_algorithm() == "HS256"


def test_get_jwt_expiration_returns_configured_value(monkeypatch) -> None:
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "45")

    assert get_jwt_access_token_expire_minutes() == 45


def test_get_jwt_expiration_uses_default(monkeypatch) -> None:
    monkeypatch.delenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", raising=False)

    assert get_jwt_access_token_expire_minutes() == 30


def test_get_jwt_expiration_rejects_zero(monkeypatch) -> None:
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "0")

    with pytest.raises(
        ValueError,
        match="JWT_ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que cero",
    ):
        get_jwt_access_token_expire_minutes()


def test_get_jwt_expiration_rejects_negative_values(monkeypatch) -> None:
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "-5")

    with pytest.raises(ValueError):
        get_jwt_access_token_expire_minutes()


def test_get_jwt_expiration_rejects_non_numeric_values(monkeypatch) -> None:
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "invalid")

    with pytest.raises(ValueError):
        get_jwt_access_token_expire_minutes()