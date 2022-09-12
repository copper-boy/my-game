from logging import getLogger

import pytest
from tortoise.exceptions import IntegrityError

from app.utils.admin import create_admin

logger = getLogger('admin_tests')


@pytest.mark.usefixtures('anyio_backend')
class TestAdminCreate:
    async def test_successfully_create(self, default_user, config):
        admin = await create_admin(default_user)

        assert await admin[0].user.filter(adminmodel=admin[0].id).count() == 1
