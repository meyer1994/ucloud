from uuid import UUID

from fastapi import APIRouter, Depends

from ucloud.models import RestResponse
from ucloud.services.rest import Rest


router = APIRouter()


@router.get('/get/{uid}')
async def get(uid: UUID, service: Rest = Depends(Rest)) -> RestResponse:
    return await service.get(uid)


@router.put('/put/{uid}')
async def put(uid: UUID, data: dict, service: Rest = Depends(Rest)) -> RestResponse:
    return await service.put(uid, data)


@router.post('/post', status_code=201)
async def post(data: dict, service: Rest = Depends(Rest)) -> RestResponse:
    return await service.post(data)


@router.delete('/delete/{uid}')
async def delete(uid: UUID, service: Rest = Depends(Rest)) -> RestResponse:
    return await service.delete(uid)
