import os
from typing import List
from pydantic import BaseSettings, Field, PostgresDsn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    app_title: str = "ShorterLinks API"
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")
    db_dsn: PostgresDsn = Field(..., env="DATABASE_DSN")
    black_list: List[str] = [
        # "127.0.0.1"
    ]

    @property
    def app_prefix(self):
        return f"{self.app_host}:{self.app_port}/api/"

    class Config:
        env_file = '.env.example'


config = AppConfig()
