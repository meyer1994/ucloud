import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import boto3  # noqa
from localstack_client.patch import enable_local_endpoints, disable_local_endpoints


FAKE_ENV = {
    'AWS_ACCESS_KEY_ID': 'localkey',
    'AWS_SECRET_ACCESS_KEY': 'localsecret',
    'AWS_DEFAULT_REGION': 'us-east-1',
}


class LocalStackMixin(IsolatedAsyncioTestCase):
    """
    Mixin that adds fake AWS credentials and enables local endpoints in
    localstack.

    It adds some basic AWS credentials to the environment and also monkey patch
    all of boto3 library

    More info about localstack check here:
        https://github.com/localstack/localstack-python-client
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        mock = patch.dict(os.environ, FAKE_ENV)
        mock.start()

        enable_local_endpoints()

        # Last in, first out (LIFO)
        cls.addClassCleanup(mock.stop)
        cls.addClassCleanup(disable_local_endpoints)
