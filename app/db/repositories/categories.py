from typing import Type

from db.models import Category
from db.repositories.base import BaseRepository


class CategoriesRepository(BaseRepository):
    @property
    def model(self) -> Type[Category]:
        return Category
