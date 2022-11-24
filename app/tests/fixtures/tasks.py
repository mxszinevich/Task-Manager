from typing import Callable

from pydantic import BaseModel, Field
import pytest

from db.models import Task
from db.repositories.tasks import TasksRepository
from tests.conftest import faker


class TaskFactory(BaseModel):
    name: str = Field(default_factory=faker.word)
    body: str = Field(default_factory=faker.paragraph)
    active: bool = Field(default=True)
    user_id: int = Field(...)


@pytest.fixture()
def task_factory(override_get_db_session) -> Callable:
    async def build_task(**kwargs) -> Task:
        async for session in override_get_db_session():
            task_repo = TasksRepository(session=session)
            task: Task = await task_repo.create(TaskFactory(**kwargs))
        return task

    return build_task


@pytest.fixture
async def task(task_factory, user_active) -> Task:
    yield await task_factory(user_id=user_active.id)


@pytest.fixture
async def tasks_generating(task_factory, user_active) -> Callable:
    async def _build(n: int, **kwargs) -> list[Task]:
        tasks = [(await task_factory(user_id=user_active.id, **kwargs)) for _ in range(n)]
        return tasks

    return _build
