from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from session import SessionModel


class QuestionSessionModel(SQLModel, table=True):
    __tablename__ = 'questionsessions'

    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = 0

    session_id: Optional[int] = Field(default=None, foreign_key='sessions.id')
    session: Optional['SessionModel'] = Relationship(back_populates='selected_questions',
                                                     sa_relationship_kwargs=dict(cascade='all,delete'))
