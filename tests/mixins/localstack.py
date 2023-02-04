from unittest import IsolatedAsyncioTestCase

import boto3  # noqa
from localstack_client.patch import enable_local_endpoints, disable_local_endpoints


class LocalStackMixin(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        enable_local_endpoints()
        cls.addClassCleanup(disable_local_endpoints)
