from app.schemas.message import MessageSchema

ABOUT_TEXT = """
Hello! I am a bot that implements Svoya-Igra in a telegram chat.
At the moment, all the functionality of the game has not been implemented, 
but you can support my project, creator - copper_boy.t.me
"""


async def about_command_handler(bot, message: MessageSchema) -> None:
    await bot.send_message(message=ABOUT_TEXT, chat_id=message.chat.id)
