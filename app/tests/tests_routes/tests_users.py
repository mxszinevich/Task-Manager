import random

from httpx import AsyncClient
import pytest
from starlette import status

from db.constants import StatusType
from db.repositories.users import UsersRepository
from shemas import TokenOutData

pytestmark = pytest.mark.asyncio


async def test_users_registration(test_client: AsyncClient, override_get_db_session, user_registration_data):
    user_registration_data: dict = user_registration_data()
    res = await test_client.post("users/", json=user_registration_data)
    assert res.status_code == status.HTTP_201_CREATED
    res_json = res.json()
    assert res_json["id"]
    assert res_json["name"] == user_registration_data["name"]
    assert res_json["email"] == user_registration_data["email"]

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


async def test_users_me_active_user(test_client: AsyncClient, access_token, user_factory, override_get_db_session):
    user = await user_factory()
    token_data: TokenOutData = access_token(user_id=user.id)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {token_data.access_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "count_task_created": 0,
        "count_task_completed": 0,
        "count_task_expired": 0,
        "created": user.created.strftime("%Y-%m-%d %H:%M"),
    }

    res = await test_client.get("users/me")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    replace_token = token_data.access_token
    replace_token = replace_token.replace(replace_token[0], replace_token[1], 1)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {replace_token}"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_users_me_inactive_user(test_client: AsyncClient, access_token, user_factory):
    user = await user_factory(is_active=False)
    token_data = access_token(user_id=user.id)
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {token_data.access_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "count_task_created": 0,
        "count_task_completed": 0,
        "count_task_expired": 0,
        "created": user.created.strftime("%Y-%m-%d %H:%M"),
    }


async def test_users_me_with_tasks(test_cred_client: AsyncClient, tasks_generating, user_active):
    created_tasks = await tasks_generating(2)
    completed_tasks = await tasks_generating(10, status=StatusType.COMPLETED)
    expired_tasks = await tasks_generating(4, status=StatusType.EXPIRED)
    res = await test_cred_client.get("users/me")
    res_json = res.json()
    assert res_json["id"] == user_active.id
    assert res_json["count_task_created"] == len(created_tasks)
    assert res_json["count_task_completed"] == len(completed_tasks)
    assert res_json["count_task_expired"] == len(expired_tasks)


async def test_users_me_none_user(test_client: AsyncClient, access_token):
    token_data = access_token(user_id=random.randint(100, 200))
    res = await test_client.get("users/me", headers={"Authorization": f"{token_data.type} {token_data.access_token}"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_user_delete(test_client: AsyncClient, access_token, user_factory, override_get_db_session):
    user_active = await user_factory()
    user_inactive = await user_factory(is_active=False)
    token_data = access_token(user_id=user_active.id)

    res = await test_client.delete(
        f"users/{user_inactive.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = await test_client.delete(
        f"users/{user_active.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_204_NO_CONTENT

    async for session in override_get_db_session():
        users_repo = UsersRepository(session=session)
        user = await users_repo.get_object(email=user_active.email)
        assert user is None
