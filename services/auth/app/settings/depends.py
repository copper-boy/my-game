from aio_pika.patterns import RPC
from fastapi.requests import Request


async def get_rpc(request: Request) -> RPC:
    return request.state.rpc
