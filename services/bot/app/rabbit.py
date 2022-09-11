from asyncio import sleep
from json import dumps
from logging import getLogger

from aio_pika import Connection, Message, connect

from settings.config import get_amqp_settings

logger = getLogger('rabbitmq')


async def get_rabbit_connection(loop) -> Connection:
    for _unused in range(10):
        try:
            connection = await connect(get_amqp_settings().AMQP_URI, loop=loop)
        except ConnectionError:
            logger.warning('error connecting to rmq')
            await sleep(5)
        else:
            return connection


async def send(connection: Connection, message: dict) -> None:
    channel = await connection.channel()

    queue = await channel.declare_queue(name='update')

    await channel.default_exchange.publish(
        message=Message(dumps(message).encode('utf-8')),
        routing_key=queue.name
    )

    logger.critical(f'successfully sent {message=}')
