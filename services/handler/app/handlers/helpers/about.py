ABOUT_TEXT = """
Hello! I am a bot that implements **Svoya igra** in a telegram chat.
At the moment, all the functionality of the game has not been implemented, 
but you can support my project, creator - copper_boy.t.me
"""

PARSE_MODE = 'Markdown'


async def about_command_handler(bot: Bot) -> None:
    await bot.send_message(message=ABOUT_TEXT,
                           parse_mode=PARSE_MODE)
