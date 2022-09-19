from app.integration.api import get_game
from app.keyboard import GAME_KEYBOARD
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.session import transaction

GAME_TEXT = """
Game has been created!
"""


@transaction
async def game_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)

    if session:
        game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                                  session_id=session.id)
        if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
            return await bot.send_message(message='The game has already started!', chat_id=callback.message.chat.id)
    else:
        session = await bot.app.store.sessions.create_session(sql_session=sql_session,
                                                              chat_id=callback.message.chat.id)
        game_state = await bot.app.store.game_states.create_game_state(sql_session=sql_session,
                                                                       session=session)

    (_, game_id) = callback.data.split('-')
    game = await get_game(client=bot.app.store.aiohttp_session_accessor.aiohttp_session, game_id=int(game_id))

    if game is None:
        return await bot.send_message(message=f'@{callback.message_from.username} game not found on server',
                                      chat_id=callback.message.chat.id)

    await bot.app.store.sessions.update_session(sql_session=sql_session,
                                                session_id=session.id, game_id=int(game_id))
    await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                      game_state_id=game_state.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYERS)

    await bot.send_message(message=GAME_TEXT, chat_id=callback.message.chat.id, reply_markup=GAME_KEYBOARD)
