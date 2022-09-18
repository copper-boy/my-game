from sqlalchemy import delete, select, update

from app.base.base_accessor import BaseAccessor
from app.orm.game_state import GameStateEnum, GameStateModel
from app.orm.session import SessionModel


class GameStateAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def create_game_state(self, session: SessionModel) -> GameStateModel:
        __game_state = GameStateModel(session=session)

        async with self.app.database.session.begin() as session:
            session.add(__game_state)

        return __game_state

    async def delete_game_state(self, game_state_id: int) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(delete(GameStateModel).
                                  where(GameStateModel.id == game_state_id))

    async def update_game_state(self,
                                game_state_id: int,
                                current_question_id: int = 0,
                                current_player: int = 0,
                                state: GameStateEnum = GameStateEnum.WAIT_FOR_SELECT_GAME) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(update(GameStateModel).
                                  where(GameStateModel.id == game_state_id).
                                  values(current_question_id=current_question_id,
                                         current_player=current_player,
                                         state=state))

    async def get_game_state_by_session_id(self, session_id: int) -> GameStateModel:
        async with self.app.database.session() as session:
            sql = await session.execute(select(GameStateModel).where(GameStateModel.session_id == session_id))

        return sql.scalar()
