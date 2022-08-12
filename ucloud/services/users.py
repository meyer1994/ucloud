from uuid import UUID
from abc import ABC, abstractmethod


class Users(ABC):
    def __init__(self, uid: UUID):
        super(Users, self).__init__()
        self.uid = uid

    @abstractmethod
    async def create(self, data: dict) -> UUID:
        pass

    @abstractmethod
    async def delete(self, uid: UUID) -> dict:
        pass

    @abstractmethod
    async def login(self, uid: UUID, data: dict) -> dict:
        pass

    @abstractmethod
    async def logout(self, uid: UUID, token: str) -> dict:
        pass

    @abstractmethod
    async def fetch(self, uid: UUID) -> dict:
        pass
