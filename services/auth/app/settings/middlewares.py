from asyncio import get_event_loop
from typing import Callable

from aio_pika import connect_robust
from aio_pika.patterns import RPC
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response

from settings.config import get_amqp_settings


async def rpc_middleware(request: Request, call_next: Callable) -> Response:
    try:
        loop = get_event_loop()
        connection = await connect_robust(get_amqp_settings().AMQP_URI, loop=loop)
        channel = await connection.channel()
        request.state.rpc = await RPC.create(channel)

        response = await call_next(request)
    finally:
        await request.state.rpc.close()
    return response


def setup_middlewares(app: FastAPI) -> None:
    app.middleware('http')(rpc_middleware)
