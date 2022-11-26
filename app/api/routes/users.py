from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies.users import get_superuser, get_user
from api.filters import UsersListFilter
from common import BadRequestException, ForbiddenException
from db.models import User
from db.repositories.users import UsersRepository
from shemas import UserInfoOut, UserRegistration, UserRegistrationOut

router = APIRouter()


@router.post(
    "/", summary="Регистрация пользователя", response_model=UserRegistrationOut, status_code=status.HTTP_201_CREATED
)
async def user_registration(user: UserRegistration, users_repo: UsersRepository = Depends()):
    user_check: User | None = await users_repo.get_object(email=user.email)
    if user_check is not None:
        raise BadRequestException(detail="Пользователь с таким email уже существует")

    return await users_repo.create(user)


@router.get("/me", summary="Информация о пользователе", response_model=UserInfoOut)
async def user_me(user: User = Depends(get_user), users_repo: UsersRepository = Depends()):
    return await users_repo.user_info(user.id)


@router.delete("/{user_id}", summary="Удаление пользователя", status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: int, user: User = Depends(get_user), users_repo: UsersRepository = Depends()):
    if user.id == user_id or user.is_superuser:
        await users_repo.delete(id=user_id)
    else:
        raise ForbiddenException


@router.get("/", summary="Список пользователей", response_model=list[UserInfoOut])
async def users_list(
    filters: UsersListFilter = Depends(), user: User = Depends(get_superuser), users_repo: UsersRepository = Depends()
):
    return await users_repo.filters(**filters.dict(exclude_none=True))
