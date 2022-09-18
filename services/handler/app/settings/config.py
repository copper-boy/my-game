from functools import lru_cache

from pydantic import BaseSettings


class AMQPSettings(BaseSettings):
    AMQP_URI: str


@lru_cache()
def get_amqp_settings() -> AMQPSettings:
    return AMQPSettings()


class AdminSettings(BaseSettings):
    INFINITY_ADMIN_TOKEN: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class ApiSiteSettings(BaseSettings):
    API_SITE_BASE_URL: str


@lru_cache()
def get_api_site_settings() -> ApiSiteSettings:
    return ApiSiteSettings()


class DatabaseSettings(BaseSettings):
    HANDLER_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class TelegramBotSettings(BaseSettings):
    TELEGRAM_BOT_API_TOKEN: str


@lru_cache()
def get_telegram_bot_settings() -> TelegramBotSettings:
    return TelegramBotSettings()
