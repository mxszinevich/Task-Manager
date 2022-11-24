from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.sql.functions import count

from common.token import get_password_hash
from db.models import Task, User
from db.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    @property
    def model(self) -> User:
        return User

    async def create(self, user: BaseModel) -> User:
        user = user.copy(update={"password": get_password_hash(user.password)})
        return await super().create(user)

    async def user_info(self, user_id: int):
        subq = select(
            count(Task.id).filter(and_(Task.active.is_(True).label("task_count"), Task.user_id == user_id))
        ).scalar_subquery()
        result = await self.session.execute(
            select(
                self.model,
                subq.label("task_count"),
            ).where(self.model.id == user_id)
        )
        return result.fetchone()
