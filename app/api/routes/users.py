from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies.users import get_user
from db.models import User
from db.repositories.users import UsersRepository
from shemas import UserInfoOut, UserRegistration, UserRegistrationOut

router = APIRouter()


@router.post(
    "/", summary="Регистрация пользователя", response_model=UserRegistrationOut, status_code=status.HTTP_201_CREATED
)
async def user_registration(user: UserRegistration, users_repo: UsersRepository = Depends()):
    await users_repo.create(user)
    return user


@router.get("/me", summary="Информация о пользователе", response_model=UserInfoOut)
async def user_me(user: User = Depends(get_user)):
    return user
