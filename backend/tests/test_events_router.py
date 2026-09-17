from datetime import (
    datetime,
    timezone,
)
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import (
    MagicMock,
    patch,
)

from fastapi import FastAPI
from fastapi.testclient import (
    TestClient,
)

from app.dependencies import (
    get_current_user,
    get_database_session,
)
from app.routers.events import router


app = FastAPI()

app.include_router(
    router
)


def override_database_session():
    yield MagicMock()


def override_operator_user():
    return SimpleNamespace(
        id="operator-123",
        role="OPERATOR",
    )


def override_citizen_user():
    return SimpleNamespace(
        id="user-123",
        role="CITIZEN",
    )


app.dependency_overrides[
    get_database_session
] = override_database_session

app.dependency_overrides[
    get_current_user
] = override_operator_user


client = TestClient(
    app
)


def build_events():
    report = SimpleNamespace(
        id="report-1",
        status="REPORTED",
        description="Bache en la vía",
        latitude=Decimal(
            "-13.5204"
        ),
        longitude=Decimal(
            "-71.9751"
        ),
        photo_url=None,
        created_at=datetime.now(
            timezone.utc
        ),
    )

    report_type = SimpleNamespace(
        code="POTHOLE",
        module="SMART_REPORT",
    )

    emergency = SimpleNamespace(
        id="emergency-1",
        status="ACTIVE",
        description=None,
        latitude=Decimal(
            "-13.5210"
        ),
        longitude=Decimal(
            "-71.9760"
        ),
        photo_url=None,
        created_at=datetime.now(
            timezone.utc
        ),
    )

    emergency_type = SimpleNamespace(
        code="SOS",
        module="SMART_SOS",
    )

    return [
        (
            report,
            report_type,
        ),
        (
            emergency,
            emergency_type,
        ),
    ]


def test_list_events_returns_200_for_operator():
    with patch(
        "app.routers.events."
        "EventQueryService.list_events",
        return_value=build_events(),
    ) as mock_list_events:
        response = client.get(
            "/api/v1/events"
        )

    assert response.status_code == 200

    mock_list_events.assert_called_once_with(
        source=None,
        event_type=None,
        status=None,
    )

    data = response.json()

    assert len(data) == 2

    assert (
        data[0]["source"]
        == "SMART_REPORT"
    )

    assert (
        data[0]["type"]
        == "POTHOLE"
    )

    assert (
        data[1]["source"]
        == "SMART_SOS"
    )

    assert (
        data[1]["type"]
        == "SOS"
    )


def test_list_events_filters_by_source():
    with patch(
        "app.routers.events."
        "EventQueryService.list_events",
        return_value=[],
    ) as mock_list_events:
        response = client.get(
            "/api/v1/events"
            "?source=SMART_REPORT"
        )

    assert response.status_code == 200

    mock_list_events.assert_called_once_with(
        source="SMART_REPORT",
        event_type=None,
        status=None,
    )

    assert response.json() == []


def test_list_events_filters_by_type():
    with patch(
        "app.routers.events."
        "EventQueryService.list_events",
        return_value=[],
    ) as mock_list_events:
        response = client.get(
            "/api/v1/events"
            "?type=POTHOLE"
        )

    assert response.status_code == 200

    mock_list_events.assert_called_once_with(
        source=None,
        event_type="POTHOLE",
        status=None,
    )


def test_list_events_filters_by_status():
    with patch(
        "app.routers.events."
        "EventQueryService.list_events",
        return_value=[],
    ) as mock_list_events:
        response = client.get(
            "/api/v1/events"
            "?status=ACTIVE"
        )

    assert response.status_code == 200

    mock_list_events.assert_called_once_with(
        source=None,
        event_type=None,
        status="ACTIVE",
    )


def test_list_events_combines_filters():
    with patch(
        "app.routers.events."
        "EventQueryService.list_events",
        return_value=[],
    ) as mock_list_events:
        response = client.get(
            "/api/v1/events"
            "?source=SMART_REPORT"
            "&type=POTHOLE"
            "&status=REPORTED"
        )

    assert response.status_code == 200

    mock_list_events.assert_called_once_with(
        source="SMART_REPORT",
        event_type="POTHOLE",
        status="REPORTED",
    )


def test_list_events_forbidden_for_citizen():
    app.dependency_overrides[
        get_current_user
    ] = override_citizen_user

    try:
        response = client.get(
            "/api/v1/events"
        )

        assert (
            response.status_code
            == 403
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = override_operator_user