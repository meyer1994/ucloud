import json
from datetime import datetime

import boto3
from fastapi import HTTPException

from ucloud.settings import Config
from ucloud.services.queue.base import QueueBase


class QueueAwsSqs(QueueBase):
    _sqs = None
    _prefix = None

    async def push(self, data: dict) -> dict:
        data = {
            'root': str(self.root),
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }

        body = json.dumps(data)
        message = self._queue.send_message(MessageBody=body)

        uid = message.get('MessageId')
        data.update(uid=uid)

        return data

    async def pop(self) -> dict:
        messages = self._queue.receive_messages(MaxNumberOfMessages=1)
        self._raise_204_if_empty(messages)
        messages[0].delete()
        return self._to_response(messages[0])

    async def peek(self) -> dict:
        messages = self._queue.receive_messages(
            MaxNumberOfMessages=1,
            AttributeNames=['SentTimestamp'],
            VisibilityTimeout=0
        )
        self._raise_204_if_empty(messages)
        return self._to_response(messages[0])

    async def empty(self) -> None:
        self._queue.purge()

    async def total(self) -> dict:
        self._queue.load()
        total = self._queue.attributes.get('ApproximateNumberOfMessages')
        return {
            'root': self.root,
            'data': {
                'total': total
            }
        }

    @classmethod
    async def startup(cls, config: Config):
        cls._sqs = boto3.resource('sqs')
        cls._prefix = config.UCLOUD_QUEUE_AWS_SQS_PATH

    @classmethod
    async def shutdown(cls, config: Config):
        cls._sqs = None
        cls._prefix = None

    @property
    def _queue(self):
        return self._sqs.create_queue(QueueName=f'{self._prefix}_{self.root}')

    def _to_response(self, message) -> dict:
        body = json.loads(message.body)
        body['uid'] = message.message_id
        return body

    def _raise_204_if_empty(self, messages: list):
        if len(messages) == 0:
            raise HTTPException(status_code=204)
