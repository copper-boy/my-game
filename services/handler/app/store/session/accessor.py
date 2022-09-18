from sqlalchemy import delete, select, update

from app.base.base_accessor import BaseAccessor
from app.orm.player import PlayerModel
from app.orm.session import SessionModel


class SessionAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def create_session(self, chat_id: str) -> SessionModel:
        __session = SessionModel(chat_id=chat_id)

        async with self.app.database.session.begin() as session:
            session.add(__session)

        return __session

    async def delete_session(self, session_id: int) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(delete(SessionModel).where(SessionModel.id == session_id))

    async def update_session(self, session_id: int, game_id: int = 0) -> None:
        async with self.app.database.session.begin() as session:
            __query = update(SessionModel).where(SessionModel.id == session_id).values(game_id=game_id)
            await session.execute(__query)

    async def get_session_by_chat_id(self, chat_id: str) -> SessionModel:
        async with self.app.database.session() as session:
            sql = await session.execute(select(SessionModel).where(SessionModel.chat_id == chat_id))

        return sql.scalar()
