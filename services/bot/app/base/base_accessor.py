from logging import getLogger
from typing import Any


class BaseAccessor:
    logger: Any | None = None

    def __init__(self) -> None:
        self.logger = getLogger('accessor')
