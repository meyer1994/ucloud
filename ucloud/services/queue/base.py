from uuid import UUID
from abc import ABC, abstractmethod

from ucloud.settings import Config


class QueueBase(ABC):
    def __init__(self, root: UUID):
        super(QueueBase, self).__init__()
        self.root = root

    @abstractmethod
    async def push(self, data: dict) -> UUID:
        pass

    @abstractmethod
    async def pop(self) -> dict:
        pass

    @abstractmethod
    async def peek(self) -> dict:
        pass

    @abstractmethod
    async def empty(self) -> None:
        pass

    @abstractmethod
    async def total(self) -> int:
        pass

    @classmethod
    @abstractmethod
    async def startup(cls, config: Config):
        pass

    @classmethod
    @abstractmethod
    async def shutdown(cls, config: Config):
        pass
