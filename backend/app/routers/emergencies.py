from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.dependencies import (
    get_current_user,
    get_database_session,
)
from app.models.user import User
from app.repositories.event_record_repository import (
    EventRecordRepository,
)
from app.repositories.event_type_repository import (
    EventTypeRepository,
)
from app.schemas.emergency import (
    EmergencyCreateResponse,
    EmergencyLocationRequest,
    EmergencyLocationResponse,
)
from app.services.emergency_service import (
    EmergencyNotActiveError,
    EmergencyNotFoundError,
    EmergencyService,
    EmergencyTypeNotFoundError,
)


router = APIRouter(
    prefix="/api/v1/emergencies",
    tags=["SmartSOS"],
)


@router.post(
    "",
    response_model=EmergencyCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Activar botón SOS",
    description=(
        "Inicia una alerta de emergencia para "
        "el ciudadano autenticado con estado ACTIVE."
    ),
)
def create_emergency(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> EmergencyCreateResponse:
    if current_user.role != "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Solo un ciudadano puede "
                "activar una alerta SOS."
            ),
        )

    service = EmergencyService(
        EventTypeRepository(session),
        EventRecordRepository(session),
    )

    try:
        emergency = service.create_emergency(
            current_user.id
        )
    except EmergencyTypeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return EmergencyCreateResponse(
        id=emergency.id,
        status=emergency.status,
        created_at=emergency.created_at,
    )


@router.put(
    "/{emergency_id}/location",
    response_model=EmergencyLocationResponse,
    summary="Registrar ubicación SOS",
    description=(
        "Registra latitud y longitud para una "
        "emergencia ACTIVE del ciudadano autenticado."
    ),
    responses={
        401: {
            "description": "Usuario no autenticado.",
        },
        403: {
            "description": (
                "Solo un ciudadano puede registrar "
                "la ubicación de una alerta SOS."
            ),
        },
        404: {
            "description": (
                "La emergencia no existe o no pertenece "
                "al usuario autenticado."
            ),
        },
        409: {
            "description": (
                "La emergencia ya no se encuentra ACTIVE."
            ),
        },
        422: {
            "description": "Coordenadas inválidas.",
        },
    },
)
def update_emergency_location(
    emergency_id: str,
    payload: EmergencyLocationRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> EmergencyLocationResponse:
    if current_user.role != "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Solo un ciudadano puede registrar "
                "la ubicación de una alerta SOS."
            ),
        )

    service = EmergencyService(
        EventTypeRepository(session),
        EventRecordRepository(session),
    )

    try:
        emergency = service.update_location(
            emergency_id=emergency_id,
            user_id=current_user.id,
            latitude=payload.latitude,
            longitude=payload.longitude,
        )

    except EmergencyNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except EmergencyNotActiveError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return EmergencyLocationResponse(
        id=emergency.id,
        latitude=emergency.latitude,
        longitude=emergency.longitude,
        status=emergency.status,
    )