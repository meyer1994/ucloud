from uuid import UUID, uuid4

import pymongo
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from ucloud.settings import Config
from ucloud.services.rest.base import RestBase


class RestMongoDB(RestBase):
    _database = None
    _collection = None

    async def get(self, uid: UUID) -> dict:
        query = {
            '_id': str(uid),
            'root': str(self.root)
        }

        result = await self._collection.find_one(query)
        self._raise_404_if_none(result, uid)

        result['uid'] = result['_id']
        del result['_id']

        return result

    async def put(self, uid: UUID, data: dict) -> dict:
        query = {
            '_id': str(uid),
            'root': str(self.root)
        }

        values = {
            '_id': str(uid),
            'root': str(self.root),
            'data': data
        }

        await self._collection.replace_one(query, values)
        return await self.get(uid)

    async def post(self, data: dict) -> UUID:
        query = {
            '_id': str(uuid4()),
            'root': str(self.root),
            'data': data
        }

        result = await self._collection.insert_one(query)
        return await self.get(result.inserted_id)

    async def delete(self, uid: UUID) -> dict:
        query = {
            '_id': str(uid),
            'root': str(self.root)
        }

        result = await self.get(uid)
        await self._collection.delete_one(query)

        return result

    @classmethod
    async def startup(cls, config: Config):
        cls._database = AsyncIOMotorClient(config.UCLOUD_REST_MONGODB_PATH)
        cls._collection = cls._database.ucloud['ucloud_rest']

        await cls._collection.create_index(
            keys=[('root', pymongo.HASHED), ('_id', pymongo.ASCENDING)],
            name='root_hashed__id_1'
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

    def _raise_404_if_none(self, data: dict, uid: str):
        if data is None:
            msg = f'Item {uid} from {self.root} not found in MongoDB'
            raise HTTPException(status_code=404, detail=msg)
