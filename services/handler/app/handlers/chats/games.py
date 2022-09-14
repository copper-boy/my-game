from aiohttp import ClientSession
from app.authed_client import set_auth_session

GAMES_TEXT = """
Available games:

{}
"""


async def games_command_handler(bot, message):
    async with ClientSession() as session:
        await set_auth_session(session)

        async with session.get(url='http://logic_service:14961/api/v1/logic/get/games') as response:
            json = await response.json()
    game_names = '\n'.join(f'{i}. {game["name"]}' for i, game in enumerate(json, start=1))
    formatted_text = GAMES_TEXT.format(game_names)

    await bot.send_message(message=formatted_text, chat_id=message.chat.id)

