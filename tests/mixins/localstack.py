import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import boto3  # noqa
from localstack_client.patch import enable_local_endpoints, disable_local_endpoints


FAKE_ENV = {
    'AWS_ACCESS_KEY': 'local',
    'AWS_SECRET_ACCESS_KEY': 'local',
    'AWS_DEFAULT_REGION': 'us-east-1'
}


class LocalStackMixin(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        enable_local_endpoints()
        cls.addClassCleanup(disable_local_endpoints)

        mock = patch.dict(os.environ, FAKE_ENV)
        mock.start()
        cls.addClassCleanup(mock.stop)
