from tests.mixins.server import ServerMixin


class TestPing(ServerMixin):
    async def test_ping(self):
        """ `GET /ping` returns `pong` """
        response = self.client.get('/ping')
        response = response.json()
        self.assertEqual(response, 'pong')
