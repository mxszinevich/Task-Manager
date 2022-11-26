from typing import Type

from sqlalchemy.engine import Row
from sqlalchemy.future import select
from sqlalchemy.sql.functions import count

from db.models import Task
from db.repositories.base import BaseRepository


class TasksRepository(BaseRepository):
    @property
    def model(self) -> Type[Task]:
        return Task

    async def get_filters(self) -> dict:
        status_subq = (
            select(self.model.status, count(self.model.id))
            .group_by(self.model.status)
            .where(self.model.status.is_not(None))
        )
        row_filters: list[Row] = await self.session.execute(status_subq)
        return {"status": [{"value": st, "label": st.display, "count": count} for st, count in row_filters.all()]}
