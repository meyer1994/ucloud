import shutil
from uuid import UUID, uuid4
from tempfile import SpooledTemporaryFile
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse

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

    async def read(self, uid: UUID) -> FileResponse:
        path = self._path / str(self.root) / str(uid)

        if not path.exists():
            msg = f'File {uid} from {self.root} not found in local'
            raise HTTPException(status_code=404, detail=msg)

        return FileResponse(path)

    async def remove(self, uid: UUID):
        path = self._path / str(self.root) / str(uid)

        if not path.exists():
            msg = f'File {uid} from {self.root} not found in local'
            raise HTTPException(status_code=404, detail=msg)

        path.unlink()

    @staticmethod
    async def startup(config: Config):
        FilesLocal._path = Path(config.UCLOUD_FILES_LOCAL_PATH)

    @staticmethod
    async def shutdown(config: Config):
        FilesLocal._path = None
