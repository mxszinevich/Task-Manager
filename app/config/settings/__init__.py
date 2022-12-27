"""isort:skip_file"""
from .base import BaseSettings
from .app import AppSettings
from .db import PostgresSettings
from .server import ServerSettings
from .redis import RedisSettings


class Settings(BaseSettings):
    db: PostgresSettings = PostgresSettings()
    app: AppSettings = AppSettings()
    server: ServerSettings = ServerSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
