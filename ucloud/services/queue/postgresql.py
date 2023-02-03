import json
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import Response
from databases import Database

from ucloud.settings import Config
from ucloud.services.queue.sqlite import QueueSqlite


class QueuePostgreSQL(QueueSqlite):
    @classmethod
    async def startup(cls, config):
        cls._database = Database(config.UCLOUD_REST_SQLITE_PATH)
        await cls._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_rest (
                root TEXT,
                uid TEXT,
                data JSONB,
                PRIMARY KEY (root, uid)
            )
        '''
        await cls._database.execute(query)
