from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.reports import router as reports_router


app = FastAPI(
    title="SmartSafe API",
    description=(
        "API REST de SmartSafe, plataforma acad?mica de seguridad "
        "y gesti?n urbana que integra los m?dulos SmartReport y SmartSOS.\n\n"
        "## M?dulos\n"
        "- **SmartReport:** registro y seguimiento de incidencias urbanas no urgentes.\n"
        "- **SmartSOS:** prototipo acad?mico para registrar y dar seguimiento "
        "a alertas de emergencia.\n\n"
        "## Alcance\n"
        "SmartSOS es un prototipo acad?mico y no reemplaza los servicios "
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
            "description": "Autenticaci?n de usuarios de SmartSafe.",
        },
        {
            "name": "SmartReport",
            "description": "Gesti?n de incidencias urbanas no urgentes.",
        },
    ],
)

app.include_router(auth_router)
app.include_router(reports_router)


@app.get(
    "/health",
    tags=["Health"],
    summary="Verificar el estado de la API",
    description=(
        "Comprueba que el servicio SmartSafe API est? disponible "
        "y responde correctamente."
    ),
    response_description="Estado operativo del servicio.",
    responses={
        200: {
            "description": "La API est? operativa.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "service": "SmartSafe API",
                    }
                }
            },
        }
    },
)
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "SmartSafe API"}
