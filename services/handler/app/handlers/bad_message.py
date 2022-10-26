from app.schemas.message import CallbackSchema, MessageSchema

BAD_MESSAGE_COMMAND_TEXT = """
I have not support this command yet!
"""

BAD_MESSAGE_CALLBACK_TEXT = """
I have not support this button yet.
"""


async def bad_message_command_handler(bot, message: MessageSchema) -> None:
    await bot.send_message(message=BAD_MESSAGE_COMMAND_TEXT, chat_id=message.chat.id)


async def bad_message_callback_handler(bot, callback: CallbackSchema) -> None:
    await bot.send_message(message=BAD_MESSAGE_CALLBACK_TEXT, chat_id=callback.message.chat.id)
