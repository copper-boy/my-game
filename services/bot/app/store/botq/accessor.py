from asyncio import get_event_loop, sleep
from json import dumps
from typing import Any

from aio_pika import Channel, Connection, Message, Queue, connect

from app.base.base_accessor import BaseAccessor
from app.settings.config import get_amqp_settings


async def get_rabbit_connection(loop) -> Connection:
    for _unused in range(10):
        try:
            connection = await connect(get_amqp_settings().AMQP_URI, loop=loop)
        except ConnectionError:
            await sleep(1)
        else:
            return connection


class BotQAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.connection: Connection | None = None
        self.channel: Channel | None = None
        self.queue: Queue | None = None

    async def setup(self) -> None:
        loop = get_event_loop()
        self.connection = await get_rabbit_connection(loop)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(name='update')

    async def send(self, message: Any) -> None:
        await self.channel.default_exchange.publish(
            message=Message(dumps(message).encode('utf-8')),
            routing_key=self.queue.name
        )
        self.logger.info(f'successfully sent {message=}')

