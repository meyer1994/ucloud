from uuid import uuid4
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock, PropertyMock

import botocore
from fastapi import HTTPException

from ucloud.services.files import FilesAwsS3


class TestServiceFilesAwsS3(IsolatedAsyncioTestCase):
    root = uuid4()

    @patch('ucloud.services.files.aws_s3.uuid4', return_value='uuid4')
    @patch.object(FilesAwsS3, '_name', new_callable=PropertyMock, return_value='_name')
    @patch.object(FilesAwsS3, '_bucket')
    async def test_write(self, _bucket, _name, uuid4):
        """ Writes file """
        data = Mock()
        service = FilesAwsS3(self.root)
        result = await service.write(data)

        uuid4\
            .assert_called_once_with()
        FilesAwsS3._bucket.upload_fileobj\
            .assert_called_once_with(data.file, f'_name/{service.root}/uuid4')

        self.assertDictEqual(result, {
            'uid': 'uuid4',
            'root': service.root,
        })

    @patch.object(FilesAwsS3, '_raise_404_if_not_exists')
    @patch.object(FilesAwsS3, '_name', new_callable=PropertyMock, return_value='_name')
    @patch.object(FilesAwsS3, '_bucket')
    async def test_read(self, _bucket, _name, _raise_404_if_not_exists):
        """ Reads file """
        data = Mock()
        service = FilesAwsS3(self.root)
        result = await service.read(data)

        service._raise_404_if_not_exists\
            .assert_called_once_with(data)
        service._bucket.Object\
            .assert_called_once_with(f'_name/{service.root}/{data}')
        service._bucket.Object().get().__getitem__\
            .assert_called_once_with('Body')

    @patch.object(FilesAwsS3, '_raise_404_if_not_exists')
    @patch.object(FilesAwsS3, '_name', new_callable=PropertyMock, return_value='_name')
    @patch.object(FilesAwsS3, '_bucket')
    async def test_remove(self, _bucket, _name, _raise_404_if_not_exists):
        """ Removes file """
        data = Mock()
        service = FilesAwsS3(self.root)
        result = await service.remove(data)

        service._raise_404_if_not_exists\
            .assert_called_once_with(data)
        service._bucket.Object\
            .assert_called_once_with(f'_name/{service.root}/{data}')
        service._bucket.Object().delete\
            .assert_called_once_with()

    @patch('ucloud.services.files.aws_s3.boto3')
    async def test_startup(self, boto3):
        """ Correctly startup """
        config = Mock()
        config.UCLOUD_FILES_AWS_S3_PATH = 's3://path'

        await FilesAwsS3.startup(config)

        boto3.resource\
            .assert_called_once_with('s3')
        boto3.resource().Bucket\
            .assert_called_once_with('path')
        boto3.resource().Bucket().create\
            .assert_called_once_with()

    @patch.object(FilesAwsS3, '_s3')
    @patch.object(FilesAwsS3, '_name')
    @patch.object(FilesAwsS3, '_bucket')
    async def test_shutdown(self, _bucket, _name, _s3):
        """ Correctly shutdown """
        config = Mock()

        await FilesAwsS3.shutdown(config)

        self.assertIsNone(FilesAwsS3._s3)
        self.assertIsNone(FilesAwsS3._name)
        self.assertIsNone(FilesAwsS3._bucket)

    @patch.object(FilesAwsS3, '_name', new_callable=PropertyMock, return_value='_name')
    @patch.object(FilesAwsS3, '_bucket')
    def test_raise_404_if_not_exists(self, _bucket, _name):
        """ Raises 404 exception if file does not exist """
        exception = botocore.exceptions.ClientError({}, None)
        FilesAwsS3._bucket.Object.return_value.load.side_effect = exception

        data = Mock()
        service = FilesAwsS3(self.root)

        with self.assertRaises(HTTPException):
            service._raise_404_if_not_exists(data)

        FilesAwsS3._bucket.Object\
            .assert_called_once_with(f'_name/{service.root}/{data}')
        FilesAwsS3._bucket.Object()\
            .load.assert_called_once_with()

    @patch.object(FilesAwsS3, '_name', new_callable=PropertyMock, return_value='_name')
    @patch.object(FilesAwsS3, '_bucket')
    def test_raise_404_if_not_exists_no_raise(self, _bucket, _name):
        """ Does not raise if file does exist """
        data = Mock()
        service = FilesAwsS3(self.root)
