from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.services.emergency_service import (
    EmergencyService,
    EmergencyTypeNotFoundError,
)


def test_create_emergency_success():
    event_type = SimpleNamespace(
        id="type-sos",
        code="SOS",
    )

    created_emergency = SimpleNamespace(
        id="emergency-1",
        status="ACTIVE",
    )

    event_type_repository = MagicMock()
    event_type_repository.get_smart_sos_type_by_code.return_value = (
        event_type
    )

    event_record_repository = MagicMock()
    event_record_repository.create.return_value = created_emergency

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    result = service.create_emergency(
        "user-123",
    )

    event_type_repository.get_smart_sos_type_by_code.assert_called_once_with(
        "SOS"
    )

    event_record_repository.create.assert_called_once()

    created_argument = (
        event_record_repository.create.call_args.args[0]
    )

    assert created_argument.user_id == "user-123"
    assert created_argument.event_type_id == "type-sos"
    assert created_argument.status == "ACTIVE"
    assert created_argument.latitude is None
    assert created_argument.longitude is None
    assert created_argument.description is None
    assert created_argument.photo_url is None

    assert result is created_emergency


def test_create_emergency_type_not_found():
    event_type_repository = MagicMock()
    event_type_repository.get_smart_sos_type_by_code.return_value = None

    event_record_repository = MagicMock()

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    with pytest.raises(
        EmergencyTypeNotFoundError,
        match="El tipo inicial SOS no está configurado",
    ):
        service.create_emergency(
            "user-123",
        )

    event_record_repository.create.assert_not_called()