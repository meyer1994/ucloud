import json
from uuid import UUID, uuid4

from fastapi import HTTPException
from databases import Database

from ucloud.settings import Config
from ucloud.services.rest.sqlite import RestSqlite


class RestPostgreSQL(RestSqlite):
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
        self._raise_404_if_none(result, uid)

        return {
            'uid': result.uid,
            'root': result.root,
            'data': json.loads(result.data)
        }

    @classmethod
    async def startup(cls, config: Config):
        cls._database = Database(config.UCLOUD_REST_POSTGRESQL_PATH)
        await cls._database.connect()

        query = '''
            CREATE TABLE IF NOT EXISTS ucloud_rest (
                root UUID,
                uid UUID,
                data JSONB,
                PRIMARY KEY (root, uid)
            )
        '''
        await cls._database.execute(query)
