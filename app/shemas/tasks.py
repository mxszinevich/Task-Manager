from datetime import datetime

from fastapi import Body
from pydantic import validator

from db.constants import StatusType
from shemas import CategoryDetail, OrmBaseModel
from shemas.validators.datetime_format import datetime_formatting


class BaseTask(OrmBaseModel):
    name: str = Body(..., description="Название задачи")
    body: str | None = Body(None, description="Тело задачи")


class TaskCreateIn(BaseTask):
    completion_date: datetime | None = Body(None, description="Дата завершения")
    categories: list[int] = Body(default=[], description="Список категорий")


class TaskCreateOut(BaseTask):
    id: int
    user_id: int
    status: StatusType
    completion_date: datetime | None
    categories: list[CategoryDetail]


class TaskShortDetail(BaseTask):
    id: int
    user_id: int
    status: StatusType
    completion_date: str | None
    created: str

    _valid_date = validator("created", "completion_date", check_fields=False, allow_reuse=True, pre=True)(
        datetime_formatting
    )


class TaskDetail(TaskShortDetail):
    categories: list[CategoryDetail]


class TaskUpdate(OrmBaseModel):
    name: str | None
    body: str | None
    status: StatusType | None
