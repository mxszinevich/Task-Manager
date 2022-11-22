from typing import Callable

from faker import Faker
from pydantic import BaseModel, Field
import pytest

from common.token import create_access_token
from db.models import User
from db.repositories.users import UsersRepository
from shemas import TokenOutData

faker = Faker(locale="ru_RU")


class UserFactory(BaseModel):
    name: str = Field(default_factory=faker.name)
    email: str = Field(default_factory=faker.email)
    password: str = Field(default_factory=faker.password)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


@pytest.fixture()
def user_registration_data() -> Callable:
    def build_data(**kwargs) -> dict:
        return UserFactory(**kwargs).dict()

    return build_data


@pytest.fixture()
def user_factory(override_get_db_session) -> Callable:
    async def build_user(**kwargs) -> User:
        async for session in override_get_db_session():
            users_repo = UsersRepository(session=session)
            user: User = await users_repo.create(UserFactory(**kwargs))
        return user

    return build_user


@pytest.fixture
async def user_active(user_factory) -> User:
    return await user_factory()


@pytest.fixture
async def user_inactive(user_factory) -> User:
    return await user_factory(is_active=False)


@pytest.fixture
async def access_token() -> TokenOutData:
    def build_token(user_id: int):
        access_token = create_access_token(user_id=user_id)
        return TokenOutData(type="Bearer", access_token=access_token)

    return build_token
