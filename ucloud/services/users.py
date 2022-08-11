from uuid import UUID
from abc import ABC, abstractmethod


class Users(ABC):
    def __init__(self, uid: UUID):
        super(Users, self).__init__()
        self.uid = uid

    @abstractmethod
    def create(data: dict) -> UUID:
        pass

    @abstractmethod
    def delete(uid: UUID) -> dict:
        pass

    @abstractmethod
    def login(uid: UUID, data: dict) -> dict:
        pass

    @abstractmethod
    def logout(uid: UUID, token: str) -> dict:
        pass

    @abstractmethod
    def fetch(uid: UUID) -> dict:
        pass
