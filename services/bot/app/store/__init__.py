from app.settings.config import get_telegram_bot_settings


class Store:
    def __init__(self) -> None:
        from .botq.accessor import BotQAccessor
        from .telegram_api.accessor import TelegramAccessor

        self.telegram_api = TelegramAccessor(get_telegram_bot_settings().TELEGRAM_BOT_API_TOKEN)
        self.botq = BotQAccessor()

    async def setup(self) -> None:
        await self.botq.setup()
