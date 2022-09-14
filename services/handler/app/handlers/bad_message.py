from typing import TYPE_CHECKING

from app.schemas.message import MessageSuperGroupSchema

if TYPE_CHECKING:
    from app.bot import Bot

BAD_MESSAGE_TEXT = """
I have not support commands in this chat yet!
"""


async def bad_message_handler(bot: 'Bot', chat_id: int | None = None,
                              message: MessageSuperGroupSchema | None = None) -> None:
    await bot.send_message(message=BAD_MESSAGE_TEXT, chat_id=message.chat.id if message else chat_id)
