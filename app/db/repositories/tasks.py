from asyncio import gather
from datetime import datetime
from typing import Type

from sqlalchemy import and_, update
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute, selectinload
from sqlalchemy.sql import Selectable
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from common.aggregate import BaseAggregate, BaseFilterAggregate
from db.constants import StatusType
from db.models import Category, Task, TaskCategory
from db.repositories.base import SqlAlchemyRepo


class StatusAggregate(BaseFilterAggregate):
    """Агрегация статусов с группировкой по кол-ву задач"""

    async def filter(self, **params) -> dict[str, str | int]:
        extra_model_filters: list[BinaryExpression] = self.build_filters(params)
        field: InstrumentedAttribute = getattr(self.model, self.field)
        filters = await self.session.execute(
            select(field, count(self.model.id))
            .where(field.is_not(None), *extra_model_filters)
            .group_by(field)
            .order_by(field)
        )
        return {self.field: [{"value": f, "label": f.display, "count": c} for f, c in filters.all()]}


class CategoriesAggregate(BaseAggregate):
    """Агрегация категорий с группировкой по кол-во задач"""

    def filter_query(self, extra_model_filters: list[BinaryExpression]) -> Selectable:
        query = (
            select(Category.id, Category.name, count(TaskCategory.c.task_id))
            .select_from(Category)
            .join(TaskCategory)
            .join(self.model)
            .where(*extra_model_filters)
            .group_by(Category.id)
            .order_by(Category.id)
        )
        return query


class TasksRepository(SqlAlchemyRepo[Task]):
    status = StatusAggregate()
    categories = CategoriesAggregate()

    @property
    def model(self) -> Type[Task]:
        return Task

    async def get_filters(self, **params) -> list[dict[str, str | int]]:
        return await gather(self.status(**params), self.categories(**params))

    async def get_task_full_data(self, **params) -> Task | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.execute(select(self.model).where(*fs).options(selectinload(self.model.categories)))
        return result.scalars().first()

    async def tasks_changing_status(self):
        await self.session.execute(
            update(Task)
            .where(
                and_(
                    datetime.today() > Task.completion_date,
                    Task.status.not_in([StatusType.COMPLETED, StatusType.EXPIRED]),
                    Task.completion_date.is_not(None),
                )
            )
            .values(status=StatusType.EXPIRED)
        )
        await self.session.commit()
