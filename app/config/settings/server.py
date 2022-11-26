from config.settings import BaseSettings


class ServerSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8000

    class Config:
        env_prefix = "server_"
