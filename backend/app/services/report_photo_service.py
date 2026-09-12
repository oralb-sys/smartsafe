from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.models.event_record import EventRecord
from app.repositories.event_record_repository import EventRecordRepository


MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/heic": ".heic",
    "image/heif": ".heif",
}


class ReportNotFoundError(Exception):
    pass


class ReportOwnershipError(Exception):
    pass


class InvalidImageTypeError(Exception):
    pass


class ImageTooLargeError(Exception):
    pass


class ReportPhotoService:
    def __init__(
        self,
        repository: EventRecordRepository,
        upload_directory: Path,
    ) -> None:
        self.repository = repository
        self.upload_directory = upload_directory

    async def attach_photo(
        self,
        *,
        report_id: str,
        user_id: str,
        photo: UploadFile,
    ) -> EventRecord:
        report = self.repository.get_by_id(report_id)

        if report is None:
            raise ReportNotFoundError(
                "El reporte solicitado no existe"
            )

        if report.user_id != user_id:
            raise ReportOwnershipError(
                "El reporte no pertenece al usuario autenticado"
            )

        extension = ALLOWED_CONTENT_TYPES.get(
            photo.content_type or ""
        )

        if extension is None:
            raise InvalidImageTypeError(
                "Formato de imagen no permitido"
            )

        content = await photo.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise ImageTooLargeError(
                "La imagen supera el tamaño máximo de 5 MB"
            )

        self.upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = f"{uuid4()}{extension}"
        destination = self.upload_directory / filename

        destination.write_bytes(content)

        photo_url = f"/uploads/reports/{filename}"

        return self.repository.update_photo_url(
            report,
            photo_url,
        )