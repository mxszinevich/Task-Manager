from fastapi import APIRouter, Depends

from common import UnauthorizedException
from common.token import create_access_token, verify_password
from db.models import User
from db.repositories.users import UsersRepository
from shemas import TokenOutData, UserCreateToken

router = APIRouter()


@router.post("/", summary="Получение токена", response_model=TokenOutData)
async def get_access_token(user: UserCreateToken, users_repo: UsersRepository = Depends()):
    user_in_db: User | None = await users_repo.get_object(email=user.email)
    if user_in_db is None:
        raise UnauthorizedException(detail="Неверный email")
    access_token = create_access_token(user_id=user_in_db.id)
    if not verify_password(user.password, user_in_db.password):
        raise UnauthorizedException(detail="Неверный пароль")
    return TokenOutData(type="Bearer", access_token=access_token)
