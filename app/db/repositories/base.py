import abc
from typing import Any, Generic, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression

from api.dependencies import get_db_session
from common import object_not_exist
from shemas import OrmBaseModel

MODEL = TypeVar("Table")
OUT_SCHEMA = TypeVar("OutShema", bound=OrmBaseModel)


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

    async def filters(self, **params) -> list[MODEL]:
        fs: list = self.build_filters(params)
        print(type(fs[0]))

        res = await self.session.execute(self.model).filter(*fs)
        return res.all()

    @object_not_exist
    async def get_object(self, **params) -> MODEL | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.scalars(select(self.model).filter(*fs))
        return result.first()

    def build_filters(self, filter_params: dict[str, Any]) -> list[BinaryExpression]:
        return [getattr(self.model, filter_name) == filter_value for filter_name, filter_value in filter_params.items()]
