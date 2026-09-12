import os

from dotenv import load_dotenv

load_dotenv()


def get_jwt_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY no esta configurada")
    return secret_key


def get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM", "HS256")


def get_jwt_access_token_expire_minutes() -> int:
    value = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    minutes = int(value)

    if minutes <= 0:
        raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que cero")

    return minutes