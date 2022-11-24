from datetime import datetime

from pydantic import validator

from shemas import OrmBaseModel


class BaseTask(OrmBaseModel):
    name: str
    body: str | None


class TaskCreateIn(BaseTask):
    ...


class TaskCreateOut(BaseTask):
    id: int
    user_id: int


class TaskDetail(BaseTask):
    id: int
    user_id: int
    created: str
    active: bool

    @validator("created", pre=True)
    def created_formatting(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")


class TaskUpdate(OrmBaseModel):
    name: str | None
    body: str | None
    active: bool | None
