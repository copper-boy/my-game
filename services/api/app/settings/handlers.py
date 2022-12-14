import logging

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_httpexception_handler(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
        logger.info(f'With request=([{request.method}][{request.url}][{request.query_params}]) '
                    f'occurred error=([{exception.status_code}][{exception.detail}])')

        return JSONResponse(status_code=exception.status_code,
                            content={
                                'detail': exception.detail
                            })


def register_all_exception_handlers(app: FastAPI) -> None:
    register_httpexception_handler(app)
