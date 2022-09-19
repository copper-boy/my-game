from sqlalchemy import delete, select, update

from app.base.base_accessor import BaseAccessor
from app.orm.game_state import GameStateEnum, GameStateModel
from app.orm.session import SessionModel


class GameStateAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    async def create_game_state(sql_session, session: SessionModel) -> GameStateModel:
        __game_state = GameStateModel(session=session)

        sql_session.add(__game_state)

        return __game_state

    @staticmethod
    async def delete_game_state(sql_session, game_state_id: int) -> None:
        await sql_session.execute(delete(GameStateModel).
                                  where(GameStateModel.id == game_state_id))

    @staticmethod
    async def update_game_state(sql_session,
                                game_state_id: int,
                                current_question_id: int = 0,
                                current_player: int = 0,
                                state: GameStateEnum = GameStateEnum.WAIT_FOR_SELECT_GAME) -> None:
        await sql_session.execute(update(GameStateModel).
                                  where(GameStateModel.id == game_state_id).
                                  values(current_question_id=current_question_id,
                                         current_player=current_player,
                                         state=state))

    @staticmethod
    async def get_game_state_by_session_id(sql_session, session_id: int) -> GameStateModel:
        sql = await sql_session.execute(select(GameStateModel).where(GameStateModel.session_id == session_id))

        return sql.scalar()
