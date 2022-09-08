from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, CharField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation


class UserModel(Model):
    id = BigIntField(pk=True, index=True)

    email = CharField(max_length=200, null=False, unique=True)
    password = CharField(max_length=200, null=False)


user_pydantic_out = pydantic_model_creator(UserModel, name='UserModelOutSchema',
                                           exclude=('password',))


class AdminModel(Model):
    id = BigIntField(pk=True, index=True)

    user: ForeignKeyRelation[UserModel] = ForeignKeyField(model_name='models.UserModel', unique=True)


admin_pydantic_out = pydantic_model_creator(AdminModel, name='AdminModelOutSchema')

