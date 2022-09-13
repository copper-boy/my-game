HELP_TEXT = """
Available commands (description - all commands will be sent 
in lowercase letters, no special char`s):
```
========================HELPERS========================
/about - shows what this bot can do
/help - shows a list of commands with their description
========================HELPERS========================

=========================CHATS=========================
/games - shows a list of all games
/select_game [game_name] - set a chat game
/begin - starts the selected game for users
/end - stops the current game and deletes the results for users
=========================CHATS=========================

========================PLAYERS========================
/join - connects to the game in the chat
/exit - exits the game in chat
========================PLAYERS========================

========================ACTIONS========================
/select_theme [theme_name]|[cost] - the user selects a theme for a reply
/answer [text] - text to answer the current theme
========================ACTIONS========================
``` 
"""

PARSE_MODE = 'Markdown'


async def help_command_handler(bot: Bot) -> None:
    await bot.send_message(message=HELP_TEXT,
                           parse_mode=PARSE_MODE)
