from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from session import SessionModel


class GameStateEnum(Enum):
    WAIT_FOR_SELECT_GAME = 0
    WAIT_FOR_PLAYERS = 1
    WAIT_FOR_PLAYER_ACTION = 2
    WAIT_FOR_PLAYER_ANSWER = 3


class GameStateModel(SQLModel, table=True):
    __tablename__ = 'gamestates'

    id: Optional[int] = Field(default=None, primary_key=True)
    current_question_id: int = 0
    current_player: int = 0

    state: GameStateEnum = GameStateEnum.WAIT_FOR_SELECT_GAME

    session_id: Optional[int] = Field(default=None, foreign_key='sessions.id')
    session: Optional['SessionModel'] = Relationship(back_populates='game_state',
                                                     sa_relationship_kwargs=dict(cascade='all,delete'))
