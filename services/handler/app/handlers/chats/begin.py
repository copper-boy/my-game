from random import choice

from app.integration.api import get_themes
from app.orm.game_state import GameStateEnum
from app.schemas.message import MessageSchema

SELECT_THEME = """
Current player is @{}, please, select theme!
"""


async def begin_command_handler(bot, message: MessageSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=message.chat.id)

    if session is None:
        return await bot.send_message(message='Please, select a game first!')

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)
    if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
        return await bot.send_message(message='The game has already started', chat_id=message.chat.id)

    players = await bot.app.store.players.get_players_by_session_id(session_id=session.id)
    if len(players) < 2:
        return await bot.send_message(message='Not enough players!', chat_id=message.chat.id)
    player = choice(players)[0]

    themes = await get_themes(session=bot.app.store.aiohttp_session_accessor.aiohttp_session, game_id=session.game_id)

    await bot.app.store.game_states.update_game_state(game_state_id=game_state.id,
                                                      current_player=player.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYER_ACTION)

    await bot.send_message(message='Themes', chat_id=message.chat.id, reply_markup=themes)

    username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player.telegram_id)
    formatted_text = SELECT_THEME.format(username)
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)
