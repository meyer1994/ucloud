from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class RestResponse(BaseModel):
    uid: UUID
    root: UUID
    data: dict


class QueueResponse(BaseModel):
    uid: UUID
    root: UUID
    data: dict
    timestamp: datetime


class QueueTotal(BaseModel):
    total: int


class QueueResponseTotal(BaseModel):
    root: UUID
    data: QueueTotal


class FileResponse(BaseModel):
    uid: UUID
    root: UUID
