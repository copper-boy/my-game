from aiohttp import ClientSession

from app.settings.config import get_admin_settings


async def set_auth_session(session: ClientSession) -> None:
    admin_config = get_admin_settings()

    async with session.post(url='http://auth_service:8956/api/v1/auth/login',
                            json={
                                'email': admin_config.ADMIN_LOGIN,
                                'password': admin_config.ADMIN_PASSWORD
                            }) as response:
        json = await response.json()
    session.headers['Authorization'] = f'Bearer {json["detail"].get("access_token", None)}'
