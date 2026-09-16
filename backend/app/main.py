from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi.staticfiles import StaticFiles

from app.routers.auth import (
    router as auth_router,
)
from app.routers.emergencies import (
    router as emergencies_router,
)
from app.routers.events import (
    router as events_router,
)
from app.routers.reports import (
    router as reports_router,
)


app = FastAPI(
    title="SmartSafe API",
    description=(
        "API REST de SmartSafe, plataforma académica de seguridad "
        "y gestión urbana que integra los módulos SmartReport y SmartSOS.\n\n"
        "## Módulos\n"
        "- **SmartReport:** registro y seguimiento de incidencias urbanas no urgentes.\n"
        "- **SmartSOS:** prototipo académico para registrar y dar seguimiento "
        "a alertas de emergencia.\n\n"
        "## Alcance\n"
        "SmartSOS es un prototipo académico y no reemplaza los servicios "
        "oficiales de emergencia."
    ),
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Health",
            "description": (
                "Operaciones para verificar "
                "el estado de la API."
            ),
        },
        {
            "name": "Authentication",
            "description": (
                "Autenticación de usuarios "
                "de SmartSafe."
            ),
        },
        {
            "name": "SmartReport",
            "description": (
                "Gestión de incidencias "
                "urbanas no urgentes."
            ),
        },
        {
            "name": "SmartSOS",
            "description": (
                "Gestión de alertas "
                "de emergencia."
            ),
        },
        {
            "name": "UrbanEvents",
            "description": (
                "Consulta unificada de eventos "
                "SmartReport y SmartSOS."
            ),
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads",
        check_dir=False,
    ),
    name="uploads",
)

app.include_router(
    auth_router
)

app.include_router(
    reports_router
)

app.include_router(
    emergencies_router
)

app.include_router(
    events_router
)


@app.get(
    "/health",
    tags=["Health"],
    summary="Verificar el estado de la API",
    description=(
        "Comprueba que el servicio SmartSafe API está disponible "
        "y responde correctamente."
    ),
    response_description=(
        "Estado operativo del servicio."
    ),
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "SmartSafe API",
    }