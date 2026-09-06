import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

import pytest


CONNECTION_FILE = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "database"
    / "connection.py"
)


def load_connection_module(monkeypatch, database_url):
    """Carga una copia aislada del módulo de conexión."""
    fake_engine = MagicMock()
    fake_sessionmaker = MagicMock()

    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setattr(
        "sqlalchemy.create_engine",
        lambda *args, **kwargs: fake_engine,
    )
    monkeypatch.setattr(
        "sqlalchemy.orm.sessionmaker",
        fake_sessionmaker,
    )

    spec = importlib.util.spec_from_file_location(
        "test_database_connection_isolated",
        CONNECTION_FILE,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module, fake_engine, fake_sessionmaker


def test_connection_creates_engine_and_session(monkeypatch):
    database_url = "mysql+pymysql://user:password@localhost:3306/test_db"

    module, fake_engine, fake_sessionmaker = load_connection_module(
        monkeypatch,
        database_url,
    )

    assert module.DATABASE_URL == database_url
    assert module.engine is fake_engine
    fake_sessionmaker.assert_called_once_with(
        autocommit=False,
        autoflush=False,
        bind=fake_engine,
    )


def test_connection_requires_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)

    spec = importlib.util.spec_from_file_location(
        "test_database_connection_missing_url",
        CONNECTION_FILE,
    )
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(
        RuntimeError,
        match="DATABASE_URL no esta configurada",
    ):
        spec.loader.exec_module(module)