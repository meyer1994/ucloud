import uuid

from tests.mixins.base import BaseMixin


class TestApiQueue(BaseMixin):
    root = str(uuid.uuid4())

    def setUp(self):
        self.client.delete(f'/{self.root}/queue/empty')

    async def test_push(self):
        """ POST /{root}/queue/push returns entry """
        response = self.client.post(
            f'/{self.root}/queue/push',
            json={'hello': 'world'}
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('timestamp', data)
        self.assertDictContainsSubset({
            'uid': data.get('uid'),
            'root': self.root,
            'data': {'hello': 'world'},
        }, data)

        self._assert_total(1)

    async def test_pop(self):
        """ GET /{root}/queue/pop returns entry """
        push = self._push_data({'hello': 'world'})

        # Assert it has one item
        self._assert_total(1)

        # Pop item
        response = self.client.get(f'/{self.root}/queue/pop')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(push, data)

        # Assert it does not exist anymore
        self._assert_total(0)

    async def test_pop_204(self):
        """ GET /{root}/queue/peek returns 204 """
        self._assert_total(0)
        response = self.client.get(f'/{self.root}/queue/pop')
        self.assertEqual(response.status_code, 204)

    async def test_peek(self):
        """ GET /{root}/queue/peek returns entry """
        push = self._push_data({'hello': 'world'})

        # Assert it has one item
        self._assert_total(1)

        # Peek item
        response = self.client.get(f'/{self.root}/queue/peek')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, push)

        # Assert it was not deleted
        self._assert_total(1)

    async def test_peek_204(self):
        """ GET /{root}/queue/peek returns 204 """
        self._assert_total(0)
        response = self.client.get(f'/{self.root}/queue/peek')
        self.assertEqual(response.status_code, 204)

    async def test_empty(self):
        """ DELETE /{root}/queue/empty returns entry """
        self._push_data({'hello': 'world'})
        self._push_data({'hello': 'world'})

        # Assert it has items
        self._assert_total(2)

        # Empty it
        response = self.client.delete(f'/{self.root}/queue/empty')
        self.assertEqual(response.status_code, 204)

        # Assert is empty
        self._assert_total(0)

    async def test_total(self):
        """ GET /{root}/queue/total returns entry """
        for _ in range(10):
            self._push_data({'hello': 'world'})

        response = self.client.get(f'/{self.root}/queue/total')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(data, {
            'root': self.root,
            'data': {'total': 10}
        })

    def _assert_total(self, total: int):
        response = self.client.get(f'/{self.root}/queue/total')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(data, {
            'root': self.root,
            'data': {'total': total}
        })

    def _push_data(self, push: dict) -> str:
        response = self.client.post(f'/{self.root}/queue/push', json=push)

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('timestamp', data)
        self.assertDictContainsSubset({
            'uid': data.get('uid'),
            'root': self.root,
            'data': {'hello': 'world'},
        }, data)

        return data
