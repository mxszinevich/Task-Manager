from fastapi import Query
from pydantic import BaseModel

from db.constants import StatusType


class TaskListQuery(BaseModel):
    status: int | None = Query(
        None, description="Статус задачи", gt=StatusType.CREATED.value - 1, le=StatusType.EXPIRED.value + 1
    )
