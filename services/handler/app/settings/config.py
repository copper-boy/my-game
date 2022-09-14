from functools import lru_cache

from pydantic import BaseSettings


class AMQPSettings(BaseSettings):
    AMQP_URI: str


@lru_cache()
def get_amqp_settings() -> AMQPSettings:
    return AMQPSettings()


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


class TelegramBotSettings(BaseSettings):
    TELEGRAM_BOT_ACCESS_TOKEN: str


@lru_cache()
def get_telegram_bot_settings() -> TelegramBotSettings:
    return TelegramBotSettings()
