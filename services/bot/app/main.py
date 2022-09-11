from asyncio import get_event_loop, run
from datetime import datetime
from logging import getLogger

from rabbit import get_rabbit_connection, send
from store import Store

logger = getLogger(__name__)


async def main() -> None:
    store = Store()

    loop = get_event_loop()
    connection = await get_rabbit_connection(loop)

    logger.info(f'telegram bot started at {datetime.now()}')
    offset = 0
    while True:
        try:
            updates = await store.telegram_api.poll(offset)
            for update in updates:
                offset = update['update_id'] + 1
            await send(connection=connection, message=updates)
        except Exception:
            logger.info(f'telegram bot stopped at {datetime.now()}')

if __name__ == '__main__':
    run(main())
