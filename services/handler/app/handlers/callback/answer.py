from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema


async def answer_callback_handler(bot, callback: CallbackSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=callback.message.chat.id)
    if session is None:
        return await bot.send_message(message='No chat game!', chat_id=callback.message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(telegram_id=callback.message_from.id,
                                                                   session_id=session.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)

    if player is None or \
            player.is_answered or \
            game_state.state != GameStateEnum.WAIT_FOR_PLAYER_ANSWER or \
            game_state.current_player != 0:
        return await bot.send_message(message=f'@{callback.message_from.username} you can`t answer!',
                                      chat_id=callback.message.chat.id)

    await bot.app.store.game_states.update_game_state(game_state_id=game_state.id,
                                                      current_question_id=game_state.current_question_id,
                                                      current_player=player.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)
    await bot.send_message(message=f'@{callback.message_from.username} waiting for your reply',
                           chat_id=callback.message.chat.id)
