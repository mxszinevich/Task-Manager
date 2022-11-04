from common import BadRequestException, NotFoundException
from common.token import get_password_hash
from db.models import User
from db.repositories.base import BaseRepository
from pydantic import BaseModel


class UsersRepository(BaseRepository):
    @property
    def model(self) -> User:
        return User

    async def create(self, user: BaseModel):
        user = user.copy(update={"password": get_password_hash(user.password)})
        try:
            await self.get_object(email=user.email)
        except NotFoundException:
            pass
        else:
            raise BadRequestException(detail="Пользователь с таким email уже существует")
        await super().create(user)
