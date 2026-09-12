from unittest.mock import MagicMock

from app.models.user import User
from app.repositories.user_repository import UserRepository


def test_get_by_email_returns_existing_user() -> None:
    session = MagicMock()
    expected_user = User(
        name="Ana",
        last_name="Perez",
        email="ana@smartsafe.demo",
        password_hash="hashed-password",
        role="CITIZEN",
    )
    session.scalar.return_value = expected_user

    repository = UserRepository(session)
    result = repository.get_by_email("ana@smartsafe.demo")

    assert result is expected_user
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]
    assert statement.compile().params == {
        "email_1": "ana@smartsafe.demo"
    }


def test_get_by_email_returns_none_when_user_does_not_exist() -> None:
    session = MagicMock()
    session.scalar.return_value = None

    repository = UserRepository(session)
    result = repository.get_by_email("missing@smartsafe.demo")

    assert result is None
    session.scalar.assert_called_once()