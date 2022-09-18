from typing import Optional

from aiohttp.web import Application
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from app.settings.config import get_database_settings


class Database:
    def __init__(self, application: Application) -> None:
        self.app = application
        self._engine: Optional[AsyncEngine] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._engine = create_async_engine(get_database_settings().HANDLER_DATABASE_URI,
                                           echo=True, future=True)
        self.session = sessionmaker(class_=AsyncSession, bind=self._engine, expire_on_commit=False)

    async def disconnect(self, *_: list, **__: dict) -> None:
        self._engine = None
        self.session = None
