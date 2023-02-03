import json
from uuid import UUID, uuid4

from fastapi import HTTPException
from databases import Database


from ucloud.services.rest.base import RestBase


class RestSqlite(RestBase):
    _database = None

    async def get(self, uid: UUID) -> dict:
        values = {
            'uid': str(uid),
            'root': str(self.root)
        }

        query = '''
            SELECT * FROM ucloud_rest
            WHERE root = :root AND uid = :uid
        '''

        result = await self._database.fetch_one(query, values)
        self._raise_404_if_none(result, uid)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data)
        }

    async def put(self, uid: UUID, data: dict) -> dict:
        values = {
            'uid': str(uid),
            'root': str(self.root),
            'data': json.dumps(data)
        }

        query = '''
            UPDATE ucloud_rest
            SET data = :data
            WHERE root = :root AND uid = :uid
            RETURNING *
        '''

        result = await self._database.fetch_one(query, values)
        self._raise_404_if_none(result, uid)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data)
        }

    async def post(self, data: dict) -> UUID:
        values = {
            'uid': str(uuid4()),
            'root': str(self.root),
            'data': json.dumps(data)
        }

        query = '''
            INSERT INTO ucloud_rest (root, uid, data)
            VALUES (:root, :uid, :data)
            RETURNING *
        '''

        result = await self._database.fetch_one(query, values)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data)
        }

    async def delete(self, uid: UUID) -> dict:
        result = await self.get(uid)

        values = {
            'uid': str(uid),
            'root': str(self.root)
        }

        query = '''
            DELETE FROM ucloud_rest
            WHERE root = :root AND uid = :uid
        '''

        await self._database.execute(query, values)

        return result

    @classmethod
    async def startup(cls, config):
        cls._database = Database(config.UCLOUD_REST_SQLITE_PATH)
        await cls._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_rest (
                root TEXT,
                uid TEXT,
                data TEXT,
                PRIMARY KEY (root, uid)
            )
        '''
        await cls._database.execute(query)

    @classmethod
    async def shutdown(cls, config):
        await cls._database.disconnect()
        cls._database = None

    def _raise_404_if_none(self, data: dict, uid: str):
        if data is None:
            msg = f'Item {uid} from {self.root} not found in SQLite'
            raise HTTPException(status_code=404, detail=msg)
