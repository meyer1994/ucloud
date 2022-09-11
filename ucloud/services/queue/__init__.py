from uuid import UUID

from fastapi import Depends

from ucloud.settings import Config, ConfigDep
from ucloud.services.queue.base import QueueBase
from ucloud.services.queue.sqlite import QueueSqlite


def Queue(root: UUID, config: Config = Depends(ConfigDep)) -> QueueBase:
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return QueueSqlite(root)


async def startup(config: Config):
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return await QueueSqlite.startup(config)


async def shutdown(config: Config):
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return await QueueSqlite.shutdown(config)
