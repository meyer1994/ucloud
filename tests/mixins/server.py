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

        # Bad configurations may make uvicorn error on startup. This way, its
        # thread will be stopped. If the thread is stopped, we will throw an
        # error.
        #
        # We also wait, at most, 5 seconds for the server to start. If it does
        # not, we throw an error
        for _ in range(500):
            # Thread is dead, error on server start
            if not self.thread.is_alive():
                raise Exception('Error when starting uvicorn server')

            # Server started, we are done here
            if self.started:
                return

            time.sleep(0.01)

        raise Exception('Uvicorn server timedout on start')


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
        cls.config = uvicorn.Config(app, port=cls.PORT, log_level='trace')
        cls.server = Server(cls.config)
        cls.server.start()

        cls.client = httpx.Client(base_url=f'http://localhost:{cls.PORT}')

        # Last in, first out (LIFO)
        cls.addClassCleanup(cls.server.stop)
        cls.addClassCleanup(cls.client.close)
