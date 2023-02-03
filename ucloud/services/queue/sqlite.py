import json
from uuid import uuid4
from datetime import datetime

from fastapi import Response
from databases import Database

from ucloud.settings import Config
from ucloud.services.queue.base import QueueBase


class QueueSqlite(QueueBase):
    _database = None

    async def push(self, data: dict) -> dict:
        values = {
            'root': str(self.root),
            'uid': str(uuid4()),
            'data': json.dumps(data),
            'timestamp': datetime.utcnow()
        }

        query = '''
            INSERT INTO ucloud_queue (root, uid, data, timestamp)
            VALUES (:root, :uid, :data, :timestamp)
            RETURNING *
        '''

        result = await self._database.fetch_one(query, values)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data),
            'timestamp': result.timestamp
        }

    async def pop(self) -> dict:
        item = await self.peek()

        if isinstance(item, Response):
            return item

        values = {
            'root': str(self.root),
            'timestamp': item['timestamp']
        }

        query = '''
            DELETE FROM ucloud_queue
            WHERE root = :root AND timestamp = :timestamp
        '''

        await self._database.execute(query, values)

        return item

    async def peek(self) -> dict:
        values = {
            'root': str(self.root)
        }

        query = '''
            SELECT * FROM ucloud_queue
            WHERE root = :root
            ORDER BY timestamp ASC
        '''

        result = await self._database.fetch_one(query, values)

        if result is None:
            return Response(status_code=206)

        return {
            'root': self.root,
            'uid': result.uid,
            'data': json.loads(result.data),
            'timestamp': result.timestamp
        }

    async def empty(self) -> None:
        values = {
            'root': str(self.root)
        }

        query = '''
            DELETE FROM ucloud_queue
            WHERE root = :root
        '''

        await self._database.execute(query, values)

    async def total(self) -> int:
        values = {
            'root': str(self.root)
        }

        query = '''
            SELECT count(*) AS total FROM ucloud_queue
            WHERE root = :root
        '''

        result = await self._database.fetch_one(query, values)

        return {
            'root': self.root,
            'data': {
                'total': result.total
            }
        }

    @classmethod
    async def startup(cls, config: Config):
        cls._database = Database(config.UCLOUD_QUEUE_SQLITE_PATH)
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

    @classmethod
    async def shutdown(cls, config):
        await cls._database.disconnect()
        cls._database = None
