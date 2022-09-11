from uuid import UUID

from fastapi import APIRouter, Depends

from ucloud.services.rest import Rest


router = APIRouter()


@router.get('/get/{uid}')
async def get(uid: UUID, service: Rest = Depends(Rest)) -> dict:
    return await service.get(uid)


@router.put('/put/{uid}')
async def put(uid: UUID, data: dict, service: Rest = Depends(Rest)) -> dict:
    return await service.put(uid, data)


@router.post('/post')
async def post(data: dict, service: Rest = Depends(Rest)) -> UUID:
    return await service.post(data)


@router.delete('/delete/{uid}')
async def delete(uid: UUID, service: Rest = Depends(Rest)) -> dict:
    return await service.delete(uid)
