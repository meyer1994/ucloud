import uuid

from tests.mixins.server import ServerMixin


class TestApiRest(ServerMixin):
    root = str(uuid.uuid4())

    async def test_get(self):
        """ GET /{root}/rest/get/{uid} returns entry """
        uid = self._post_data({'hello': 'world'})

        response = self.client.get(f'/{self.root}/rest/get/{uid}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': uid,
            'root': self.root,
            'data': {'hello': 'world'},
        })

    async def test_get_404(self):
        """ GET /{root}/rest/get/{uid} returns 404 """
        uid = uuid.uuid4()

        response = self.client.get(f'/{self.root}/rest/get/{uid}')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('detail', data)
        self.assertRegex(data['detail'], r'Item .+ from .+ not found in .+')

    async def test_put(self):
        """ PUT /{root}/rest/put/{uid} returns entry """
        uid = self._post_data({'hello': 'world'})

        response = self.client.put(
            f'/{self.root}/rest/put/{uid}',
            json={'bye': 'world'}
        )

        response = self.client.get(f'/{self.root}/rest/get/{uid}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': uid,
            'root': self.root,
            'data': {'bye': 'world'},
        })

    async def test_put_404(self):
        """ PUT /{root}/rest/put/{uid} returns 404 """
        uid = uuid.uuid4()

        response = self.client.put(
            f'/{self.root}/rest/put/{uid}',
            json={'hello': 'world'}
        )

        self.assertEqual(response.status_code, 404)

    async def test_post(self):
        """ POST /{root}/rest/post returns new entry """
        response = self.client.post(
            f'/{self.root}/rest/post',
            json={'hello': 'world'}
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': data.get('uid'),
            'root': self.root,
            'data': {'hello': 'world'},
        })

    async def test_delete(self):
        """ DELETE /{root}/rest/delete returns old entry """
        uid = self._post_data({'hello': 'world'})

        # Deletes item
        response = self.client.delete(f'/{self.root}/rest/delete/{uid}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': uid,
            'root': self.root,
            'data': {'hello': 'world'},
        })

        # Assert it does not exist anymore
        response = self.client.get(f'/{self.root}/rest/get/{uid}')
        self.assertEqual(response.status_code, 404)

    async def test_delete_404(self):
        """ DELETE /{root}/rest/delete/{uid} returns 404 """
        uid = uuid.uuid4()

        response = self.client.delete(f'/{self.root}/rest/delete/{uid}')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('detail', data)
        self.assertRegex(data['detail'], r'Item .+ from .+ not found in .+')

    def _post_data(self, post: dict) -> str:
        response = self.client.post(f'/{self.root}/rest/post', json=post)

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertDictEqual(data, {
            'uid': data.get('uid'),
            'root': self.root,
            'data': post
        })

        return response.json().get('uid')
