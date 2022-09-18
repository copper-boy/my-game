from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import load_only
from sqlalchemy.sql.functions import count

from app.base.base_accessor import BaseAccessor
from app.orm.player import PlayerModel
from app.orm.session import SessionModel


class PlayerAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def create_player(self, session: SessionModel, telegram_id: str) -> PlayerModel:
        __player = PlayerModel(session=session, telegram_id=telegram_id)

        async with self.app.database.session.begin() as __session:
            __session.add(__player)

        return __player

    async def delete_player(self, player_id: int) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(delete(PlayerModel).
                                  where(PlayerModel.id == player_id))

    async def update_player(self, player_id: int, pot: int) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(update(PlayerModel).
                                  where(PlayerModel.id == player_id).
                                  values(pot=pot))

    async def update_all_is_answered(self, session_id: int, is_answered: bool) -> bool:
        async with self.app.database.session.begin() as session:
            await session.execute(update(PlayerModel).
                                  where(PlayerModel.session_id == session_id).
                                  values(is_answered=is_answered))

    async def update_is_answered(self, player_id: int, is_answered: bool) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(update(PlayerModel).
                                  where(PlayerModel.id == player_id).
                                  values(is_answered=is_answered))

    async def get_player_by_telegram_id(self, telegram_id: str, session_id: int) -> PlayerModel:
        async with self.app.database.session() as session:
            sql = await session.execute(select(PlayerModel).
                                        where(and_(PlayerModel.telegram_id == telegram_id,
                                                   PlayerModel.session_id == session_id)))

        return sql.scalar()

    async def get_players_by_session_id(self, session_id: int) -> list[PlayerModel]:
        async with self.app.database.session() as session:
            scalars = await session.execute(select(PlayerModel).
                                            where(PlayerModel.session_id == session_id))

        return scalars.all()

    async def get_players_count(self, session_id: int) -> int:
        async with self.app.database.session() as session:
            sql = await session.execute(select(count(PlayerModel.id)).where(PlayerModel.session_id == session_id))

        return sql.scalars()
