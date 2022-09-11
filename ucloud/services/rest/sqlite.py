import json
from uuid import UUID, uuid4

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
        values = {
            'uid': str(uid),
            'root': str(self.root)
        }

        query = '''
            DELETE FROM ucloud_rest
            WHERE root = :root AND uid = :uid
        '''

        result = await self.get(uid)
        await self._database.execute(query, values)

        return result

    @staticmethod
    async def startup(config):
        RestSqlite._database = Database(config.UCLOUD_REST_SQLITE_PATH)
        await RestSqlite._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_rest (
                root TEXT,
                uid TEXT,
                data TEXT,
                PRIMARY KEY (root, uid)
            )
        '''
        await RestSqlite._database.execute(query)

    @staticmethod
    async def shutdown(config):
        await RestSqlite._database.disconnect()
        RestSqlite._database = None
