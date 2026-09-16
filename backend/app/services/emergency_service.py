from decimal import Decimal

from app.models.event_record import EventRecord
from app.repositories.event_record_repository import (
    EventRecordRepository,
)
from app.repositories.event_type_repository import (
    EventTypeRepository,
)


class EmergencyTypeNotFoundError(Exception):
    pass


class EmergencyNotFoundError(Exception):
    pass


class EmergencyNotActiveError(Exception):
    pass


class InvalidEmergencyStatusTransitionError(
    Exception
):
    pass


class EmergencyService:
    VALID_STATUS_TRANSITIONS = {
        "ACTIVE": "IN_PROGRESS",
        "IN_PROGRESS": "FINISHED",
    }

    def __init__(
        self,
        event_type_repository: EventTypeRepository,
        event_record_repository: EventRecordRepository,
    ) -> None:
        self.event_type_repository = (
            event_type_repository
        )

        self.event_record_repository = (
            event_record_repository
        )

    def create_emergency(
        self,
        user_id: str,
    ) -> EventRecord:
        event_type = (
            self.event_type_repository
            .get_smart_sos_type_by_code(
                "SOS"
            )
        )

        if event_type is None:
            raise EmergencyTypeNotFoundError(
                "El tipo inicial SOS no está configurado."
            )

        emergency = EventRecord(
            user_id=user_id,
            event_type_id=event_type.id,
            description=None,
            latitude=None,
            longitude=None,
            photo_url=None,
            status="ACTIVE",
        )

        return (
            self.event_record_repository
            .create(
                emergency
            )
        )

    def update_location(
        self,
        emergency_id: str,
        user_id: str,
        latitude: Decimal,
        longitude: Decimal,
    ) -> EventRecord:
        emergency = (
            self.event_record_repository
            .get_by_id_and_user_id(
                emergency_id,
                user_id,
            )
        )

        if emergency is None:
            raise EmergencyNotFoundError(
                "La emergencia no existe "
                "o no pertenece al usuario."
            )

        if emergency.status != "ACTIVE":
            raise EmergencyNotActiveError(
                "Solo se puede registrar "
                "la ubicación de una "
                "emergencia activa."
            )

        return (
            self.event_record_repository
            .update_location(
                emergency,
                latitude,
                longitude,
            )
        )

    def list_emergencies(
        self,
    ) -> list[EventRecord]:
        return (
            self.event_record_repository
            .list_smart_sos_emergencies()
        )

    def get_emergency(
        self,
        emergency_id: str,
    ) -> EventRecord:
        emergency = (
            self.event_record_repository
            .get_smart_sos_emergency_by_id(
                emergency_id
            )
        )

        if emergency is None:
            raise EmergencyNotFoundError(
                "La emergencia no existe."
            )

        return emergency

    def update_status(
        self,
        emergency_id: str,
        new_status: str,
    ) -> EventRecord:
        emergency = (
            self.event_record_repository
            .get_smart_sos_emergency_by_id(
                emergency_id
            )
        )

        if emergency is None:
            raise EmergencyNotFoundError(
                "La emergencia no existe."
            )

        expected_status = (
            self.VALID_STATUS_TRANSITIONS
            .get(
                emergency.status
            )
        )

        if expected_status != new_status:
            raise (
                InvalidEmergencyStatusTransitionError(
                    "Transición de estado "
                    "no permitida: "
                    f"{emergency.status} "
                    f"-> {new_status}."
                )
            )

        return (
            self.event_record_repository
            .update_status(
                emergency,
                new_status,
            )
        )