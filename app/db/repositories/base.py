import abc
from typing import Any, Generic, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from api.dependencies.db import get_db_session

MODEL = TypeVar("Table")


class BaseRepository(Generic[MODEL], abc.ABC):
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    @abc.abstractmethod
    def model(self) -> Type[MODEL]:
        ...

    async def create(self, object: BaseModel):
        self.session.add(self.model(**object.dict()))

    async def delete(self, obj_id: int):
        await self.session.execute(delete(self.model).filter(self.model.id == obj_id))

    async def filters(self, limit: int | None = None, offset: int | None = None, **params) -> list[MODEL]:
        fs: list = self.build_filters(params)
        res = await self.session.scalars(select(self.model).filter(*fs).limit(limit).offset(offset))
        return res.all()

    async def get_object(self, **params) -> MODEL | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.scalars(select(self.model).filter(*fs))
        return result.first()

    async def count(self) -> int:
        result = await self.session.scalars(count(self.model.id))
        return result.first()

    def build_filters(self, filter_params: dict[str, Any]) -> list[BinaryExpression]:
        return [getattr(self.model, filter_name) == filter_value for filter_name, filter_value in filter_params.items()]
