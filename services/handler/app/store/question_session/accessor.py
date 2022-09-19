from sqlalchemy import delete, select
from sqlalchemy.sql import and_

from app.base.base_accessor import BaseAccessor
from app.orm.question_session import QuestionSessionModel
from app.orm.session import SessionModel


class QuestionSessionAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def create_question_session(self, question_id: int, session: SessionModel) -> QuestionSessionModel:
        __question_session = QuestionSessionModel(question_id=question_id, session=session)

        async with self.app.database.session.begin() as session:
            session.add(__question_session)

        return __question_session

    async def delete_question_session(self, session_id: int) -> None:
        async with self.app.database.session.begin() as session:
            await session.execute(delete(QuestionSessionModel).
                                  where(QuestionSessionModel.session_id == session_id))

    async def get_question_session_by_id(self, session_id: int, question_id: int) -> QuestionSessionModel:
        async with self.app.database.session() as session:
            sql = await session.execute(select(QuestionSessionModel).
                                        where(and_(QuestionSessionModel.session_id == session_id,
                                                   QuestionSessionModel.question_id == int(question_id))))

        return sql.scalar()

    async def get_questions_sessions_count(self, session_id: int) -> int:
        async with self.app.database.session() as session:
            sql = await session.execute(select(QuestionSessionModel).
                                        where(QuestionSessionModel.session_id == session_id))

        return len(sql.all())
