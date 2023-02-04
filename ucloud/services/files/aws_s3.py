import os
import shutil
from uuid import UUID, uuid4
from tempfile import SpooledTemporaryFile
from pathlib import Path

import boto3
import botocore
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from ucloud.settings import Config
from ucloud.services.files.base import FilesBase


class FilesAwsS3(FilesBase):
    _s3 = None
    _bucket = None
    _name = None

    async def write(self, data: SpooledTemporaryFile) -> dict:
        uid = uuid4()

        path = f'{self._name}/{self.root}/{uid}'
        self._bucket.upload_fileobj(data.file, path)

        return {
            'uid': uid,
            'root': self.root
        }

    async def read(self, uid: UUID) -> StreamingResponse:
        self._raise_404_if_not_exists(uid)

        path = f'{self._name}/{self.root}/{uid}'
        obj = self._bucket.Object(path)
        body = obj.get()['Body']

        return StreamingResponse(body)

    async def remove(self, uid: UUID):
        self._raise_404_if_not_exists(uid)

        path = f'{self._name}/{self.root}/{uid}'
        obj = self._bucket.Object(path)
        obj.delete()

    @classmethod
    async def startup(cls, config: Config):
        cls._name = config.UCLOUD_FILES_AWS_S3_PATH.removeprefix('s3://')
        cls._s3 = boto3.resource('s3')
        cls._bucket = cls._s3.Bucket(cls._name)
        cls._bucket.create()

    @classmethod
    async def shutdown(cls, config: Config):
        cls._s3 = None
        cls._name = None
        cls._bucket = None

    def _raise_404_if_not_exists(self, uid: str):
        path = f'{self._name}/{self.root}/{uid}'

        try:
            obj = self._bucket.Object(path)
            obj.load()
        except botocore.exceptions.ClientError as e:
            msg = f'Item {uid} from {self.root} not found in S3'
            raise HTTPException(status_code=404, detail=msg)
