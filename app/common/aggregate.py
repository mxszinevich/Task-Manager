import abc
from typing import Any

from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.selectable import Selectable

from db.repositories.utils import SqlHelperMixin


class BaseAggregate(SqlHelperMixin, abc.ABC):
    def __set_name__(self, owner, name: str):
        self.field: str = name

    def __get__(self, instance, owner):
        self.model = instance.model
        self.session = instance.session
        return self.filter

    @abc.abstractmethod
    def filter_query(self, extra_model_filters: list[BinaryExpression]) -> Selectable:
        """Метод формирования select запроса"""
        ...

    async def filter(self, **params) -> dict[str, Any]:
        extra_model_filters: list[BinaryExpression] = self.build_filters(params)
        filters = await self.session.execute(self.filter_query(extra_model_filters))
        return {self.field: [{"value": value, "label": name, "count": count_} for value, name, count_ in filters.all()]}


class BaseFilterAggregate(BaseAggregate):
    def filter_query(self, *args, **kwargs) -> Selectable:
        ...

    @abc.abstractmethod
    async def filter(self, **params) -> dict[str, Any]:
        ...
