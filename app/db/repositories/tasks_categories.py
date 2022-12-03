from typing import Any

from sqlalchemy import Table, insert
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from db.models import TaskCategory
from db.repositories.base import SessionRepository


class TasksCategoryRepository(SessionRepository):
    @property
    def model(self) -> Table:
        return TaskCategory

    async def filters(self, limit: int | None = None, offset: int | None = None, **params) -> list[tuple[int, ...]]:
        res = await self.session.execute(
            select(self.model).filter(*self.build_filters(params)).limit(limit).offset(offset)
        )
        return res.all()

    async def bulk_insert(self, insert_data: list[dict[str, Any]]) -> int:
        result = await self.session.execute(insert(self.model).values(insert_data))
        return result.rowcount

    async def count(self, field="id") -> int:
        result = await self.session.scalars(count(getattr(self.model.c, field)))
        return result.first()

    async def create(self, data: dict[str, Any]) -> None:
        await self.session.execute(self.model.insert(), [data])

    def build_filters(self, filter_params: dict[str, Any]) -> list[BinaryExpression]:
        return [
            getattr(self.model.c, filter_name) == filter_value for filter_name, filter_value in filter_params.items()
        ]
