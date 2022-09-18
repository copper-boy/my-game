from app.schemas.message import MessageSchema

HELP_TEXT = """
Available commands (description - all commands will be sent 
in lowercase letters, no special char`s):

/about - shows what this bot can do
/help - shows a list of commands with their description

/begin - starts the game

/games - shows game list

/answer - [text] the player answers the question
"""


async def help_command_handler(bot, message: MessageSchema) -> None:
    return await bot.send_message(message=HELP_TEXT, chat_id=message.chat.id)
