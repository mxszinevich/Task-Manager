from typing import Callable

from pydantic import BaseModel, Field
import pytest

from db.models import Category
from db.repositories.categories import CategoriesRepository
from tests.conftest import faker


class CategoryFactory(BaseModel):
    name: str = Field(default_factory=faker.word)


@pytest.fixture()
def category_factory(override_get_db_session) -> Callable:
    async def _build_category(**kwargs) -> Category:
        async for session in override_get_db_session():
            categories_repo = CategoriesRepository(session=session)
            category = await categories_repo.create(CategoryFactory(**kwargs))
            await session.commit()
            return category

    return _build_category


@pytest.fixture()
async def category(category_factory) -> Category:
    yield await category_factory()


@pytest.fixture
async def categories_generating(category_factory, user_active) -> Callable:
    async def _build(n: int = 1, **kwargs) -> list[Category]:
        return [(await category_factory(**kwargs)) for _ in range(n)]

    return _build
