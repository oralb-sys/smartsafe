from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from app.shared.auth_config import (
    get_jwt_access_token_expire_minutes,
    get_jwt_algorithm,
    get_jwt_secret_key,
)


def create_access_token(user_id: str, role: str) -> str:
    """Genera un token JWT de acceso para un usuario."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=get_jwt_access_token_expire_minutes()
    )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        get_jwt_secret_key(),
        algorithm=get_jwt_algorithm(),
    )


def decode_access_token(token: str) -> dict:
    """Valida y decodifica un token JWT de acceso."""
    try:
        return jwt.decode(
            token,
            get_jwt_secret_key(),
            algorithms=[get_jwt_algorithm()],
        )
    except InvalidTokenError as exc:
        raise ValueError("Token de acceso invalido") from exc