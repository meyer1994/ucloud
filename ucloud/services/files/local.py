import shutil
from uuid import UUID, uuid4
from tempfile import SpooledTemporaryFile
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from ucloud.settings import Config
from ucloud.services.files.base import FilesBase


class FilesLocal(FilesBase):
    _path = None

    async def write(self, data: SpooledTemporaryFile) -> dict:
        uid = uuid4()

        path = self._path / str(self.root)
        path.mkdir(parents=True, exist_ok=True)
        path = path / str(uid)

        with open(path, 'wb') as f:
            shutil.copyfileobj(data.file, f)

        return {
            'uid': uid,
            'root': self.root
        }

    async def read(self, uid: UUID) -> StreamingResponse:
        self._raise_404_if_not_exists(uid)

        path = self._path / str(self.root) / str(uid)

        def stream():
            with open(path, 'rb') as f:
                yield from f

        return StreamingResponse(stream())

    async def remove(self, uid: UUID):
        self._raise_404_if_not_exists(uid)
        path = self._path / str(self.root) / str(uid)
        path.unlink()

    @classmethod
    async def startup(cls, config: Config):
        cls._path = Path(config.UCLOUD_FILES_LOCAL_PATH)

    @classmethod
    async def shutdown(cls, config: Config):
        cls._path = None

    def _raise_404_if_not_exists(self, uid: str):
        path = self._path / str(self.root) / str(uid)
        if not path.exists():
            msg = f'Item {uid} from {self.root} not found in local'
            raise HTTPException(status_code=404, detail=msg)
