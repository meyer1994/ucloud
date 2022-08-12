from typing import IO
from uuid import UUID
from abc import ABC, abstractmethod


class Files(ABC):
    def __init__(self, uid: UUID):
        super(Files, self).__init__()
        self.uid = uid

    @abstractmethod
    async def write(self, data: IO[bytes]) -> UUID:
        pass

    @abstractmethod
    async def read(self, uid: UUID) -> IO[bytes]:
        pass

    @abstractmethod
    async def remove(self, uid: UUID) -> IO[bytes]:
        pass
