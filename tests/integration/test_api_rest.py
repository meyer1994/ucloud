import time
import uuid
import asyncio
from threading import Thread
from unittest import IsolatedAsyncioTestCase, mock

import httpx
import uvicorn


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        while not self.started:
            time.sleep(1e-3)
        return

    def stop(self):
        self.should_exit = True
        self.thread.join()


class BaseServerTestMixin(IsolatedAsyncioTestCase):
    PORT = 5000

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.config = uvicorn.Config('ucloud:app', port=self.PORT, log_level='error')
        self.server = Server(self.config)
        self.server.start()
        self.client = httpx.AsyncClient(base_url=f'http://localhost:{self.PORT}')

    async def asyncTearDown(self):
        await super().asyncTearDown()
        self.server.stop()


class TestPing(BaseServerTestMixin):
    async def test_ping(self):
        """ `GET /ping` returns `pong` """
        async with self.client as client:
            response = await client.get('/ping')
            response = response.json()
            self.assertEqual(response, 'pong')


class TestApiRest(BaseServerTestMixin):
    root = str(uuid.uuid4())

    async def test_post(self):
        """ `POST /{root}/rest/post` returns new entry """
        async with self.client as client:
            response = await client.post(
                f'/{self.root}/rest/post',
                json={'hello': 'world'}
            )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        uuid.UUID(data['uid'])

        self.assertEqual(data['root'], self.root)
        self.assertDictEqual(data['data'], {'hello': 'world'})

    # async def test_get(self):
    #     response = httpx.post(
    #         f'http://localhost:5000/{self.root}/rest/post',
    #         json={'hello': 'world'}
    #     )

    #     data = response.json()
    #     uid = data['uid']

    #     response = httpx.get(
    #         f'http://localhost:5000/{self.root}/rest/get/{uid}'
    #     )

    #     self.assertEqual(response.status_code, 200)

    #     data = response.json()
    #     uuid.UUID(data['uid'])

    #     self.assertEqual(data['root'], self.root)
    #     self.assertDictEqual(data['data'], {'hello': 'world'})
