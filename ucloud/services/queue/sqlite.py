import json
from uuid import UUID, uuid4
from datetime import datetime

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
        values = {
            'root': str(self.root)
        }

        query = '''
            SELECT * FROM ucloud_queue
            WHERE root = :root
            ORDER BY timestamp ASC
        '''

        result = await self._database.fetch_one(query, values)

        values = {
            'root': str(self.root),
            'timestamp': result.timestamp
        }

        query = '''
            DELETE FROM ucloud_queue
            WHERE root = :root AND timestamp = :timestamp
        '''

        await self._database.execute(query, values)

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

        return {
            'root': self.root
        }

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

    @staticmethod
    async def startup(config):
        QueueSqlite._database = Database(config.UCLOUD_QUEUE_SQLITE_PATH)
        await QueueSqlite._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_queue (
                root TEXT,
                uid TEXT,
                data TEXT,
                timestamp TIMESTAMP,
                PRIMARY KEY (root, uid)
            )
        '''
        await QueueSqlite._database.execute(query)

        query = '''
            CREATE INDEX IF NOT EXISTS ucloud_queue_timestamp_idx
            ON ucloud_queue (timestamp ASC)
        '''
        await QueueSqlite._database.execute(query)

    @staticmethod
    async def shutdown(config):
        await QueueSqlite._database.disconnect()
        QueueSqlite._database = None
