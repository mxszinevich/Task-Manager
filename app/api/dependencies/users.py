from fastapi import Depends
from jose import JWTError, jwt

from api.dependencies.token import TokenInputData
from common import ForbiddenException, UnauthorizedException
from config import settings
from db.models import User
from db.repositories.users import UsersRepository


async def get_user(
    credentials: TokenInputData = Depends(TokenInputData()), users_rep: UsersRepository = Depends()
) -> User:
    try:
        schema, token = credentials.split(" ")
        if schema != "Bearer":
            raise UnauthorizedException
        payload = jwt.decode(token, settings.app.token_secret_key, algorithms=[settings.app.token_algorithm])
        user_id: int | None = int(payload["sub"])
        if user_id is None:
            raise UnauthorizedException
    except (JWTError, ValueError):
        raise UnauthorizedException
    user: User = await users_rep.get_object(id=user_id)
    if user is None:
        raise UnauthorizedException

    return user


async def get_active_user(user: User = Depends(get_user)) -> User:
    if not user.is_active:
        raise ForbiddenException(detail="Аккаунт заблокирован")
    return user


async def get_superuser(user: User = Depends(get_active_user)) -> User:
    if not user.is_superuser:
        raise ForbiddenException(detail="Нет доступа")
    return user
