from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, BooleanField, CharField


class UserModel(Model):
    id = BigIntField(pk=True, index=True)

    email = CharField(max_length=200, null=False, unique=True)
    password = CharField(max_length=200, null=False)

    is_admin = BooleanField(default=False)


user_pydantic_out = pydantic_model_creator(UserModel, name='UserModelOutSchema',
                                           exclude=('password',))
