from sqlalchemy import delete, select, update

from app.base.base_accessor import BaseAccessor
from app.orm.session import SessionModel


class SessionAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    async def create_session(sql_session, chat_id: str) -> SessionModel:
        __session = SessionModel(chat_id=chat_id)

        sql_session.add(__session)

        return __session

    @staticmethod
    async def delete_session(sql_session, session_id: int) -> None:
        await sql_session.execute(delete(SessionModel).where(SessionModel.id == session_id))

    @staticmethod
    async def update_session(sql_session, session_id: int, game_id: int = 0) -> None:
        await sql_session.execute(update(SessionModel).where(SessionModel.id == session_id).values(game_id=game_id))

    @staticmethod
    async def get_session_by_chat_id(sql_session, chat_id: str) -> SessionModel:
        sql = await sql_session.execute(select(SessionModel).where(SessionModel.chat_id == chat_id))

        return sql.scalar()
