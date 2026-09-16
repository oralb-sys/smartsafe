from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.services.emergency_service import (
    EmergencyNotActiveError,
    EmergencyNotFoundError,
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
    event_record_repository.create.return_value = (
        created_emergency
    )

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
    event_type_repository.get_smart_sos_type_by_code.return_value = (
        None
    )

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


def test_update_location_success():
    emergency = SimpleNamespace(
        id="emergency-1",
        user_id="user-123",
        status="ACTIVE",
        latitude=None,
        longitude=None,
    )

    updated_emergency = SimpleNamespace(
        id="emergency-1",
        user_id="user-123",
        status="ACTIVE",
        latitude=Decimal("-13.5204"),
        longitude=Decimal("-71.9751"),
    )

    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.get_by_id_and_user_id.return_value = (
        emergency
    )

    event_record_repository.update_location.return_value = (
        updated_emergency
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    result = service.update_location(
        emergency_id="emergency-1",
        user_id="user-123",
        latitude=Decimal("-13.5204"),
        longitude=Decimal("-71.9751"),
    )

    event_record_repository.get_by_id_and_user_id.assert_called_once_with(
        "emergency-1",
        "user-123",
    )

    event_record_repository.update_location.assert_called_once_with(
        emergency,
        Decimal("-13.5204"),
        Decimal("-71.9751"),
    )

    assert result is updated_emergency


def test_update_location_emergency_not_found():
    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.get_by_id_and_user_id.return_value = (
        None
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    with pytest.raises(
        EmergencyNotFoundError,
        match="La emergencia no existe",
    ):
        service.update_location(
            emergency_id="missing-emergency",
            user_id="user-123",
            latitude=Decimal("-13.5204"),
            longitude=Decimal("-71.9751"),
        )

    event_record_repository.update_location.assert_not_called()


def test_update_location_emergency_not_active():
    emergency = SimpleNamespace(
        id="emergency-1",
        user_id="user-123",
        status="FINISHED",
    )

    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.get_by_id_and_user_id.return_value = (
        emergency
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    with pytest.raises(
        EmergencyNotActiveError,
        match="Solo se puede registrar la ubicación",
    ):
        service.update_location(
            emergency_id="emergency-1",
            user_id="user-123",
            latitude=Decimal("-13.5204"),
            longitude=Decimal("-71.9751"),
        )

    event_record_repository.update_location.assert_not_called()


def test_list_emergencies():
    emergency_1 = SimpleNamespace(
        id="emergency-1",
    )

    emergency_2 = SimpleNamespace(
        id="emergency-2",
    )

    emergencies = [
        emergency_1,
        emergency_2,
    ]

    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.list_smart_sos_emergencies.return_value = (
        emergencies
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    result = service.list_emergencies()

    event_record_repository.list_smart_sos_emergencies.assert_called_once()

    assert result == emergencies


def test_get_emergency_success():
    emergency = SimpleNamespace(
        id="emergency-1",
        status="ACTIVE",
    )

    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.get_smart_sos_emergency_by_id.return_value = (
        emergency
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    result = service.get_emergency(
        "emergency-1"
    )

    event_record_repository.get_smart_sos_emergency_by_id.assert_called_once_with(
        "emergency-1"
    )

    assert result is emergency


def test_get_emergency_not_found():
    event_type_repository = MagicMock()
    event_record_repository = MagicMock()

    event_record_repository.get_smart_sos_emergency_by_id.return_value = (
        None
    )

    service = EmergencyService(
        event_type_repository,
        event_record_repository,
    )

    with pytest.raises(
        EmergencyNotFoundError,
        match="La emergencia no existe",
    ):
        service.get_emergency(
            "missing-emergency"
        )