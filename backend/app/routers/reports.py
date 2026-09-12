from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_database_session
from app.models.user import User
from app.repositories.event_record_repository import EventRecordRepository
from app.repositories.event_type_repository import EventTypeRepository
from app.schemas.report import ReportCreateRequest, ReportCreateResponse
from app.services.report_service import (
    InvalidReportCategoryError,
    ReportService,
)
from pathlib import Path

from fastapi import File, UploadFile
from app.services.report_photo_service import (
    ImageTooLargeError,
    InvalidImageTypeError,
    ReportNotFoundError,
    ReportOwnershipError,
    ReportPhotoService,
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
        "Registra una incidencia urbana no urgente asociada al usuario "
        "autenticado. El estado inicial es REPORTED."
    ),
    responses={
        401: {"description": "Usuario no autenticado."},
        422: {"description": "Datos de entrada inv?lidos."},
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
@router.post(
    "/{report_id}/photo",
    response_model=ReportCreateResponse,
    summary="Adjuntar fotografía a un reporte",
    description=(
        "Adjunta una fotografía a un reporte existente "
        "del usuario autenticado."
    ),
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
    except ReportNotFoundError as exc:
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

    event_type_repository = EventTypeRepository(session)
    event_type = event_type_repository.get_smart_report_type_by_code(
        next(
            code
            for code in (
                "POTHOLE",
                "WASTE",
                "STREET_LIGHT",
                "WATER_LEAK",
            )
            if event.event_type.code == code
        )
    )

    return ReportCreateResponse(
        id=event.id,
        category=event_type.code,
        description=event.description,
        latitude=event.latitude,
        longitude=event.longitude,
        photo_url=event.photo_url,
        status=event.status,
        created_at=event.created_at,
    )