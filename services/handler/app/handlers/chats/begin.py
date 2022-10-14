from app.integration.api import get_themes
from app.orm.game_state import GameStateEnum
from app.schemas.message import MessageSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction


@handle_exceptions
@transaction
async def begin_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=message.chat.id)

    game_state = await bot.app.store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                              session_id=session.id)
    if game_state.state != GameStateEnum.WAIT_FOR_PLAYERS:
        raise RuntimeError

    count = await bot.app.store.players.get_players_count(sql_session=sql_session,
                                                          session_id=session.id)
    if count < 2:
        raise RuntimeError

    player = await bot.app.store.players.get_random_player_by_session_id(sql_session=sql_session,
                                                                         session_id=session.id)

    themes = await get_themes(session=bot.app.store.aiohttp_session_accessor.aiohttp_session, game_id=session.game_id)

    await bot.app.store.game_states.update_game_state(sql_session=sql_session,
                                                      game_state_id=game_state.id,
                                                      current_player=player.id,
                                                      state=GameStateEnum.WAIT_FOR_PLAYER_ACTION)

    username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player.telegram_id)
    await bot.send_message(message=f'Current player is @{username}, please, select theme!',
                           chat_id=message.chat.id, reply_markup=themes[1])
