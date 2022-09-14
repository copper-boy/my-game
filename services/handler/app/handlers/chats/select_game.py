from aiohttp import ClientSession

from app.authed_client import set_auth_session

from app.schemas.message import MessageSuperGroupSchema


SELECT_GAME_MESSAGE = """
For chat {} successfully selected game {}.
"""


async def update_session(session: ClientSession, chat_id: int, game_id: int) -> dict:
    async with session.put('http://logic_service:14961/api/v1/logic/update/session/game_id',
                           params={
                               'game_id': game_id,
                               'chat_id': chat_id
                           }) as update_session_response:
        update_session_json = await update_session_response.json()

    return update_session_json


async def select_game_command_handler(bot, message: MessageSuperGroupSchema):
    game_name = message.text.split(' ')[1].lower()
    async with ClientSession() as session:
        await set_auth_session(session)

        async with session.get('http://logic_service:14961/api/v1/logic/get/game/by-name',
                               params={
                                   'game_name': game_name
                               }) as get_game_response:
            if get_game_response.status == 404:
                return await bot.send_message(message='Game not found', chat_id=message.chat.id)

            get_game_json = await get_game_response.json()

        async with session.post(url='http://logic_service:14961/api/v1/logic/create/session',
                                params={
                                    'game_id': get_game_json['id'],
                                    'chat_id': message.chat.id
                                }) as create_session_response:
            if create_session_response.status != 200:
                await update_session(session=session, chat_id=message.chat.id, game_id=get_game_json['id'])

    formatted_text = SELECT_GAME_MESSAGE.format(message.chat.title, game_name)
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)
