from functools import lru_cache

from pydantic import BaseSettings


class AdminSettings(BaseSettings):
    INFINITY_ADMIN_TOKEN: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class DatabaseSettings(BaseSettings):
    API_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()
