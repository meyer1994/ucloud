from typing import IO
from uuid import UUID
from abc import ABC, abstractmethod

from ucloud.settings import Config


class FilesBase(ABC):
    def __init__(self, root: UUID):
        super(FilesBase, self).__init__()
        self.root = root

    @abstractmethod
    async def write(self, data: IO[bytes]) -> UUID:
        pass

    @abstractmethod
    async def read(self, uid: UUID) -> IO[bytes]:
        pass

    @abstractmethod
    async def remove(self, uid: UUID) -> IO[bytes]:
        pass

    @staticmethod
    @abstractmethod
    async def startup(config: Config):
        pass

    @staticmethod
    @abstractmethod
    async def shutdown(config: Config):
        pass
