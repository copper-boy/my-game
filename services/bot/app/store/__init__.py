from settings.config import get_telegram_bot_settings


class Store:
    def __init__(self):
        from .telegram_api.accessor import TelegramAccessor

        self.telegram_api = TelegramAccessor(get_telegram_bot_settings().TELEGRAM_BOT_API_TOKEN)
