from sqlalchemy.orm import configure_mappers

from app.database.base import Base
from app.models import EventRecord, EventType, User


def test_models_are_registered() -> None:
    assert set(Base.metadata.tables.keys()) == {
        "users",
        "event_types",
        "event_records",
    }


def test_model_relationships_are_configured() -> None:
    configure_mappers()

    assert User.events.property.mapper.class_ is EventRecord
    assert EventType.events.property.mapper.class_ is EventRecord
    assert EventRecord.user.property.mapper.class_ is User
    assert EventRecord.event_type.property.mapper.class_ is EventType