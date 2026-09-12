from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import UploadFile

from app.services.report_photo_service import (
    ImageTooLargeError,
    InvalidImageTypeError,
    ReportNotFoundError,
    ReportOwnershipError,
    ReportPhotoService,
)


class FakeRepository:
    def __init__(self, report=None):
        self.report = report
        self.updated_photo_url = None

    def get_by_id(self, report_id):
        return self.report

    def update_photo_url(self, report, photo_url):
        self.updated_photo_url = photo_url
        report.photo_url = photo_url
        return report


def make_upload(
    content: bytes = b"fake-image",
    content_type: str = "image/jpeg",
    filename: str = "photo.jpg",
):
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers={"content-type": content_type},
    )


@pytest.mark.anyio
async def test_attach_photo_success(tmp_path):
    report = SimpleNamespace(
        id="report-1",
        user_id="user-1",
        photo_url=None,
    )

    repository = FakeRepository(report)

    service = ReportPhotoService(
        repository=repository,
        upload_directory=tmp_path,
    )

    photo = make_upload()

    result = await service.attach_photo(
        report_id="report-1",
        user_id="user-1",
        photo=photo,
    )

    assert result.photo_url is not None
    assert result.photo_url.startswith("/uploads/reports/")
    assert result.photo_url.endswith(".jpg")

    saved_files = list(tmp_path.iterdir())

    assert len(saved_files) == 1
    assert saved_files[0].read_bytes() == b"fake-image"


@pytest.mark.anyio
async def test_attach_photo_report_not_found(tmp_path):
    repository = FakeRepository(report=None)

    service = ReportPhotoService(
        repository=repository,
        upload_directory=tmp_path,
    )

    with pytest.raises(ReportNotFoundError):
        await service.attach_photo(
            report_id="missing-report",
            user_id="user-1",
            photo=make_upload(),
        )


@pytest.mark.anyio
async def test_attach_photo_rejects_other_users_report(tmp_path):
    report = SimpleNamespace(
        id="report-1",
        user_id="user-owner",
        photo_url=None,
    )

    repository = FakeRepository(report)

    service = ReportPhotoService(
        repository=repository,
        upload_directory=tmp_path,
    )

    with pytest.raises(ReportOwnershipError):
        await service.attach_photo(
            report_id="report-1",
            user_id="another-user",
            photo=make_upload(),
        )


@pytest.mark.anyio
async def test_attach_photo_rejects_invalid_content_type(tmp_path):
    report = SimpleNamespace(
        id="report-1",
        user_id="user-1",
        photo_url=None,
    )

    repository = FakeRepository(report)

    service = ReportPhotoService(
        repository=repository,
        upload_directory=tmp_path,
    )

    photo = make_upload(
        content=b"not-an-image",
        content_type="text/plain",
        filename="file.txt",
    )

    with pytest.raises(InvalidImageTypeError):
        await service.attach_photo(
            report_id="report-1",
            user_id="user-1",
            photo=photo,
        )


@pytest.mark.anyio
async def test_attach_photo_rejects_file_larger_than_5mb(tmp_path):
    report = SimpleNamespace(
        id="report-1",
        user_id="user-1",
        photo_url=None,
    )

    repository = FakeRepository(report)

    service = ReportPhotoService(
        repository=repository,
        upload_directory=tmp_path,
    )

    photo = make_upload(
        content=b"x" * (5 * 1024 * 1024 + 1),
    )

    with pytest.raises(ImageTooLargeError):
        await service.attach_photo(
            report_id="report-1",
            user_id="user-1",
            photo=photo,
        )