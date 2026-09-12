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
