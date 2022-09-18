from app.keyboard import GAME_KEYBOARD
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema

EXIT_TEXT = """
@{} left game!
"""


async def exit_callback_handler(bot, callback: CallbackSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=callback.message.chat.id)
    if session is None:
        return await bot.send_message(message='No chat game!', chat_id=callback.message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(telegram_id=callback.message_from.id,
                                                                   session_id=session.id)

    if player is None:
        return await bot.send_message(message=f'@{callback.message_from.username} are not in the game!',
                                      chat_id=callback.message.chat.id)

    await bot.app.store.players.delete_player(player_id=player.id)

    formatted_text = EXIT_TEXT.format(callback.message_from.username)
    await bot.send_message(message=formatted_text, chat_id=callback.message.chat.id, reply_markup=GAME_KEYBOARD)

    players = await bot.app.store.players.get_players_by_session_id(session_id=session.id)
    players_count = await bot.app.store.players.get_players_count(session_id=session.id)

    if players_count.first() == 1:
        player = players[0][0]
        game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)
        if game_state is None or \
                game_state.state == GameStateEnum.WAIT_FOR_SELECT_GAME or \
                game_state.state == GameStateEnum.WAIT_FOR_PLAYERS:
            return None

        username = await bot.get_chat_member_username(chat_id=callback.message.chat.id, user_id=player.telegram_id)

        await bot.app.store.questions_sessions.delete_question_session(session_id=session.id)
        await bot.app.store.players.delete_player(player_id=player.id)
        await bot.app.store.game_states.delete_game_state(game_state_id=game_state.id)
        await bot.app.store.sessions.delete_session(session_id=session.id)

        return await bot.send_message(message=f'Winner @{username} with pot {player.pot}!',
                                      chat_id=callback.message.chat.id)
