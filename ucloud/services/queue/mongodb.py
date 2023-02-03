from uuid import uuid4
from datetime import datetime

import pymongo
from fastapi import Response
from motor.motor_asyncio import AsyncIOMotorClient

from ucloud.settings import Config
from ucloud.services.queue.base import QueueBase


class QueueMongoDB(QueueBase):
    _database = None
    _collection = None

    async def push(self, data: dict) -> dict:
        query = {
            '_id': str(uuid4()),
            'root': str(self.root),
            'data': data,
            'timestamp': datetime.utcnow()
        }

        result = await self._collection.insert_one(query)
        result = await self._collection.find_one({'_id': result.inserted_id})

        result['uid'] = result['_id']
        del result['_id']

        return result

    async def pop(self) -> dict:
        item = await self.peek()

        if isinstance(item, Response):
            return item

        query = {'_id': item.get('uid')}
        await self._collection.delete_one(query)
        return item

    async def peek(self) -> dict:
        query = {'root': str(self.root)}
        sort = [('timestamp', pymongo.ASCENDING)]

        result = await self._collection.find_one(query, sort=sort)

        if result is None:
            return Response(status_code=206)

        result['uid'] = result['_id']
        del result['_id']

        return result

    async def empty(self) -> None:
        query = {'root': str(self.root)}
        await self._collection.delete_many(query)

    async def total(self) -> dict:
        query = {'root': str(self.root)}
        total = await self._collection.count_documents(query)
        return {
            'root': self.root,
            'data': {
                'total': total
            }
        }

    @classmethod
    async def startup(cls, config: Config):
        cls._database = AsyncIOMotorClient(config.UCLOUD_QUEUE_MONGODB_PATH)
        cls._collection = cls._database.ucloud['ucloud_queue']

        await cls._collection.create_index(
            keys=[('root', pymongo.HASHED), ('timestamp', pymongo.ASCENDING)],
            name='root_hashed_timestamp_1'
        )

        await cls._collection.create_index(
            keys=[('root', pymongo.ASCENDING), ('_id', pymongo.ASCENDING)],
            name='root_1__id_1_unique',
            unique=True
        )

    @classmethod
    async def shutdown(cls, config: Config):
        cls._database = None
        cls._collection = None
