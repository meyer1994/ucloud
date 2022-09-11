from uuid import UUID

from fastapi import Depends

from ucloud.settings import Config, ConfigDep
from ucloud.services.rest.base import RestBase
from ucloud.services.rest.sqlite import RestSqlite
from ucloud.services.rest.postgresql import RestPostgreSQL


def Rest(root: UUID, config: Config = Depends(ConfigDep)) -> RestBase:
    if config.UCLOUD_REST_TYPE == 'sqlite':
        return RestSqlite(root)
    if config.UCLOUD_REST_TYPE == 'postgresql':
        return RestPostgreSQL(root)


async def startup(config: Config):
    if config.UCLOUD_REST_TYPE == 'sqlite':
        return await RestSqlite.startup(config)
    if config.UCLOUD_REST_TYPE == 'postgresql':
        return await RestPostgreSQL.startup(config)


async def shutdown(config: Config):
    if config.UCLOUD_REST_TYPE == 'sqlite':
        return await RestSqlite.shutdown(config)
    if config.UCLOUD_REST_TYPE == 'postgresql':
        return await RestPostgreSQL.shutdown(config)
