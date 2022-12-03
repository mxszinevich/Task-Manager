from typing import Coroutine

from pydantic import BaseModel, Field
import pytest

from db.models import Category, Task
from db.repositories.tasks_categories import TasksCategoryRepository


class TaskCategoryFactory(BaseModel):
    task_id: int = Field(...)
    category_id: int = Field(...)


@pytest.fixture()
def task_category_factory(override_get_db_session) -> Coroutine:
    async def build_task_category(task_id: int, category_id: int) -> list[tuple[int, ...]]:
        async for session in override_get_db_session():
            task_cat_repo = TasksCategoryRepository(session=session)
            await task_cat_repo.create(TaskCategoryFactory(task_id=task_id, category_id=category_id).dict())
        return await task_cat_repo.filters(task_id=task_id, category_id=category_id)

    return build_task_category


@pytest.fixture()
async def task_category(task_category_factory: Coroutine, category: Category, task: Task):
    return await task_category_factory(task_id=task.id, category_id=category.id)
