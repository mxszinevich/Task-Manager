import abc
from typing import Any


class BaseAggregate(abc.ABC):
    def __set_name__(self, owner, name):
        self.field: str = name

    def __get__(self, instance, owner):
        self.model = instance.model
        self.session = instance.session
        return self.filter

    @abc.abstractmethod
    async def filter(self) -> dict[str, Any]:
        ...
