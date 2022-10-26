from app.schemas.message import MessageSchema

HELP_TEXT = """
Available commands (description - all commands will be sent 
in lowercase letters, no special char`s):

/about - shows what this bot can do
/help - shows a list of commands with their description

/start - creates a game session

/games - shows game list

/begin - starts the game
/end - delete game session available only to admins

/done - shows the answer to the question if all players answered incorrectly

/answer - [text] the player answers the question
"""


async def help_command_handler(bot, message: MessageSchema) -> None:
    return await bot.send_message(message=HELP_TEXT, chat_id=message.chat.id)
