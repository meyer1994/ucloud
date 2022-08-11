from uuid import UUID
from abc import ABC, abstractmethod


class Queue(ABC):
    def __init__(self, uid: UUID):
        super(Queue, self).__init__()
        self.uid = uid

    @abstractmethod
    def push(data: dict) -> UUID:
        pass

    @abstractmethod
    def pop(uid: UUID) -> dict:
        pass

    @abstractmethod
    def empty() -> None:
        pass

    @abstractmethod
    def total() -> int:
        pass
