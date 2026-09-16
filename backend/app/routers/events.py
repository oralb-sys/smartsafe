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
from app.schemas.event import (
    UrbanEventResponse,
)
from app.services.event_query_service import (
    EventQueryService,
)


router = APIRouter(
    prefix="/api/v1/events",
    tags=["UrbanEvents"],
)


@router.get(
    "",
    response_model=list[UrbanEventResponse],
    summary="Consultar eventos para mapa",
    description=(
        "Obtiene eventos de SmartReport y "
        "SmartSOS para su visualización "
        "unificada en el mapa."
    ),
)
def list_events(
    current_user: User = Depends(
        get_current_user
    ),
    session: Session = Depends(
        get_database_session
    ),
) -> list[UrbanEventResponse]:
    if current_user.role != "OPERATOR":
        raise HTTPException(
            status_code=(
                status.HTTP_403_FORBIDDEN
            ),
            detail=(
                "Solo un operador puede "
                "consultar el mapa de eventos."
            ),
        )

    service = EventQueryService(
        EventRecordRepository(
            session
        )
    )

    events = service.list_events()

    return [
        UrbanEventResponse(
            id=event.id,
            source=event_type.module,
            type=event_type.code,
            status=event.status,
            description=event.description,
            latitude=event.latitude,
            longitude=event.longitude,
            photo_url=event.photo_url,
            created_at=event.created_at,
        )
        for (
            event,
            event_type,
        ) in events
    ]