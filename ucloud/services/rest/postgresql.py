import json
from uuid import UUID, uuid4

from databases import Database

from ucloud.settings import Config
from ucloud.services.rest.base import RestBase


class RestPostgreSQL(RestBase):
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
            RETURNING *
        '''

        result = await self._database.fetch_one(query, values)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data)
        }

    @staticmethod
    async def startup(config: Config):
        RestPostgreSQL._database = Database(config.UCLOUD_REST_POSTGRESQL_PATH)
        await RestPostgreSQL._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_rest (
                root UUID,
                uid UUID,
                data JSONB,
                PRIMARY KEY (root, uid)
            )
        '''
        await RestPostgreSQL._database.execute(query)

    @staticmethod
    async def shutdown(config: Config):
        await RestPostgreSQL._database.disconnect()
        RestPostgreSQL._database = None
