from functools import lru_cache

from pydantic import BaseModel, BaseSettings


class AdminSettings(BaseSettings):
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class AMQPSettings(BaseSettings):
    AMQP_URI: str


@lru_cache()
def get_amqp_settings() -> AMQPSettings:
    return AMQPSettings()


class JWTSettings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str


@lru_cache()
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


class DatabaseSettings(BaseSettings):
    AUTH_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class JWTSettingsSchema(BaseModel):
    authjwt_algorithm: str = get_jwt_settings().JWT_ALGORITHM
    authjwt_public_key: str = get_jwt_settings().JWT_PUBLIC_KEY
    authjwt_private_key: str = get_jwt_settings().JWT_PRIVATE_KEY

