from uuid import UUID
from abc import ABC, abstractmethod

from ucloud.settings import Config


class RestBase(ABC):
    def __init__(self, root: UUID):
        super(RestBase, self).__init__()
        self.root = root

    @abstractmethod
    async def get(self, uid: UUID) -> dict:
        pass

    @abstractmethod
    async def put(self, uid: UUID, data: dict) -> dict:
        pass

    @abstractmethod
    async def post(self, data: dict) -> UUID:
        pass

    @abstractmethod
    async def delete(self, uid: UUID) -> dict:
        pass

    @staticmethod
    @abstractmethod
    async def startup(config: Config):
        pass

    @staticmethod
    @abstractmethod
    async def shutdown(config: Config):
        pass
