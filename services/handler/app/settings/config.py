from functools import lru_cache

from pydantic import BaseSettings


class AdminSettings(BaseSettings):
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class AuthSiteSettings(BaseSettings):
    AUTH_SITE_URL: str


@lru_cache()
def get_auth_site_settings() -> AuthSiteSettings:
    return AuthSiteSettings()
