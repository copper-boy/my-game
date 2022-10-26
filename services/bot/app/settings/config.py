from functools import lru_cache

from pydantic import BaseSettings


class AMQPSettings(BaseSettings):
    AMQP_URI: str


@lru_cache()
def get_amqp_settings() -> AMQPSettings:
    return AMQPSettings()


class TelegramBotSettings(BaseSettings):
    TELEGRAM_BOT_API_TOKEN: str


@lru_cache()
def get_telegram_bot_settings() -> TelegramBotSettings:
    return TelegramBotSettings()
