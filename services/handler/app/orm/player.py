from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from session import SessionModel


class PlayerModel(SQLModel, table=True):
    __tablename__ = 'players'

    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: str = Field(default='', index=True)

    pot: int = 0
    is_answered: bool = False

    session_id: Optional[int] = Field(default=None, foreign_key='sessions.id')
    session: Optional['SessionModel'] = Relationship(back_populates='players',
                                                     sa_relationship_kwargs=dict(cascade='all,delete'))
