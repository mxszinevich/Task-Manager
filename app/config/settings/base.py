from pydantic import BaseSettings as _BaseSettings


class BaseSettings(_BaseSettings):
    class Config:
        env_file = "../.env"
