from uuid import UUID
from abc import ABC, abstractmethod


class Rest(ABC):
    def __init__(self, uid: UUID):
        super(Rest, self).__init__()
        self.uid = uid

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
