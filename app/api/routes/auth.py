from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from common.token import create_access_token, verify_password
from db.models import User
from db.repositories.users import UsersRepository
from shemas import TokenOutData, UserCreateToken

router = APIRouter()


@router.post("/", summary="Получение токена", response_model=TokenOutData)
async def get_access_token(user: UserCreateToken, users_repo: UsersRepository = Depends()):
    user_in_db: User = await users_repo.get_object(email=user.email)
    access_token = create_access_token(user_id=user_in_db.id)
    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
    return TokenOutData(type="Bearer", access_token=access_token)
