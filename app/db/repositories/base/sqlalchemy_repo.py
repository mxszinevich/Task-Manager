import abc
from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import count

from db.models import Base
from db.repositories.base import SessionRepository
from db.repositories.utils import SqlHelperMixin

MODEL = TypeVar("Model", bound=Base)


class SqlAlchemyRepo(Generic[MODEL], SqlHelperMixin, SessionRepository, abc.ABC):
    @property
    @abc.abstractmethod
    def model(self) -> Type[MODEL]:
        ...

    async def create(self, object_: BaseModel) -> MODEL:
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

    async def filters(self, limit: int | None = None, offset: int | None = None, **params) -> list[MODEL]:
        fs: list = self.build_filters(params)
        res = await self.session.scalars(select(self.model).filter(*fs).limit(limit).offset(offset))
        return res.all()

    async def get_object(self, **params) -> MODEL | None:
        fs: list[BinaryExpression] = self.build_filters(params)
        result = await self.session.scalars(select(self.model).filter(*fs))
        return result.first()

    async def count(self, field="id") -> int:
        result = await self.session.scalars(count(getattr(self.model, field)))
        return result.first()
