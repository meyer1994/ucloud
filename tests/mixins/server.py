import time
from threading import Thread
from unittest import IsolatedAsyncioTestCase

import httpx
import uvicorn


class Server(uvicorn.Server):
    """
    Simple uvicorn server that is started in a separated thread.

    Adapted from:
        https://stackoverflow.com/a/66589593
    """

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


class ServerMixin(IsolatedAsyncioTestCase):
    """
    Mixin that includes a uvicorn server and client for every test
    """

    PORT = 5000

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.config = uvicorn.Config('ucloud:app', port=self.PORT, log_level='error')
        self.server = Server(self.config)
        self.server.start()
        self.client = httpx.Client(base_url=f'http://localhost:{self.PORT}')

    async def asyncTearDown(self):
        await super().asyncTearDown()
        self.server.stop()
