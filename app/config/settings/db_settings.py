from typing import Any

from pydantic import PostgresDsn, validator

from config.settings import BaseSettings


class PostgresSettings(BaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    dsn: str | None
    echo: bool = True

    @validator("dsn", pre=True)
    def dsn_build(cls, value: str | None, values: dict[str, Any]) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme=values["scheme"],
            host=values["host"],
            port=values["port"],
            user=values["user"],
            password=values["password"],
            path=f"/{values['db']}",
        )

    class Config:
        env_prefix = "postgres_"
