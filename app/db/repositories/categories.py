from typing import Type

from db.models import Category
from db.repositories.base import BaseRepository, SqlAlchemyRepo


class CategoriesRepository(SqlAlchemyRepo, BaseRepository):
    @property
    def model(self) -> Type[Category]:
        return Category
