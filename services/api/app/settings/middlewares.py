from typing import Callable

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from app.settings.config import get_admin_settings


async def admin_middleware(request: Request, call_next: Callable) -> Response:
    token = request.query_params.get('token', None)

    if token != get_admin_settings().INFINITY_ADMIN_TOKEN:
        return JSONResponse(status_code=403,
                            content={
                                'detail': 'user is not admin'
                            })
    response = await call_next(request)
    return response


def setup_middlewares(app: FastAPI) -> None:
    app.middleware('http')(admin_middleware)
