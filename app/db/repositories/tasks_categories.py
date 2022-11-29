from sqlalchemy import Table

from db.models import TaskCategory
from db.repositories.base.base_table_repo import BaseTableRepository


class TasksCategoryRepository(BaseTableRepository):
    @property
    def model(self) -> Table:
        return TaskCategory
