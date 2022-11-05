from functools import wraps
from typing import Any, Awaitable


def object_not_exist(coro: Awaitable):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        from common import NotFoundException

        res: Any | None = await coro(*args, **kwargs)
        if res is None:
            params = (f"{name}={value}" for name, value in kwargs.items())
            raise NotFoundException(detail=f"Объект с параметрами: [{','.join(params)}] не найден")

        return res

    return wrapper
