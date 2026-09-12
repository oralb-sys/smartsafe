from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.reports import router as reports_router


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
            "description": "Operaciones para verificar el estado de la API.",
        },
        {
            "name": "Authentication",
            "description": "Autenticación de usuarios de SmartSafe.",
        },
        {
            "name": "SmartReport",
            "description": "Gestión de incidencias urbanas no urgentes.",
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

app.include_router(auth_router)
app.include_router(reports_router)


@app.get(
    "/health",
    tags=["Health"],
    summary="Verificar el estado de la API",
    description=(
        "Comprueba que el servicio SmartSafe API está disponible "
        "y responde correctamente."
    ),
    response_description="Estado operativo del servicio.",
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "SmartSafe API",
    }