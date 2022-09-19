from app.keyboard import get_join_exit_keyboard
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction


@handle_exceptions
@transaction
async def join_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)
    if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
        raise RuntimeError

    if await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                             session_id=session.id,
                                                             telegram_id=callback.message_from.id):
        raise RuntimeError

    await bot.app.store.players.create_player(sql_session=sql_session,
                                              telegram_id=callback.message_from.id, session=session)

    await bot.send_sticker(sticker='CAACAgIAAx0CaNrB4wACAfFjIgMZ8-CBGhmDK5oOW29QhLNjeQACMRUAArUauEiQLLLFAAFAlegpBA',
                           chat_id=callback.message.chat.id)

    await bot.send_message(message=f'@{callback.message_from.username} join the game!',
                           chat_id=callback.message.chat.id,
                           reply_markup=get_join_exit_keyboard())
