import abc
from typing import Generic, Type, TypeVar

from db.models import Base

MODEL = TypeVar("Table", bound=Base)


class BaseRepository(Generic[MODEL], abc.ABC):
    @property
    @abc.abstractmethod
    def model(self) -> Type[MODEL]:
        ...
