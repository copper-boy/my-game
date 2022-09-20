from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from game_state import GameStateModel
    from player import PlayerModel
    from question_session import QuestionSessionModel


class SessionModel(SQLModel, table=True):
    __tablename__ = 'sessions'

    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: Optional[str] = Field(default=None, index=True, unique=True)
    game_id: Optional[str] = Field(default=None, index=True)

    players: list['PlayerModel'] = Relationship(back_populates='session')
    game_state: Optional['GameStateModel'] = Relationship(back_populates='session',
                                                          sa_relationship_kwargs={
                                                              'uselist': False
                                                          })
    selected_questions: list['QuestionSessionModel'] = Relationship(back_populates='session')
