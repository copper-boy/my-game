from logging import getLogger

from aiohttp.web import Application


class BaseAccessor:
    app: Application

    def __init__(self, application: Application) -> None:
        self.app = application

        self.logger = getLogger('accessor')

        self.app.on_startup.append(self.connect)
        self.app.on_cleanup.append(self.disconnect)

    async def connect(self, *_: list, **__: dict) -> None:
        pass

    async def disconnect(self, *_: list, **__: dict) -> None:
        pass
