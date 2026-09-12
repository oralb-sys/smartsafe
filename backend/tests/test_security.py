from app.shared.security import hash_password, verify_password


def test_hash_password_does_not_store_plain_text() -> None:
    password = "SmartSafeTest123!"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password.startswith("$argon2")


def test_verify_password_accepts_valid_password() -> None:
    password = "SmartSafeTest123!"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_invalid_password() -> None:
    hashed_password = hash_password("SmartSafeTest123!")

    assert verify_password("IncorrectPassword", hashed_password) is False


def test_hash_password_uses_unique_salts() -> None:
    password = "SmartSafeTest123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash) is True
    assert verify_password(password, second_hash) is True