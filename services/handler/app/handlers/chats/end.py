from app.schemas.message import MessageSchema
from app.utils.decorators.session import transaction


@transaction
async def end_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session, chat_id=message.chat.id)
    if session is None:
        return await bot.send_message(message=bot.message_helper.bad_message(username=message.message_from.username),
                                      chat_id=message.chat.id)

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)

    bot_answer: list[str] = []
    for player in await bot.app.store.players.get_players_by_session_id(session_id=session.id):
        username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player.telegram_id)
        s = f'@{username} has pot {player.pot}, gg!'
        bot_answer.append(s)
        await bot.app.store.players.delete_player(sql_session=sql_session,
                                                  player_id=player.id)

    await bot.app.store.questions_sessions.delete_question_session(sql_session=sql_session,
                                                                   session_id=session.id)
    await bot.app.store.game_states.delete_game_state(sql_session=sql_session,
                                                      game_state_id=game_state.id)
    await bot.app.store.sessions.delete_session(sql_session=sql_session,
                                                session_id=session.id)
