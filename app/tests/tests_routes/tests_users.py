import json

from httpx import AsyncClient
import pytest
from starlette import status

from db.models import User
from db.repositories.users import UsersRepository
from shemas import TokenOutData, UserInfoOut

pytestmark = pytest.mark.asyncio


async def test_user_registration(test_client: AsyncClient, override_get_db_session, user_registration_data):
    user_registration_data = user_registration_data()
    res = await test_client.post("users/", json=user_registration_data)
    assert res.status_code == status.HTTP_201_CREATED

    async for session in override_get_db_session():
        users_repo = UsersRepository(session=session)
        count_users = await users_repo.count()
        assert count_users == 1
        user = await users_repo.get_object(email=user_registration_data["email"])
        assert user.name == user_registration_data["name"]
        assert user.is_active is True

    res = await test_client.post("users/", json=user_registration_data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "Пользователь с таким email уже существует"}

    registration_data = user_registration_data.copy()
    registration_data.pop("password")
    res = await test_client.post("users/", json=registration_data)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    registration_data = user_registration_data.copy()
    registration_data.pop("name")
    registration_data = {"email": "user@example.com", "password": "test"}
    res = await test_client.post("users/", json=registration_data)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_user_me_active_user(test_client: AsyncClient, access_token, user_active_in_db: User):
    token_data: TokenOutData = access_token(user_id=user_active_in_db.id)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {token_data.access_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == json.loads(UserInfoOut.from_orm(user_active_in_db).json())

    res = await test_client.get("users/me")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    replace_token = token_data.access_token
    replace_token = replace_token.replace(replace_token[0], replace_token[1], 1)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {replace_token}"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_user_me_inactive_user(test_client: AsyncClient, access_token, user_inactive_in_db: User):
    token_data = access_token(user_id=user_inactive_in_db.id)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {token_data.access_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == json.loads(UserInfoOut.from_orm(user_inactive_in_db).json())
