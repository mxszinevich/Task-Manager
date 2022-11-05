from datetime import datetime

from fastapi import Body
from pydantic import EmailStr

from shemas import OrmBaseModel


class BaseUserModel(OrmBaseModel):
    name: str = Body(..., description="Имя пользователя")
    email: EmailStr


class UserRegistration(BaseUserModel):
    password: str = Body(..., description="Пароль", min_length=6)


class UserRegistrationOut(BaseUserModel):
    ...


class UserInfoOut(BaseUserModel):
    id: int
    is_active: bool
    created: datetime


class UserCreateToken(OrmBaseModel):
    email: EmailStr
    password: str
