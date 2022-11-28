from sqlalchemy import Table

from db.models import TaskCategory
from db.repositories.base import SqlAlchemyRepo


class TasksCategoryRepository(SqlAlchemyRepo):
    @property
    def model(self) -> Table:
        return TaskCategory
