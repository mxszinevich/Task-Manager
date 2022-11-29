from typing import Type

from db.repositories.base import SqlAlchemyRepo
from db.repositories.base.sqlalchemy_repo import MODEL


class BaseModelRepository(SqlAlchemyRepo):
    @property
    def column(self) -> Type[MODEL]:
        return self.model
