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
    async def pop(self, uid: UUID) -> dict:
        pass

    @abstractmethod
    async def empty(self) -> None:
        pass

    @abstractmethod
    async def total(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    async def startup(config: Config):
        pass

    @staticmethod
    @abstractmethod
    async def shutdown(config: Config):
        pass
