from uuid import UUID
from typing import IO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.datastructures import UploadFile


router = APIRouter()


@router.post('/write')
def write(root: UUID, data: UploadFile) -> UUID:
    pass

@router.get('/read/{uid}')
def read(root: UUID, uid: UUID) -> StreamingResponse:
    pass

@router.delete('/delete/{uid}')
def remove(root: UUID, uid: UUID) -> StreamingResponse:
    pass
