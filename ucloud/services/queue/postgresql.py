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
        cls._database = Database(config.UCLOUD_QUEUE_POSTGRESQL_PATH)
        await cls._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_queue (
                root TEXT,
                uid TEXT,
                data TEXT,
                timestamp TIMESTAMP NOT NULL,
                PRIMARY KEY (root, uid)
            )
        '''
        await cls._database.execute(query)

        query = '''
            CREATE INDEX IF NOT EXISTS ucloud_queue_root_timestamp_idx
            ON ucloud_queue (root, timestamp ASC)
        '''
        await cls._database.execute(query)
