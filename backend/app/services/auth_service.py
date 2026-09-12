from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.shared.jwt_service import create_access_token
from app.shared.security import verify_password


class InvalidCredentialsError(Exception):
    """Indica que las credenciales proporcionadas no son válidas."""


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> User:
        """Autentica un usuario mediante correo y contraseña."""
        user = self.user_repository.get_by_email(email)

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Credenciales invalidas")

        return user

    def create_token(self, user: User) -> str:
        """Genera un token de acceso para un usuario autenticado."""
        return create_access_token(
            user_id=user.id,
            role=user.role,
        )