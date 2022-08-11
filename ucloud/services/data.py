from uuid import UUID
from abc import ABC, abstractmethod


class Data(ABC):
    def __init__(self, uid: UUID):
        super(Data, self).__init__()
        self.uid = uid

    @abstractmethod
    def get(uid: UUID) -> dict:
        pass

    @abstractmethod
    def put(uid: UUID, data: dict) -> dict:
        pass

    @abstractmethod
    def post(data: dict) -> UUID:
        pass

    @abstractmethod
    def delete(uid: UUID) -> dict:
        pass
