from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, CharField, IntField, TextField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        OneToOneField, OneToOneRelation,
                                        ReverseRelation)


class GameModel(Model):
    id = BigIntField(pk=True, index=True)

    name = CharField(max_length=200, unique=True)

    session: OneToOneRelation
    themes: ReverseRelation


game_pydantic_in = pydantic_model_creator(GameModel,
                                          name='GameInSchema',
                                          exclude=('id', 'is_started', 'session', 'themes',))

game_pydantic_out = pydantic_model_creator(GameModel,
                                           name='GameOutSchema')


class ThemeModel(Model):
    id = BigIntField(pk=True, index=True)

    title = TextField()

    game: ForeignKeyRelation['GameModel'] = ForeignKeyField(model_name='models.GameModel',
                                                            related_name='themes')
    questions: ReverseRelation


theme_pydantic_in = pydantic_model_creator(ThemeModel,
                                           name='ThemeInSchema',
                                           exclude=('id', 'game', 'questions',))

theme_pydantic_out = pydantic_model_creator(ThemeModel,
                                            name='ThemeOutSchema')


class QuestionModel(Model):
    id = BigIntField(pk=True, index=True)

    title = CharField(max_length=200, unique=True)
    cost = IntField(default=0)

    theme: ForeignKeyRelation['ThemeModel'] = ForeignKeyField(model_name='models.ThemeModel',
                                                              related_name='questions')
    answer: ForeignKeyRelation


question_pydantic_in = pydantic_model_creator(QuestionModel,
                                              name='QuestionInSchema',
                                              exclude=('id', 'theme', 'answer',))

question_pydantic_out = pydantic_model_creator(QuestionModel,
                                               name='QuestionOutSchema')


class AnswerModel(Model):
    id = BigIntField(pk=True, index=True)

    correct = TextField()

    question: ForeignKeyRelation['QuestionModel'] = ForeignKeyField(model_name='models.AnswerModel',
                                                                    related_name='answer')


answer_pydantic_in = pydantic_model_creator(AnswerModel,
                                            name='AnswerInSchema',
                                            exclude=('id', 'question',))

answer_pydantic_out = pydantic_model_creator(AnswerModel,
                                             name='AnswerOutSchema')
