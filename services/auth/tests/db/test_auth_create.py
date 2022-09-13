from logging import getLogger

import pytest
from tortoise.exceptions import DoesNotExist

from app.schemas.auth import AuthSchema
from app.utils.auth import authenticate_user, delete_user, register_user

logger = getLogger('auth')


class TestUserCreate:
    async def test_successfully_create(self, config):
        await delete_user(config.ADMIN_LOGIN)

        user = await register_user(config.ADMIN_LOGIN, config.ADMIN_PASSWORD)

        assert user.email == config.ADMIN_LOGIN


class TestUserAuth:
    async def test_db_successfully_auth(self, config):
        user = await authenticate_user(AuthSchema(email=config.ADMIN_LOGIN,
                                                  password=config.ADMIN_PASSWORD))

        assert user.email == config.ADMIN_LOGIN

    async def test_db_bad_login(self, config):
        with pytest.raises(DoesNotExist) as e_info:
            await authenticate_user(AuthSchema(email='not-found@email.com',
                                               password='invalid_password_posted'))
            logger.exception(e_info)
