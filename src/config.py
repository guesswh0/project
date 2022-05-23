from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'project'
    api_route: str = '/api'
    origins: list[str] = ["*"]

    # dev purpose
    db_url: str = 'sqlite:///./db.sqlite3'


@lru_cache()
def get_settings():
    return Settings()
