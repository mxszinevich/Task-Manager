"""isort:skip_file"""
from .base import BaseSettings
from .app_settings import AppSettings
from .db_settings import PostgresSettings


class Settings(BaseSettings):
    db: "PostgresSettings" = PostgresSettings()
    app: "AppSettings" = AppSettings()


settings = Settings()
