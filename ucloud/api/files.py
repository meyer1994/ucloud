from uuid import UUID
from typing import IO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.datastructures import UploadFile

from ucloud.services.files import Files


router = APIRouter()


@router.post('/write')
async def write(data: UploadFile, service: Files = Depends(Files)) -> UUID:
    return await service.write(data)


@router.get('/read/{uid}')
async def read(uid: UUID, service: Files = Depends(Files)) -> StreamingResponse:
    return await service.read(uid)


@router.delete('/delete/{uid}')
async def remove(uid: UUID, service: Files = Depends(Files)):
    return await service.remove(uid)
