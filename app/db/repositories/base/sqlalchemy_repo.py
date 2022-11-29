import abc
from typing import Any, Generic, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Table, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from api.dependencies.db import get_db_session
from db.models import Base

MODEL = TypeVar("Model", bound=Base)
TABLE = TypeVar("Table", bound=Table)


class SqlAlchemyRepo(Generic[MODEL, TABLE], abc.ABC):
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self._session = session

    @property
    @abc.abstractmethod
    def model(self) -> Type[MODEL] | TABLE:
        ...

    @property
    @abc.abstractmethod
    def column(self) -> Type[MODEL]:
        ...

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def create(self, object_: BaseModel) -> MODEL | TABLE:
        created_obj: MODEL = self.model(**object_.dict())
        self.session.add(created_obj)
        await self.session.flush()
        return created_obj

    async def update(self, filter_params: dict[str, Any], update_values: dict[str, Any]):
        fs: list = self.build_filters(filter_params)
        query = update(self.model).where(*fs).values(**update_values)
        await self.session.execute(query)

    async def delete(self, **params):
        fs: list[BinaryExpression] = self.build_filters(params)
        await self.session.execute(delete(self.model).filter(*fs))

    async def filters(self, limit: int | None = None, offset: int | None = None, **params) -> list[MODEL | TABLE]:
        fs: list = self.build_filters(params)
        res = await self.session.scalars(select(self.model).filter(*fs).limit(limit).offset(offset))
        return res.all()

    async def get_object(self, **params) -> MODEL | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.scalars(select(self.model).filter(*fs))
        return result.first()

    async def count(self, field="id") -> int:
        result = await self.session.scalars(count(getattr(self.column, field)))
        return result.first()

    async def bulk_insert(self, insert_data: list[dict[str, Any]]) -> int:
        result = await self.session.execute(insert(self.model).values(insert_data))
        return result.rowcount

    def build_filters(self, filter_params: dict[str, Any]) -> list[BinaryExpression]:
        return [getattr(self.model, filter_name) == filter_value for filter_name, filter_value in filter_params.items()]
