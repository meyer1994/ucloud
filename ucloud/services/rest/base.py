from uuid import UUID
from abc import ABC, abstractmethod

from ucloud.settings import config


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
