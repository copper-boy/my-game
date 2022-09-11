from typing import Callable

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from settings.config import get_auth_site_settings


async def check_admin_authorization(authorization: str) -> bool:
    try:
        async with ClientSession(base_url=get_auth_site_settings().AUTH_SITE_BASE_URL,
                                 headers={'authorization': authorization}) as session:
            async with session.get(url='/api/v1/auth/current',
                                   raise_for_status=True) as response:
                json = await response.json()
    except (ClientResponseError, TypeError):
        return False

    return json['detail'].get('admin', None) is not None


async def admin_middleware(request: Request, call_next: Callable) -> Response:
    is_admin = await check_admin_authorization(request.headers.get('authorization'))

    if not is_admin:
        return JSONResponse(status_code=403,
                            content={
                                'detail': 'user is not admin'
                            })
    response = await call_next(request)
    return response


def setup_middlewares(app: FastAPI) -> None:
    app.middleware('http')(admin_middleware)
