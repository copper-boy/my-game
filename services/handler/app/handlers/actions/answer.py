from app.integration.api import get_answer, get_question, get_themes, get_questions_count
from app.orm.game_state import GameStateEnum
from app.schemas.message import MessageSchema


async def answer_command_handler(bot, message: MessageSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=message.chat.id)
    if session is None:
        return await bot.send_message(message='No chat game!', chat_id=message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(session_id=session.id,
                                                                   telegram_id=message.message_from.id)
    game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)

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
        await bot.app.store.game_states.update_game_state(game_state_id=game_state.id,
                                                          current_player=player.id,
                                                          state=GameStateEnum.WAIT_FOR_PLAYER_ACTION)
        await bot.app.store.players.update_all_is_answered(session_id=session.id, is_answered=False)
        await bot.app.store.players.update_player(player_id=player.id,
                                                  pot=player.pot + question['cost'])

        themes = await get_themes(session=bot.app.store.aiohttp_session_accessor.aiohttp_session,
                                  game_id=session.game_id,
                                  exclude=True)
        if themes is None:

            for player in await bot.app.store.players.get_players_by_session_id(session_id=session.id):

            await bot.app.store.questions_sessions.delete_question_session(session_id=session.id)
            await bot.app.store.game_states.delete_game_state(game_state_id=game_state.id)
            await bot.app.store.sessions.delete_session(session_id=session.id)

        await bot.send_message(message=f'@{message.message_from.username}, yea, this is current answer!',
                               chat_id=message.chat.id)

        await bot.send_message(message='Themes', chat_id=message.chat.id, reply_markup=themes)
    else:
        await bot.app.store.players.update_is_answered(player_id=player.id,
                                                       is_answered=True)
        await bot.app.store.players.update_player(player_id=player.id,
                                                  pot=player.pot - question['cost'])
        await bot.app.store.game_states.update_game_state(game_state_id=game_state.id,
                                                          current_question_id=game_state.current_question_id,
                                                          current_player=0,
                                                          state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)

        await bot.send_message(message=f'@{message.message_from.username} is not correct answer!',
                               chat_id=message.chat.id)
