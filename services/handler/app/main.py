import asyncio
import json

from aio_pika import connect
from aio_pika import IncomingMessage

from app.bot import Bot
from app.settings.config import get_telegram_bot_settings, get_amqp_settings

bot = Bot(get_telegram_bot_settings().TELEGRAM_BOT_ACCESS_TOKEN)


async def on_message(message: IncomingMessage) -> None:
    updates: list = json.loads(message.body.decode('utf-8'))

    await bot.handle(updates)


async def main() -> None:
    connection = None
    while True:
        try:
            connection = await connect(get_amqp_settings().AMQP_URI)
        except ConnectionError:
            continue
        else:
            break

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("update")
        await queue.consume(on_message, no_ack=True)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
