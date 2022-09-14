from aiohttp import ClientSession

from app.authed_client import set_auth_session

EXIT_TEXT = """
@{} left game.
"""


async def exit_command_handler(bot, message):
    async with ClientSession() as session:
        await set_auth_session(session)

        async with session.delete(url='http://logic_service:14961/api/v1/logic/delete/player',
                                  params={
                                      'chat_id': message.chat.id,
                                      'player_id': message.message_from.id
                                  }) as delete_player_response:
            if delete_player_response.status == 404:
                return await bot.send_message(message=f'The player @{message.message_from.username} not in game yet.')
    formatted_text = EXIT_TEXT.format(message.message_from.username)
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)
