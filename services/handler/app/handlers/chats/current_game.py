from aiohttp import ClientSession

from app.authed_client import set_auth_session

CURRENT_GAME_TEXT = """
The current game is {}.
"""


async def current_game_command_handler(bot, message):
    async with ClientSession() as session:
        await set_auth_session(session)

        async with session.get(url='http://logic_service:14961/api/v1/logic/get/session',
                               params={
                                   'chat_id': message.chat.id
                               }) as get_session_response:
            if get_session_response.status != 200:
                return await bot.send_message(message='No game selected.', chat_id=message.chat.id)

            get_session_json = await get_session_response.json()

        async with session.get('http://logic_service:14961/api/v1/logic/get/game/by-id',
                               params={
                                   'game_id': get_session_json['game_id']
                               }) as get_game_response:
            get_game_json = await get_game_response.json()

    formatted_text = CURRENT_GAME_TEXT.format(get_game_json['name'])
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)

