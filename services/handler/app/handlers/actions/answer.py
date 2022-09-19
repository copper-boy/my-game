from app.integration.api import get_answer, get_question, get_themes
from app.orm.game_state import GameStateEnum
from app.schemas.message import MessageSchema
from app.utils.decorators.session import transaction


@transaction
async def answer_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session, chat_id=message.chat.id)
    if session is None:
        return await bot.send_message(message='No chat game!', chat_id=message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                                   session_id=session.id,
                                                                   telegram_id=message.message_from.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)

    if player is None or \
            player.is_answered or \
            game_state.state != GameStateEnum.WAIT_FOR_PLAYER_ANSWER or \
            game_state.current_player != player.id:
        return await bot.send_message(message=f'@{message.message_from.username} you can`t answer!',
                                      chat_id=message.chat.id)

    answer_data = message.text.split()
    player_answer = ' '.join(answer_data[1:])

    question = await get_question(client=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                  question_id=game_state.current_question_id)
    server_answer = await get_answer(client=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                     question_id=game_state.current_question_id)

    if question is None or server_answer is None:
        return await bot.send_message(message=f'@{message.message_from.username} impossible to answer the question!',
                                      chat_id=message.chat.id)

    if player_answer.lower() == server_answer['correct'].lower():
        await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                          game_state_id=game_state.id,
                                                          current_player=player.id,
                                                          state=GameStateEnum.WAIT_FOR_PLAYER_ACTION)
        await bot.app.store.players.update_all_is_answered(sql_session=sql_session,
                                                           session_id=session.id, is_answered=False)
        await bot.app.store.players.update_player(sql_session=sql_session,
                                                  player_id=player.id,
                                                  pot=player.pot + question['cost'])

        themes = await get_themes(session=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                  game_id=session.game_id)
        count = await bot.app.store.questions_sessions.get_questions_sessions_count(sql_session=sql_session,
                                                                                    session_id=session.id)
        if themes[0] == count:
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

            await bot.send_message(message='\n'.join(bot_answer), chat_id=message.chat.id)
        else:
            await bot.send_message(message=f'@{message.message_from.username}, yea, this is current answer!',
                                   chat_id=message.chat.id)

            await bot.send_message(message='Themes', chat_id=message.chat.id, reply_markup=themes[1])
    else:
        await bot.app.store.players.update_is_answered(sql_session=sql_session,
                                                       player_id=player.id,
                                                       is_answered=True)
        await bot.app.store.players.update_player(sql_session=sql_session,
                                                  player_id=player.id,
                                                  pot=player.pot - question['cost'])
        await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                          game_state_id=game_state.id,
                                                          current_question_id=game_state.current_question_id,
                                                          current_player=0,
                                                          state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)

        await bot.send_message(message=f'@{message.message_from.username} is not correct answer!',
                               chat_id=message.chat.id)
