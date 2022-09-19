from app.keyboard import get_join_exit_keyboard
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction


@handle_exceptions
@transaction
async def exit_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                                   telegram_id=callback.message_from.id,
                                                                   session_id=session.id)

    await bot.app.store.players.delete_player(sql_session=sql_session,
                                              player_id=player.id)

    await bot.send_message(message=f'@{callback.message_from.username} left game!', chat_id=callback.message.chat.id,
                           reply_markup=get_join_exit_keyboard())

    players = await bot.app.store.players.get_players_by_session_id(sql_session=sql_session,
                                                                    session_id=session.id)
    players_count = await bot.app.store.players.get_players_count(sql_session=sql_session,
                                                                  session_id=session.id)

    if players_count == 1:
        player = players.first()
        game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session,
                                                                                  session_id=session.id)
        if game_state is None or \
                game_state.state == GameStateEnum.WAIT_FOR_SELECT_GAME or \
                game_state.state == GameStateEnum.WAIT_FOR_PLAYERS:
            return None

        await bot.app.store.questions_sessions.delete_question_session(sql_session=sql_session,
                                                                       session_id=session.id)
        await bot.app.store.players.delete_player(sql_session=sql_session,
                                                  player_id=player.id)
        await bot.app.store.game_states.delete_game_state(sql_session=sql_session,
                                                          game_state_id=game_state.id)
        await bot.app.store.sessions.delete_session(sql_session=sql_session,
                                                    session_id=session.id)

        username = await bot.get_chat_member_username(chat_id=callback.message.chat.id, user_id=player.telegram_id)

        return await bot.send_message(message=f'Winner @{username} with pot {player.pot}!',
                                      chat_id=callback.message.chat.id)
