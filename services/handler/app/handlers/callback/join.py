from app.keyboard import GAME_KEYBOARD
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.session import transaction

JOIN_TEXT = """
@{} join the game!
"""


@transaction
async def join_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)
    if session is None:
        return await bot.send_message(message=bot.message_helper.bad_message(username=callback.message_from.username),
                                      chat_id=callback.message.chat.id)

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)
    if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
        return await bot.send_message(message=bot.message_helper.bad_message(username=callback.message_from.username),
                                      chat_id=callback.message.chat.id)

    if await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                             session_id=session.id,
                                                             telegram_id=callback.message_from.id):
        return await bot.send_message(message=bot.message_helper.bad_message(username=callback.message_from.username),
                                      chat_id=callback.message.chat.id)

    await bot.app.store.players.create_player(sql_session=sql_session,
                                              telegram_id=callback.message_from.id, session=session)

    await bot.send_sticker(sticker='CAACAgIAAx0CaNrB4wACAfFjIgMZ8-CBGhmDK5oOW29QhLNjeQACMRUAArUauEiQLLLFAAFAlegpBA',
                           chat_id=callback.message.chat.id)

    formatted_text = JOIN_TEXT.format(callback.message_from.username)
    await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id, reply_markup=GAME_KEYBOARD)
