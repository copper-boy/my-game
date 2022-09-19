from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import load_only
from sqlalchemy.sql.functions import count

from app.base.base_accessor import BaseAccessor
from app.orm.player import PlayerModel
from app.orm.session import SessionModel


class PlayerAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    async def create_player(sql_session, session: SessionModel, telegram_id: str) -> PlayerModel:
        __player = PlayerModel(session=session, telegram_id=telegram_id)

        sql_session.add(__player)

        return __player

    @staticmethod
    async def delete_player(sql_session, player_id: int) -> None:
        await sql_session.execute(delete(PlayerModel).
                                  where(PlayerModel.id == player_id))

    @staticmethod
    async def update_player(sql_session, player_id: int, pot: int) -> None:
        await sql_session.execute(update(PlayerModel).
                                  where(PlayerModel.id == player_id).
                                  values(pot=pot))

    @staticmethod
    async def update_all_is_answered(sql_session, session_id: int, is_answered: bool) -> bool:
        await sql_session.execute(update(PlayerModel).
                                  where(PlayerModel.session_id == session_id).
                                  values(is_answered=is_answered))

    @staticmethod
    async def update_is_answered(sql_session, player_id: int, is_answered: bool) -> None:
        await sql_session.execute(update(PlayerModel).
                                  where(PlayerModel.id == player_id).
                                  values(is_answered=is_answered))

    @staticmethod
    async def get_player_by_telegram_id(sql_session, telegram_id: str, session_id: int) -> PlayerModel:
        sql = await sql_session.execute(select(PlayerModel).
                                        where(and_(PlayerModel.telegram_id == telegram_id,
                                                   PlayerModel.session_id == session_id)))

        return sql.scalar()

    @staticmethod
    async def get_players_by_session_id(sql_session, session_id: int) -> list[PlayerModel]:
        scalars = await sql_session.execute(select(PlayerModel).
                                            where(PlayerModel.session_id == session_id))

        return scalars.scalars()

    @staticmethod
    async def get_players_count(sql_session, session_id: int) -> int:
        sql = await sql_session.execute(select(count(PlayerModel.id)).where(PlayerModel.session_id == session_id))

        return sql.scalar()
