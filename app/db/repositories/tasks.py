from asyncio import gather
from typing import Type

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from common.aggregate import BaseAggregate
from db.models import Category, Task, TaskCategory
from db.repositories.base import BaseRepository, SqlAlchemyRepo


class StatusAggregate(BaseAggregate):
    async def filter(self) -> dict[str, str | int]:
        filters = await self.session.execute(
            select(getattr(self.model, self.field), count(self.model.id))
            .group_by(getattr(self.model, self.field))
            .where(getattr(self.model, self.field).is_not(None))
        )
        return {self.field: [{"value": f, "label": f.display, "count": count} for f, count in filters.all()]}


class CategoriesAggregate(BaseAggregate):
    async def filter(self) -> dict[str, str | int]:
        join_subq = (
            select(TaskCategory.c.category_id, count(TaskCategory.c.task_id))
            .group_by(TaskCategory.c.category_id)
            .subquery("tasks_cats")
        )
        filters = await self.session.execute(
            select(join_subq.c.category_id, Category.name, join_subq.c.count).join(join_subq)
        )
        return {self.field: [{"value": id_, "label": name, "count": count} for id_, name, count in filters.all()]}


class TasksRepository(SqlAlchemyRepo, BaseRepository):
    status = StatusAggregate()
    categories = CategoriesAggregate()

    @property
    def model(self) -> Type[Task]:
        return Task

    async def get_filters(self) -> dict:
        return await gather(self.categories(), self.status())

    async def get_task_full_data(self, **params) -> Task | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.execute(select(self.model).where(*fs).options(selectinload(self.model.categories)))
        return result.scalars().first()
