from functools import lru_cache

from pydantic import BaseSettings


class AuthSiteSettings(BaseSettings):
    AUTH_SITE_BASE_URL: str


@lru_cache()
def get_auth_site_settings() -> AuthSiteSettings:
    return AuthSiteSettings()


class DatabaseSettings(BaseSettings):
    LOGIC_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()
