from typing import Callable

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from app.settings.config import get_auth_site_settings


async def check_admin_authorization_token(token: str) -> bool:
    try:
        async with ClientSession(base_url=get_auth_site_settings().AUTH_SITE_BASE_URL) as session:
            async with session.get(url='/api/v1/auth/admin',
                                   params={
                                       'token': token
                                   },
                                   raise_for_status=True):
                return True
    except ClientResponseError:
        return False


async def check_admin_authorization_header(authorization: str) -> bool:
    try:
        async with ClientSession(base_url=get_auth_site_settings().AUTH_SITE_BASE_URL,
                                 headers={'authorization': authorization}) as session:
            async with session.get(url='/api/v1/auth/current',
                                   raise_for_status=True) as response:
                json = await response.json()
    except (ClientResponseError, TypeError):
        return False

    return json['detail']['user']['is_admin']


async def admin_middleware(request: Request, call_next: Callable) -> Response:
    if request.url.path in {
        '/api/openapi.json',
        '/api/docs',
        '/api/redoc',
        '/favico.ico'
    }:
        response = await call_next(request)
        return response

    token = request.query_params.get('token', None)
    header = request.headers.get('authorization', None)

    if token:
        is_admin = await check_admin_authorization_token(token)
    else:
        is_admin = await check_admin_authorization_header(header)

    if not is_admin:
        return JSONResponse(status_code=403,
                            content={
                                'detail': 'user is not admin'
                            })
    response = await call_next(request)
    return response


def setup_middlewares(app: FastAPI) -> None:
    app.middleware('http')(admin_middleware)
