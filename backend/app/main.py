from fastapi import FastAPI
from app.routers.auth import router as auth_router

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
    ],
)
app.include_router(auth_router)

@app.get(
    "/health",
    tags=["Health"],
    summary="Verificar el estado de la API",
    description=(
        "Comprueba que el servicio SmartSafe API está disponible "
        "y responde correctamente."
    ),
    response_description="Estado operativo del servicio.",
    responses={
        200: {
            "description": "La API está operativa.",
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