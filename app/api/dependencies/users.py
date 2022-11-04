from api.dependencies.token import TokenInputData
from common import UnauthorizedException
from config import settings
from db.models import User
from db.repositories.users import UsersRepository
from fastapi import Depends, HTTPException
from jose import JWTError, jwt


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
    try:
        user: User = await users_rep.get_object(id=user_id)
    except HTTPException:
        raise UnauthorizedException

    return user
