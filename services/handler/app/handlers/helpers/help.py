from typing import TYPE_CHECKING

from app.schemas.message import MessageSuperGroupSchema

if TYPE_CHECKING:
    from app.bot import Bot

HELP_TEXT = """
Available commands (description - all commands will be sent 
in lowercase letters, no special char`s):

/about - shows what this bot can do
/help - shows a list of commands with their description

/games - shows a list of all games
/select_game [game_name] - set a chat game
/begin - starts the selected game for users
/end - stops the current game and deletes the results for users

/join - connects to the game in the chat
/exit - exits the game in chat

/select_theme [theme_name]|[cost] - the user selects a theme for a reply
/answer [text] - text to answer the current theme
"""


async def help_command_handler(bot: 'Bot', message: MessageSuperGroupSchema) -> None:
    await bot.send_message(message=HELP_TEXT,
                           chat_id=message.chat.id)
