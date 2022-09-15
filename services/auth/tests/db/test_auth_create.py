from logging import getLogger

import pytest
from app.schemas.auth import AuthSchema
from app.utils.auth import authenticate_user, delete_user, register_user
from tortoise.exceptions import DoesNotExist

logger = getLogger('auth')


class TestUserCreate:
    async def test_successfully_create(self):
        await delete_user('some@email.com')

        user = await register_user('some@email.com', 'very_strong_password')

        assert user.email == 'some@email.com'


class TestUserAuth:
    async def test_db_successfully_auth(self):
        user = await authenticate_user(AuthSchema(email='some@email.com',
                                                  password='very_strong_password'))

        assert user.email == 'some@email.com'

    async def test_db_bad_login(self):
        with pytest.raises(DoesNotExist) as e_info:
            await authenticate_user(AuthSchema(email='not-found@email.com',
                                               password='invalid_password_posted'))
            logger.exception(e_info)
