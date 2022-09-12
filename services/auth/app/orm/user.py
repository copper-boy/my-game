from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, CharField
from tortoise.fields.relational import OneToOneField, OneToOneRelation


class UserModel(Model):
    id = BigIntField(pk=True, index=True)

    email = CharField(max_length=200, null=False, unique=True)
    password = CharField(max_length=200, null=False)

    admin: OneToOneRelation


user_pydantic_out = pydantic_model_creator(UserModel, name='UserModelOutSchema',
                                           exclude=('password',))


class AdminModel(Model):
    id = BigIntField(pk=True, index=True)

    user: OneToOneRelation['UserModel'] = OneToOneField(model_name='models.UserModel')


admin_pydantic_out = pydantic_model_creator(AdminModel, name='AdminModelOutSchema')
