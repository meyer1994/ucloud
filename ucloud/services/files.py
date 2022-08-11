from typing import IO
from uuid import UUID
from abc import ABC, abstractmethod


class Files(ABC):
    def __init__(self, uid: UUID):
        super(Files, self).__init__()
        self.uid = uid

    @abstractmethod
    def write(data: IO[bytes]) -> UUID:
        pass

    @abstractmethod
    def read(uid: UUID) -> IO[bytes]:
        pass

    @abstractmethod
    def remove(uid: UUID) -> IO[bytes]:
        pass
