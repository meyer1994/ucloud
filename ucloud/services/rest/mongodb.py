import json
from uuid import UUID, uuid4

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

        result = await self._collection.replace_one(query, values)
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

    @staticmethod
    async def startup(config: Config):
        RestMongoDB._database = AsyncIOMotorClient(config.UCLOUD_REST_MONGODB_PATH)
        RestMongoDB._collection = RestMongoDB._database.ucloud['ucloud_rest']

        keys = [('root', 1), ('_id', 1)]
        await RestMongoDB._collection.create_index(keys, unique=True)

    @staticmethod
    async def shutdown(config: Config):
        RestMongoDB._database = None
        RestMongoDB._collection = None
