from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse

from ucloud.models import FileResponse
from ucloud.services.files import Files


router = APIRouter()


@router.put('/write', status_code=201)
async def write(file: UploadFile, service: Files = Depends(Files)) -> FileResponse:
    return await service.write(file)


@router.get('/read/{uid}')
async def read(uid: UUID, service: Files = Depends(Files)) -> FastAPIFileResponse:
    return await service.read(uid)


@router.delete('/remove/{uid}', status_code=204)
async def remove(uid: UUID, service: Files = Depends(Files)) -> None:
    return await service.remove(uid)
