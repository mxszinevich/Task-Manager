from pydantic import RedisDsn, validator

from config.settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: str = "6379"
    dsn: str | None

    @validator("dsn", pre=True)
    def dsn_build(cls, value: str | None, values: dict[str, int]) -> str:
        if isinstance(value, str):
            return value

        return RedisDsn.build(scheme="redis", host=values["host"], port=values["port"], path="/0")

    class Config:
        env_prefix = "redis_"
