from uuid import UUID

from fastapi import Depends

from ucloud.settings import Config, ConfigDep
from ucloud.services.queue.base import QueueBase
from ucloud.services.queue.sqlite import QueueSqlite
from ucloud.services.queue.mongodb import QueueMongoDB
from ucloud.services.queue.postgresql import QueuePostgreSQL
from ucloud.services.queue.aws_sqs import QueueAwsSqs


def Queue(root: UUID, config: Config = Depends(ConfigDep)) -> QueueBase:
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return QueueSqlite(root)
    if config.UCLOUD_QUEUE_TYPE == 'mongodb':
        return QueueMongoDB(root)
    if config.UCLOUD_QUEUE_TYPE == 'postgresql':
        return QueuePostgreSQL(root)
    if config.UCLOUD_QUEUE_TYPE == 'aws_sqs':
        return QueueAwsSqs(root)


async def startup(config: Config):
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return await QueueSqlite.startup(config)
    if config.UCLOUD_QUEUE_TYPE == 'mongodb':
        return await QueueMongoDB.startup(config)
    if config.UCLOUD_QUEUE_TYPE == 'postgresql':
        return await QueuePostgreSQL.startup(config)
    if config.UCLOUD_QUEUE_TYPE == 'aws_sqs':
        return await QueueAwsSqs.startup(config)


async def shutdown(config: Config):
    if config.UCLOUD_QUEUE_TYPE == 'sqlite':
        return await QueueSqlite.shutdown(config)
    if config.UCLOUD_QUEUE_TYPE == 'mongodb':
        return await QueueMongoDB.shutdown(config)
    if config.UCLOUD_QUEUE_TYPE == 'postgresql':
        return await QueuePostgreSQL.shutdown(config)
    if config.UCLOUD_QUEUE_TYPE == 'aws_sqs':
        return await QueueAwsSqs.shutdown(config)
