from aiohttp import ClientSession

from app.authed_client import set_auth_session

JOIN_TEXT = """
@{} join the game.
"""


async def join_command_handler(bot, message):
    async with ClientSession() as session:
        await set_auth_session(session)

        async with session.get(url='http://logic_service:14961/api/v1/logic/get/session',
                               params={
                                   'chat_id': message.chat.id
                               }) as get_session_response:
            if get_session_response.status == 404:
                return await bot.send_message(message='Not game selected yet!', chat_id=message.chat.id)
            get_session_json = await get_session_response.json()

            if get_session_json['is_started']:
                return await bot.send_message(message=f'Player @{message.message_from.username} is trying to '
                                                      f'join the game that has started. Rejected, noob.',
                                              chat_id=message.chat.id)

        async with session.post(url='http://logic_service:14961/api/v1/logic/create/player',
                                params={
                                    'chat_id': message.chat.id,
                                    'player_id': message.message_from.id
                                }) as create_player_response:
            if create_player_response.status == 409:
                return await bot.send_message(message='Already in game!', chat_id=message.chat.id)

    await bot.send_sticker(sticker='CAACAgIAAx0CaNrB4wACAfFjIgMZ8-CBGhmDK5oOW29QhLNjeQACMRUAArUauEiQLLLFAAFAlegpBA',
                           chat_id=message.chat.id)
    formatted_text = JOIN_TEXT.format(message.message_from.username)
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)
