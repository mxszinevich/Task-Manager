from datetime import datetime, timedelta
from typing import Callable

import pytest

from db.constants import StatusType
from db.models import Task, User
from db.repositories.tasks import TasksRepository


@pytest.mark.asyncio
class TestTasksWorker:
    async def test_tasks_changing_status(self, task_factory: Callable, user_active: User, override_get_db_session):
        task_expired_active: Task = await task_factory(
            user_id=user_active.id,
            completion_date=datetime.today() - timedelta(days=1),
            status=StatusType.ACTIVE,
        )
        task_expired_created: Task = await task_factory(
            user_id=user_active.id,
            completion_date=datetime.today() - timedelta(days=1),
            status=StatusType.CREATED,
        )
        task_active_created: Task = await task_factory(
            user_id=user_active.id,
            completion_date=datetime.today() + timedelta(days=1),
            status=StatusType.ACTIVE,
        )
        task_none_completion_date: Task = await task_factory(user_id=user_active.id, completion_date=None)
        async for session in override_get_db_session():
            task_repo = TasksRepository(session=session)
            await task_repo.tasks_changing_status()

            task: Task = await task_repo.get_object(id=task_expired_active.id)
            assert task.status == StatusType.EXPIRED
            task: Task = await task_repo.get_object(id=task_expired_created.id)
            assert task.status == StatusType.EXPIRED
            task: Task = await task_repo.get_object(id=task_none_completion_date.id)
            assert task.status == StatusType.CREATED
            task: Task = await task_repo.get_object(id=task_active_created.id)
            assert task.status == StatusType.ACTIVE
