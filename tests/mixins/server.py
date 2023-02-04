import time
from threading import Thread
from unittest import IsolatedAsyncioTestCase

import httpx
import uvicorn

from ucloud import app


class Server(uvicorn.Server):
    """
    Simple uvicorn server that is started in a separated thread.

    Adapted from:
        https://stackoverflow.com/a/66589593
    """

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        while not self.started:
            time.sleep(0.01)

    def stop(self):
        self.should_exit = True
        self.thread.join()


class ServerMixin(IsolatedAsyncioTestCase):
    """
    Mixin that includes a uvicorn server and client for every test
    """

    PORT = 5000

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = uvicorn.Config(app, port=cls.PORT, log_level='debug')
        cls.server = Server(cls.config)
        cls.server.start()

        cls.client = httpx.Client(base_url=f'http://localhost:{cls.PORT}')

        # Last in, first out (LIFO)
        cls.addClassCleanup(cls.server.stop)
        cls.addClassCleanup(cls.client.close)
