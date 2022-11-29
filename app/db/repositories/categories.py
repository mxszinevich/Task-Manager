from typing import Type

from db.models import Category
from db.repositories.base import BaseModelRepository


class CategoriesRepository(BaseModelRepository):
    @property
    def model(self) -> Type[Category]:
        return Category
