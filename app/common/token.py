from datetime import datetime, timedelta

from config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.app.token_expires_min)
    payload = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(payload, settings.app.token_secret_key, algorithm=settings.app.token_algorithm)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
