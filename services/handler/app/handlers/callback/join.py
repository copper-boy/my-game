from app.keyboard import GAME_KEYBOARD
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema

JOIN_TEXT = """
@{} join the game!
"""

BAD_JOIN_TEXT = """
@{} refused to connect to the game!
"""


async def join_callback_handler(bot, callback: CallbackSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=callback.message.chat.id)
    if session is None:
        formatted_text = BAD_JOIN_TEXT.format(callback.message_from.username)
        return await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id)

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)
    if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
        formatted_text = BAD_JOIN_TEXT.format(callback.message_from.username)
        return await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id)

    if await bot.app.store.players.get_player_by_telegram_id(session_id=session.id,
                                                             telegram_id=callback.message_from.id):
        formatted_text = BAD_JOIN_TEXT.format(callback.message_from.username)
        return await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id)

    await bot.app.store.players.create_player(telegram_id=callback.message_from.id, session=session)

    await bot.send_sticker(sticker='CAACAgIAAx0CaNrB4wACAfFjIgMZ8-CBGhmDK5oOW29QhLNjeQACMRUAArUauEiQLLLFAAFAlegpBA',
                           chat_id=callback.message.chat.id)

    formatted_text = JOIN_TEXT.format(callback.message_from.username)
    await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id, reply_markup=GAME_KEYBOARD)
