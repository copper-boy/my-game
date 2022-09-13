from asyncio import run
from datetime import datetime
from logging import getLogger

from app.store import Store

logger = getLogger(__name__)


async def main() -> None:
    store = Store()
    await store.setup()

    logger.info(f'telegram bot started at {datetime.now()}')
    offset = 0
    while True:
        try:
            updates = await store.telegram_api.poll(offset)
            for update in updates:
                offset = update['update_id'] + 1
            await store.botq.send(updates)
        except Exception:
            logger.info(f'telegram bot stopped at {datetime.now()}')

if __name__ == '__main__':
    run(main())
