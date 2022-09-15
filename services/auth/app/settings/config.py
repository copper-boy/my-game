from functools import lru_cache

from pydantic import BaseModel, BaseSettings


class AdminInfinityTokenSettings(BaseSettings):
    INFINITY_ADMIN_TOKEN: str


@lru_cache()
def get_admin_infinity_token_settings() -> AdminInfinityTokenSettings:
    return AdminInfinityTokenSettings()


class AdminSettings(BaseSettings):
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str


@lru_cache()
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


class DatabaseSettings(BaseSettings):
    AUTH_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class JWTSettingsSchema(BaseModel):
    authjwt_secret_key: str = get_jwt_settings().JWT_SECRET_KEY
