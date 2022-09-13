from logging import getLogger

import pytest

from app.utils.user import (get_user_by_email, register_admin,
                            update_user_to_admin)

logger = getLogger('admin')


@pytest.mark.usefixtures('anyio_backend')
class TestAdminCreate:
    async def test_successfully_create(self, default_user, config):
        await update_user_to_admin(default_user)

        assert default_user.is_admin

    async def test_register_admin(self, config):
        await register_admin()
        user = await get_user_by_email(email=config.ADMIN_LOGIN)

        assert user.is_admin


