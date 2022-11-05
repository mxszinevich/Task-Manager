import pytest

from common.token import create_access_token
from db.models import User
from db.repositories.users import UsersRepository
from shemas import TokenOutData, UserRegistration


@pytest.fixture()
def user_registration_data(faker) -> dict:
    user_data = {"name": faker.name(), "email": faker.email(), "password": faker.password()}

    def build_data(**kwargs):
        return {**user_data, **kwargs}

    return build_data


@pytest.fixture
async def user_active_in_db(user_registration_data, override_get_db_session) -> User:
    user_registration_data = user_registration_data()
    async for session in override_get_db_session():
        users_repo = UsersRepository(session=session)
        await users_repo.create(UserRegistration(**user_registration_data))
        await session.commit()
        user = await users_repo.get_object(email=user_registration_data["email"])
        return user


@pytest.fixture
async def user_inactive_in_db(user_registration_data, override_get_db_session, faker) -> User:
    user_registration_data = user_registration_data(name=faker.name(), email=faker.email())
    async for session in override_get_db_session():
        users_repo = UsersRepository(session=session)
        await users_repo.create(UserRegistration(**user_registration_data).copy(update={"is_active": False}))
        await session.commit()
        user = await users_repo.get_object(email=user_registration_data["email"])
        return user


@pytest.fixture
async def access_token() -> TokenOutData:
    def build_token(user_id: int):
        access_token = create_access_token(user_id=user_id)
        return TokenOutData(type="Bearer", access_token=access_token)

    return build_token
