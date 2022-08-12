from uuid import UUID
from typing import IO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.datastructures import UploadFile


router = APIRouter()


@router.post('/write')
async def write(root: UUID, data: UploadFile) -> UUID:
    pass

@router.get('/read/{uid}')
async def read(root: UUID, uid: UUID) -> StreamingResponse:
    pass

@router.delete('/delete/{uid}')
async def remove(root: UUID, uid: UUID) -> StreamingResponse:
    pass
