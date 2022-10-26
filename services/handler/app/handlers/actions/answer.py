from app.integration.api import get_answer, get_question, get_themes
from app.orm.game_state import GameStateEnum
from app.schemas.message import MessageSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction
from app.utils.delete import delete_session
from app.utils.end_message import get_end_message
from app.utils.player import (execute_player_bad_answer,
                              is_player_cant_give_answer)


@handle_exceptions
@transaction
async def answer_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session, chat_id=message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(sql_session=sql_session,
                                                                   session_id=session.id,
                                                                   telegram_id=message.message_from.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)

    if is_player_cant_give_answer(player=player, game_state=game_state):
        raise RuntimeError

    answer_data = message.text.split()
    player_answer = ' '.join(answer_data[1:])

    question = await get_question(client=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                  question_id=game_state.current_question_id)
    server_answer = await get_answer(client=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                     question_id=game_state.current_question_id)

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
            for player in await bot.app.store.players.get_players_by_session_id(sql_session=sql_session,
                                                                                session_id=session.id):
                username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player.telegram_id)
                s = f'@{username} has pot {player.pot}, gg!'
                bot_answer.append(s)

            await bot.send_message(message='\n'.join(bot_answer), chat_id=message.chat.id)

            await delete_session(store=bot.app.store,
                                 sql_session=sql_session,
                                 session=session)
        else:
            await bot.send_message(message=f'@{message.message_from.username}, yea, this is current answer!',
                                   chat_id=message.chat.id,
                                   reply_markup=themes[1])
    else:
        await execute_player_bad_answer(store=bot.app.store,
                                        sql_session=sql_session,
                                        player=player,
                                        game_state=game_state,
                                        question_cost=question['cost'])
        await bot.send_message(message=f'@{message.message_from.username} is not correct answer!',
                               chat_id=message.chat.id)
