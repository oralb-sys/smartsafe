from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
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
from app.schemas.report import (
    ReportCreateRequest,
    ReportCreateResponse,
    ReportDetailResponse,
    ReportListItemResponse,
)
from app.services.report_photo_service import (
    ImageTooLargeError,
    InvalidImageTypeError,
    ReportNotFoundError as PhotoReportNotFoundError,
    ReportOwnershipError,
    ReportPhotoService,
)
from app.services.report_query_service import (
    ReportNotFoundError as QueryReportNotFoundError,
    ReportQueryService,
)
from app.services.report_service import (
    InvalidReportCategoryError,
    ReportService,
)

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["SmartReport"],
)


@router.post(
    "",
    response_model=ReportCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar incidencia urbana",
    description=(
        "Registra una incidencia urbana no urgente asociada "
        "al usuario autenticado. El estado inicial es REPORTED."
    ),
    responses={
        401: {
            "description": "Usuario no autenticado.",
        },
        422: {
            "description": "Datos de entrada inválidos.",
        },
    },
)
def create_report(
    report: ReportCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> ReportCreateResponse:
    service = ReportService(
        EventTypeRepository(session),
        EventRecordRepository(session),
    )

    try:
        event, category = service.create_report(
            user_id=current_user.id,
            category=report.category,
            description=report.description,
            latitude=report.latitude,
            longitude=report.longitude,
            photo_url=report.photo_url,
        )
    except InvalidReportCategoryError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ReportCreateResponse(
        id=event.id,
        category=category,
        description=event.description,
        latitude=event.latitude,
        longitude=event.longitude,
        photo_url=event.photo_url,
        status=event.status,
        created_at=event.created_at,
    )


@router.get(
    "",
    response_model=list[ReportListItemResponse],
    summary="Consultar mis reportes",
    description=(
        "Devuelve únicamente los reportes SmartReport "
        "registrados por el usuario autenticado."
    ),
    responses={
        401: {
            "description": "Usuario no autenticado.",
        },
    },
)
def list_my_reports(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> list[ReportListItemResponse]:
    repository = EventRecordRepository(session)
    service = ReportQueryService(repository)

    reports = service.list_user_reports(
        current_user.id,
    )

    return [
        ReportListItemResponse(
            id=report.id,
            category=report.event_type.code,
            status=report.status,
            created_at=report.created_at,
        )
        for report in reports
    ]


@router.get(
    "/{report_id}",
    response_model=ReportDetailResponse,
    summary="Consultar detalle de un reporte",
    description=(
        "Devuelve el detalle de un reporte perteneciente "
        "al usuario autenticado."
    ),
    responses={
        401: {
            "description": "Usuario no autenticado.",
        },
        404: {
            "description": (
                "El reporte no existe o no pertenece "
                "al usuario autenticado."
            ),
        },
    },
)
def get_my_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> ReportDetailResponse:
    repository = EventRecordRepository(session)
    service = ReportQueryService(repository)

    try:
        report = service.get_user_report(
            report_id,
            current_user.id,
        )
    except QueryReportNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ReportDetailResponse(
        id=report.id,
        category=report.event_type.code,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        photo_url=report.photo_url,
        status=report.status,
        created_at=report.created_at,
    )


@router.post(
    "/{report_id}/photo",
    response_model=ReportCreateResponse,
    summary="Adjuntar fotografía a un reporte",
    description=(
        "Adjunta una fotografía a un reporte existente "
        "del usuario autenticado."
    ),
    responses={
        401: {
            "description": "Usuario no autenticado.",
        },
        403: {
            "description": (
                "El reporte no pertenece al usuario autenticado."
            ),
        },
        404: {
            "description": "El reporte no existe.",
        },
        413: {
            "description": (
                "La fotografía supera el tamaño permitido."
            ),
        },
        415: {
            "description": (
                "El formato de imagen no está permitido."
            ),
        },
    },
)
async def attach_report_photo(
    report_id: str,
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_database_session),
) -> ReportCreateResponse:
    repository = EventRecordRepository(session)

    service = ReportPhotoService(
        repository,
        Path("uploads/reports"),
    )

    try:
        event = await service.attach_photo(
            report_id=report_id,
            user_id=current_user.id,
            photo=photo,
        )
    except PhotoReportNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ReportOwnershipError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except InvalidImageTypeError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except ImageTooLargeError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        ) from exc

    return ReportCreateResponse(
        id=event.id,
        category=event.event_type.code,
        description=event.description,
        latitude=event.latitude,
        longitude=event.longitude,
        photo_url=event.photo_url,
        status=event.status,
        created_at=event.created_at,
    )