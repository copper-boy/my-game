from asyncio import sleep
from json import loads
from logging import getLogger

from aio_pika import IncomingMessage, connect
from aiohttp.web import Application, Request, json_response, run_app

from app.bot import Bot
from app.settings.config import get_amqp_settings, get_telegram_bot_settings
from app.store import setup_store

logger = getLogger(__name__)


async def root(request: Request) -> json_response:
    logger.info('health check called')
    return json_response(status=200,
                         data={
                             'ping': 'pong'
                         })


async def on_message(message: IncomingMessage) -> None:
    updates: list = loads(message.body.decode('utf-8'))

    await bot.handle(updates)


async def get_connection() -> None:
    while True:
        try:
            connection = await connect(get_amqp_settings().AMQP_URI)
        except ConnectionError:
            logger.info('wait for rabbitmq')
            await sleep(1)
        else:
            return connection


async def listen_events(application: Application) -> None:
    connection = application['rabbitmq']

    channel = await connection.channel()
    queue = await channel.declare_queue("update")
    await queue.consume(on_message, no_ack=True)


async def setup_rabbitmq(application: Application) -> None:
    connection = await get_connection()
    application['rabbitmq'] = connection
    await listen_events(application)


async def close_rabbitmq(application: Application) -> None:
    await application['rabbitmq'].close()


def setup_application() -> Application:
    application = Application()

    setup_store(application)

    application.router.add_get('/', root)

    application.on_startup.append(setup_rabbitmq)
    application.on_shutdown.append(close_rabbitmq)

    return application


app = setup_application()
bot = Bot(application=app, bot_token=get_telegram_bot_settings().TELEGRAM_BOT_API_TOKEN)

if __name__ == '__main__':
    run_app(app)
