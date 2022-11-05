from fastapi import Query
from pydantic import BaseModel


class UsersListFilter(BaseModel):
    name: str | None = Query(None, description="Имя пользователя")
    limit: int | None = Query(None)
    offset: int | None = Query(None)
    is_active: bool | None = Query(None, description="Статус")
