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
)
from app.services.emergency_service import (
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