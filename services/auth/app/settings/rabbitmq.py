import logging
from asyncio import sleep

from aio_pika import RobustConnection, connect_robust
from aio_pika.patterns import RPC

from settings.config import get_admin_settings, get_amqp_settings
from utils.admin import create_admin
from utils.auth import register_user


async def admin() -> None:
    user = await register_user(get_admin_settings().ADMIN_LOGIN, get_admin_settings().ADMIN_PASSWORD)
    _unused = await create_admin(user)


async def register_methods(rpc: RPC) -> None:
    await rpc.register('create_admin', admin, auto_delete=True)


async def get_robust_connection(loop) -> RobustConnection:
    while True:
        try:
            connection = await connect_robust(get_amqp_settings().AMQP_URI, loop=loop)
        except ConnectionError:
            logging.warning('error connecting to rmq')
            await sleep(5)
        else:
            return connection


async def consume(loop) -> RobustConnection:
    connection = await get_robust_connection(loop)
    channel = await connection.channel()
    rpc = await RPC.create(channel)

    await register_methods(rpc)

    return connection

