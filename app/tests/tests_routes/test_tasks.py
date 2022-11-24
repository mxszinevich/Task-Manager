import json

from httpx import AsyncClient
import pytest
from starlette import status

from db.repositories.tasks import TasksRepository
from shemas import TokenOutData

pytestmark = pytest.mark.asyncio


async def test_task_create(test_client: AsyncClient, user_active, user_inactive, access_token, override_get_db_session):
    token_data = access_token(user_id=user_active.id)
    data = {
        "name": "test_task",
        "body": "test_body",
    }
    res = await test_client.post(
        "tasks/", data=json.dumps(data), headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "name": "test_task",
        "body": "test_body",
        "id": 1,
        "user_id": user_active.id,
    }
    async for session in override_get_db_session():
        tasks_repo = TasksRepository(session=session)
        tasks_count = await tasks_repo.count()
        assert tasks_count == 1

    token_data = access_token(user_id=user_inactive.id)
    res = await test_client.post(
        "tasks/", data=json.dumps(data), headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


async def test_task_list(tasks_generating, test_cred_client):
    tasks = await tasks_generating(3)
    res = await test_cred_client.get("tasks/")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 3
    assert res.json() == [
        {
            "name": task.name,
            "body": task.body,
            "id": task.id,
            "user_id": task.user_id,
            "created": task.created.strftime("%Y-%m-%d %H:%M"),
            "active": task.active,
        }
        for task in tasks
    ]


@pytest.mark.parametrize("data_gen,active", [({"n": 2}, True), ({"n": 3, "active": False}, False)])
async def test_task_list_filters(tasks_generating, test_cred_client, data_gen, active):
    tasks = await tasks_generating(**data_gen)
    res = await test_cred_client.get("tasks/", params={"active": active})
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == data_gen["n"]
    assert res.json() == [
        {
            "name": task.name,
            "body": task.body,
            "id": task.id,
            "user_id": task.user_id,
            "created": task.created.strftime("%Y-%m-%d %H:%M"),
            "active": task.active,
        }
        for task in tasks
    ]


async def test_task_detail(task, test_cred_client, faker):
    res = await test_cred_client.get(f"tasks/{task.id}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "name": task.name,
        "body": task.body,
        "id": task.id,
        "user_id": task.user_id,
        "created": task.created.strftime("%Y-%m-%d %H:%M"),
        "active": task.active,
    }

    res = await test_cred_client.get(f"tasks/{faker.pyint(min_value=1000)}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_task_detail_with_another_user(task, test_client, access_token, another_user_active):
    token_data: TokenOutData = access_token(user_id=another_user_active.id)
    res = await test_client.get(
        f"tasks/{task.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": f"Объект с id={task.id} не существует"}


async def test_task_delete(task, test_cred_client, override_get_db_session):
    res = await test_cred_client.delete(f"tasks/{task.id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT

    async for session in override_get_db_session():
        tasks_repo = TasksRepository(session=session)
        task = await tasks_repo.get_object(id=task.id)
        assert task is None


async def test_task_delete_with_another_user(
    task, test_client, access_token, another_user_active, override_get_db_session
):
    token_data: TokenOutData = access_token(user_id=another_user_active.id)
    res = await test_client.delete(
        f"tasks/{task.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND

    async for session in override_get_db_session():
        tasks_repo = TasksRepository(session=session)
        task = await tasks_repo.get_object(id=task.id)
        assert task is not None


async def test_task_delete_with_super_user(task, test_client, access_token, super_user, override_get_db_session):
    token_data: TokenOutData = access_token(user_id=super_user.id)
    res = await test_client.delete(
        f"tasks/{task.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )

    assert res.status_code == status.HTTP_204_NO_CONTENT

    async for session in override_get_db_session():
        tasks_repo = TasksRepository(session=session)
        task = await tasks_repo.get_object(id=task.id)
        assert task is None


async def test_task_update(task, test_cred_client):
    update_data = {
        "name": "updated_name",
        "body": "updated_body1",
    }
    res = await test_cred_client.patch(f"tasks/{task.id}", json=update_data)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "name": "updated_name",
        "body": "updated_body1",
        "id": task.id,
        "user_id": task.user_id,
        "created": task.created.strftime("%Y-%m-%d %H:%M"),
        "active": task.active,
    }
    update_data = {
        "body": "updated_body2",
    }
    res = await test_cred_client.patch(f"tasks/{task.id}", json=update_data)
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert res_json["name"] == "updated_name"
    assert res_json["body"] == "updated_body2"

    res = await test_cred_client.patch(f"tasks/{task.id}")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_task_update_with_another_user(
    task, test_client, access_token, another_user_active, override_get_db_session
):
    update_data = {
        "name": "updated_name",
        "body": "updated_body1",
    }
    token_data: TokenOutData = access_token(user_id=another_user_active.id)
    res = await test_client.patch(
        f"tasks/{task.id}", json=update_data, headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_task_update_with_inactive_user(task, test_client, access_token, user_inactive, override_get_db_session):
    update_data = {
        "name": "updated_name",
        "body": "updated_body1",
    }
    token_data: TokenOutData = access_token(user_id=user_inactive.id)
    res = await test_client.patch(
        f"tasks/{task.id}", json=update_data, headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN
