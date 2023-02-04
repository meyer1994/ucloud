from tests.mixins.base import BaseMixin


class TestPing(BaseMixin):
    async def test_ping(self):
        """ `GET /ping` returns `pong` """
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, 'pong')
