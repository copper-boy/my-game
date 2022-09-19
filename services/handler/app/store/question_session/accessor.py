from sqlalchemy import delete, select
from sqlalchemy.sql import and_

from app.base.base_accessor import BaseAccessor
from app.orm.question_session import QuestionSessionModel
from app.orm.session import SessionModel


class QuestionSessionAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    async def create_question_session(sql_session, question_id: int, session: SessionModel) -> QuestionSessionModel:
        __question_session = QuestionSessionModel(question_id=question_id, session=session)

        sql_session.add(__question_session)

        return __question_session

    @staticmethod
    async def delete_question_session(sql_session, session_id: int) -> None:
        await sql_session.execute(delete(QuestionSessionModel).
                                  where(QuestionSessionModel.session_id == session_id))

    @staticmethod
    async def get_question_session_by_id(sql_session, session_id: int, question_id: int) -> QuestionSessionModel:
        sql = await sql_session.execute(select(QuestionSessionModel).
                                        where(and_(QuestionSessionModel.session_id == session_id,
                                                   QuestionSessionModel.question_id == int(question_id))))

        return sql.scalar()

    @staticmethod
    async def get_questions_sessions_count(sql_session, session_id: int) -> int:
        sql = await sql_session.execute(select(QuestionSessionModel).
                                        where(QuestionSessionModel.session_id == session_id))

        return len(sql.all())
