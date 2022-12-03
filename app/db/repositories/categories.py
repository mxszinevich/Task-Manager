from typing import Type

from db.models import Category
from db.repositories.base import SqlAlchemyRepo


class CategoriesRepository(SqlAlchemyRepo[Category]):
    @property
    def model(self) -> Type[Category]:
        return Category
