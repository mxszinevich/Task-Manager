from fastapi import Query
from pydantic import BaseModel


class TaskListQuery(BaseModel):
    active: bool | None = Query(None, description="Статус задачи")
