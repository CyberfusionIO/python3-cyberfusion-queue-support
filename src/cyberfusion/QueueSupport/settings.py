from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_path: Path = Path("queue-support.db")

    class Config:
        env_prefix = "queue_support_"

        env_file = ".env", "/etc/queue-support.conf"


settings = Settings()
