from uuid import UUID

from fastapi import Depends

from ucloud.settings import Config, ConfigDep
from ucloud.services.files.base import FilesBase
from ucloud.services.files.local import FilesLocal


def Files(root: UUID, config: Config = Depends(ConfigDep)) -> FilesBase:
    if config.UCLOUD_FILES_TYPE == 'local':
        return FilesLocal(root)


async def startup(config: Config):
    if config.UCLOUD_FILES_TYPE == 'local':
        return await FilesLocal.startup(config)


async def shutdown(config: Config):
    if config.UCLOUD_FILES_TYPE == 'local':
        return await FilesLocal.shutdown(config)
