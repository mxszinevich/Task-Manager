import json

from httpx import AsyncClient
import pytest
from starlette import status

from db.repositories.tasks import TasksRepository

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
