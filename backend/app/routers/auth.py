from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService, InvalidCredentialsError


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesi?n",
    description="Autentica un usuario mediante correo y contrase?a.",
    responses={
        401: {
            "description": "Credenciales inv?lidas.",
        }
    },
)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_database_session),
) -> LoginResponse:
    repository = UserRepository(session)
    service = AuthService(repository)

    try:
        user = service.authenticate(
            email=str(credentials.email),
            password=credentials.password,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        ) from exc

    access_token = service.create_token(user)

    return LoginResponse(
        access_token=access_token,
        role=user.role,
    )
