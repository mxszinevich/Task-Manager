from pydantic import BaseModel

from common import BadRequestException
from common.token import get_password_hash
from db.models import User
from db.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    @property
    def model(self) -> User:
        return User

    async def create(self, user: BaseModel):
        user = user.copy(update={"password": get_password_hash(user.password)})
        user_check = await self.get_object(email=user.email)
        if user_check is not None:
            raise BadRequestException(detail="Пользователь с таким email уже существует")
        await super().create(user)
