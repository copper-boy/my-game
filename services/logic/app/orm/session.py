from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, BooleanField, IntField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        ReverseRelation)


class PlayerModel(Model):
    id = BigIntField(pk=True, index=True)
    player_id = BigIntField()

    pot = IntField(default=0)

    session: ForeignKeyRelation = ForeignKeyField(model_name='models.SessionModel',
                                                  related_name='players')


player_pydantic_out = pydantic_model_creator(PlayerModel,
                                             name='PlayerOutSchema')


class SessionModel(Model):
    id = BigIntField(pk=True, index=True)

    is_started = BooleanField(default=False)
    chat_id = BigIntField(unique=True)
    game_id = BigIntField()

    players: ReverseRelation['PlayerModel']


session_pydantic_out = pydantic_model_creator(SessionModel,
                                              name='SessionOutSchema')
