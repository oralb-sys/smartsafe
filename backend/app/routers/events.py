from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
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
    summary="Consultar UrbanEvents",
    description=(
        "Obtiene eventos SmartReport y SmartSOS. "
        "Permite filtrar por source, type y status."
    ),
)
def list_events(
    source: str | None = Query(
        default=None,
        description=(
            "Origen del evento: "
            "SMART_REPORT o SMART_SOS."
        ),
    ),
    event_type: str | None = Query(
        default=None,
        alias="type",
        description=(
            "Tipo de evento, por ejemplo "
            "POTHOLE, WASTE o SOS."
        ),
    ),
    event_status: str | None = Query(
        default=None,
        alias="status",
        description=(
            "Estado del evento."
        ),
    ),
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
                "consultar los eventos."
            ),
        )

    service = EventQueryService(
        EventRecordRepository(
            session
        )
    )

    events = service.list_events(
        source=source,
        event_type=event_type,
        status=event_status,
    )

    return [
        UrbanEventResponse(
            id=event.id,
            source=event_type_record.module,
            type=event_type_record.code,
            status=event.status,
            description=event.description,
            latitude=event.latitude,
            longitude=event.longitude,
            photo_url=event.photo_url,
            created_at=event.created_at,
        )
        for (
            event,
            event_type_record,
        ) in events
    ]