from uuid import UUID
from abc import ABC, abstractmethod


class Queue(ABC):
    def __init__(self, uid: UUID):
        super(Queue, self).__init__()
        self.uid = uid

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
