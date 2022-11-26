from datetime import datetime

from fastapi import Body
from pydantic import EmailStr, validator

from shemas import OrmBaseModel


class BaseUserModel(OrmBaseModel):
    name: str = Body(..., description="Имя пользователя")
    email: EmailStr


class UserRegistration(BaseUserModel):
    password: str = Body(..., description="Пароль", min_length=6)


class UserRegistrationOut(BaseUserModel):
    id: int


class UserInfoOut(BaseUserModel):
    id: int
    count_task_created: int | None
    count_task_completed: int | None
    count_task_expired: int | None
    created: str

    @validator("created", pre=True)
    def created_format(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")


class UserCreateToken(OrmBaseModel):
    email: EmailStr
    password: str
