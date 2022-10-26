from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.game_state import GameStateEnum, GameStateModel
from app.orm.player import PlayerModel
from app.store import Store


async def execute_player_bad_answer(store: Store,
                                    sql_session: AsyncSession,
                                    player: PlayerModel,
                                    game_state: GameStateModel,
                                    question_cost: int) -> None:
    await store.players.update_is_answered(sql_session=sql_session,
                                           player_id=player.id,
                                           is_answered=True)
    await store.players.update_player(sql_session=sql_session,
                                      player_id=player.id,
                                      pot=player.pot - question_cost)
    await store.game_states.update_game_state(sql_session=sql_session,
                                              game_state_id=game_state.id,
                                              current_question_id=game_state.current_question_id,
                                              current_player=0,
                                              state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)


def is_player_cant_give_answer(player: PlayerModel,
                               game_state: GameStateModel,
                               current_player: int = None) -> bool:
    __id = current_player if current_player is not None else player.id
    return (player is None or player.is_answered or
            game_state.state != GameStateEnum.WAIT_FOR_PLAYER_ANSWER or game_state.current_player != __id)
