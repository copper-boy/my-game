from typing import Any, Callable


class transaction:
    def __init__(self, function: Callable) -> None:
        self.function = function

    async def __call__(self, *args, **kwargs) -> Any:
        async with kwargs.get('bot').app.database.session.begin() as sql_session:
            return await self.function(sql_session=sql_session, *args, **kwargs)
