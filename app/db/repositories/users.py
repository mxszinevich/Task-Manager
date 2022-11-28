from typing import Type

from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from common.token import get_password_hash
from db.models import User
from db.repositories.base import BaseRepository, SqlAlchemyRepo


class UsersRepository(SqlAlchemyRepo, BaseRepository):
    @property
    def model(self) -> Type[User]:
        return User

    async def create(self, user: BaseModel) -> User:
        user = user.copy(update={"password": get_password_hash(user.password)})
        return await super().create(user)

    async def user_info(self, user_id: int):
        result = await self.session.scalars(
            select(self.model).where(self.model.id == user_id).options(selectinload(self.model.tasks))
        )

        return result.first()
