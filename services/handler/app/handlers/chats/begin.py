from aiohttp import ClientSession

from app.authed_client import set_auth_session
from app.settings.config import get_auth_site_settings


async def begin_command_handler(bot: Bot, message: Message):
    async with ClientSession(base_url=get_auth_site_settings().AUTH_SITE_URL) as session:
        await set_auth_session(session)

        async with session.post(url='') as response:
            pass
