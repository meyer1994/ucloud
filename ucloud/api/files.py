from uuid import UUID
from typing import IO

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

from ucloud.services.files import Files


router = APIRouter()


@router.put('/write')
async def write(data: UploadFile, service: Files = Depends(Files)) -> UUID:
    return await service.write(data)


@router.get('/read/{uid}')
async def read(uid: UUID, service: Files = Depends(Files)) -> FileResponse:
    return await service.read(uid)


@router.delete('/remove/{uid}')
async def remove(uid: UUID, service: Files = Depends(Files)) -> None:
    return await service.remove(uid)
