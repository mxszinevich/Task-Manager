from .app_settings import AppSettings
from .base import BaseSettings
from .db_settings import PostgresSettings


class Settings(BaseSettings):
    db: PostgresSettings = PostgresSettings()
    app: AppSettings = AppSettings()


settings = Settings()
