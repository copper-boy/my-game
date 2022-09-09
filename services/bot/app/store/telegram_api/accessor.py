from aiohttp.client import ClientSession

from base.base_accessor import BaseAccessor

API_PATH = 'https://api.telegram.org'


class TelegramAccessor(BaseAccessor):
    bot_token: str

    def __init__(self, bot_token: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bot_token = bot_token

    async def poll(self, offset: int = 0) -> dict:
        async with ClientSession(base_url=API_PATH) as session:
            async with session.get(
                    url=f'/bot{self.bot_token}/getUpdates',
                    params={
                        'offset': offset,
                        'timeout': 60
                    }
            ) as response:
                json = await response.json()

        return json['result']
