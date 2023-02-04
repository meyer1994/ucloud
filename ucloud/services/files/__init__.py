from uuid import UUID

from fastapi import Depends

from ucloud.settings import Config, ConfigDep
from ucloud.services.files.base import FilesBase
from ucloud.services.files.local import FilesLocal
from ucloud.services.files.aws_s3 import FilesAwsS3


def Files(root: UUID, config: Config = Depends(ConfigDep)) -> FilesBase:
    if config.UCLOUD_FILES_TYPE == 'local':
        return FilesLocal(root)
    if config.UCLOUD_FILES_TYPE == 'aws_s3':
        return FilesAwsS3(root)


async def startup(config: Config):
    if config.UCLOUD_FILES_TYPE == 'local':
        return await FilesLocal.startup(config)
    if config.UCLOUD_FILES_TYPE == 'aws_s3':
        return await FilesAwsS3.startup(config)


async def shutdown(config: Config):
    if config.UCLOUD_FILES_TYPE == 'local':
        return await FilesLocal.shutdown(config)
    if config.UCLOUD_FILES_TYPE == 'aws_s3':
        return await FilesAwsS3.shutdown(config)
