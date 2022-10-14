from app.integration.api import get_game
from app.keyboard import get_join_exit_keyboard
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction

GAME_TEXT = """
Game has been created!
"""


@handle_exceptions
@transaction
async def game_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)

    if game_state.state != GameStateEnum.WAIT_FOR_SELECT_GAME:
        raise RuntimeError

    (_, game_id) = callback.data.split('-')

    game = await get_game(client=bot.app.store.aiohttp_session_accessor.aiohttp_session, game_id=game_id)

    if game is None:
        raise RuntimeError

    await bot.app.store.sessions.update_session(sql_session=sql_session,
                                                session_id=session.id,
                                                game_id=game_id)

    await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                      game_state_id=game_state.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYERS)

    await bot.send_message(message='Game has been created!',
                           chat_id=callback.message.chat.id,
                           reply_markup=get_join_exit_keyboard())
