from typing import Any, Callable


class handle_exceptions:
    def __init__(self, function: Callable) -> None:
        self.function = function

    async def __call__(self, *args, **kwargs) -> Any:
        try:
            return await self.function(*args, **kwargs)
        except Exception:
            bot = kwargs.get('bot')
            callback, message = kwargs.get('callback'), kwargs.get('message')

            if callback:
                username = callback.message_from.username
                chat_id: str = callback.message.chat.id
            else:
                username = message.message_from.username
                chat_id: str = message.chat.id

            await bot.send_message(message=bot.message_helper.bad_message(username=username),
                                   chat_id=chat_id)

            raise
