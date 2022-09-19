from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.session import SessionModel
from app.store import Store


async def get_session_or_raise(store: Store,
                               sql_session: AsyncSession,
                               chat_id: str) -> SessionModel:
    session = await store.sessions.get_session_by_chat_id(sql_session=sql_session, chat_id=chat_id)

    if session is None:
        raise RuntimeError

    return session
