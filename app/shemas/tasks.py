from pydantic import validator

from db.constants import StatusType
from shemas import CategoryDetail, OrmBaseModel
from shemas.validators.datetime_format import datetime_formatting


class BaseTask(OrmBaseModel):
    name: str
    body: str | None


class TaskCreateIn(BaseTask):
    ...


class TaskCreateOut(BaseTask):
    id: int
    user_id: int
    status: StatusType


class TaskDetail(BaseTask):
    id: int
    user_id: int
    status: StatusType
    completion_date: str | None
    created: str
    categories: list[CategoryDetail]

    _valid_date = validator("created", "completion_date", check_fields=False, allow_reuse=True, pre=True)(
        datetime_formatting
    )


class TaskUpdate(OrmBaseModel):
    name: str | None
    body: str | None
    status: StatusType | None
