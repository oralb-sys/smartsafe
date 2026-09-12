from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService, InvalidCredentialsError


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


def get_database_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica un usuario mediante correo y contraseña.",
    responses={
        401: {
            "description": "Credenciales inválidas.",
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