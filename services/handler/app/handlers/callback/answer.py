from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction
from app.utils.player import is_player_cant_give_answer


@handle_exceptions
@transaction
async def answer_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                                   telegram_id=callback.message_from.id,
                                                                   session_id=session.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)
    if is_player_cant_give_answer(player=player,
                                  game_state=game_state,
                                  current_player=0):
        raise RuntimeError

    await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                      game_state_id=game_state.id,
                                                      current_question_id=game_state.current_question_id,
                                                      current_player=player.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)

    await bot.send_message(message=f'@{callback.message_from.username} waiting for your reply...',
                           chat_id=callback.message.chat.id)
