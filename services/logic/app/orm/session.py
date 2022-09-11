from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, BooleanField, IntField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        OneToOneField, OneToOneRelation,
                                        ReverseRelation)


class ChatModel(Model):
    id = BigIntField(pk=True, index=True)

    chat_id = BigIntField()
    session: OneToOneRelation = OneToOneField(model_name='models.SessionModel',
                                              related_name='chat')


chat_pydantic_out = pydantic_model_creator(ChatModel,
                                           name='ChatOutSchema')


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

    game: OneToOneRelation = OneToOneField(model_name='models.GameModel',
                                           related_name='sessions')
    chat: OneToOneRelation['ChatModel']
    players: ReverseRelation['PlayerModel']


session_pydantic_out = pydantic_model_creator(SessionModel,
                                              name='SessionOutSchema')
