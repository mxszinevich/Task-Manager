from typing import Any

from config.settings import BaseSettings
from pydantic import validator


class AppSettings(BaseSettings):
    name: str = "Task manager"
    api_ver: str = "1.0.0"
    docs_url: str = "/docs"
    description: str = "API Менеджера задач"
    token_expires_min: int = 60 * 24
    token_secret_key: str | None
    token_algorithm: str = "HS256"

    @validator("token_secret_key")
    def build_token(cls, value: str | None, values: dict[str, Any]) -> str:
        if value is None:
            value = values["name"]
        return value
