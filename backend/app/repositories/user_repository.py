from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        """Busca un usuario por su correo electrónico."""
        statement = select(User).where(User.email == email)
        return self.session.scalar(statement)