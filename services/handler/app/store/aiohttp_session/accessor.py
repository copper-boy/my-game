from aiohttp import ClientSession

from app.base.base_accessor import BaseAccessor


class AiohttpSessionAccessor(BaseAccessor):
    aiohttp_session: ClientSession

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def connect(self, *_: list, **__: dict) -> None:
        self.aiohttp_session = ClientSession()

    async def disconnect(self, *_: list, **__: dict) -> None:
        await self.aiohttp_session.close()
