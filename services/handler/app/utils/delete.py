from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.session import SessionModel
from app.store import Store


async def delete_session(store: Store,
                         sql_session: AsyncSession,
                         session: SessionModel) -> None:
    game_state = await store.game_states.get_game_state_by_session_id(sql_session=sql_session,
                                                                      session_id=session.id)
    players = await store.players.get_players_by_session_id(sql_session=sql_session,
                                                            session_id=session.id)

    for player in players:
        await store.players.delete_player(sql_session=sql_session,
                                          player_id=player.id)

    await store.questions_sessions.delete_question_session(sql_session=sql_session,
                                                           session_id=session.id)
    await store.game_states.delete_game_state(sql_session=sql_session,
                                              game_state_id=game_state.id)
    await store.sessions.delete_session(sql_session=sql_session,
                                        session_id=session.id)
