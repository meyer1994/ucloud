import uuid

from tests.mixins.server import ServerMixin


class TestApiRest(ServerMixin):
    root = str(uuid.uuid4())

    async def test_post(self):
        """ POST /{root}/rest/post returns new entry """
        response = self.client.post(
            f'/{self.root}/rest/post',
            json={'hello': 'world'}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        uuid.UUID(data['uid'])

        self.assertEqual(data['root'], self.root)
        self.assertDictEqual(data['data'], {'hello': 'world'})

    async def test_get(self):
        """ GET /{root}/rest/get/{uid} returns entry """
        response = self.client.post(
            f'/{self.root}/rest/post',
            json={'hello': 'world'}
        )

        data = response.json()
        uid = data['uid']

        response = self.client.get(f'/{self.root}/rest/get/{uid}')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        uuid.UUID(data['uid'])

        self.assertEqual(data['root'], self.root)
        self.assertDictEqual(data['data'], {'hello': 'world'})
