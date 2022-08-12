from uuid import UUID

from fastapi import APIRouter, Depends

from ucloud.services.users import Users


router = APIRouter()


@router.post('/create')
async def create(data: dict, service: Users = Depends(Users)) -> UUID:
    return await service.create(data)


@router.delete('/delete/{uid}')
async def delete(uid: UUID, service: Users = Depends(Users)) -> dict:
    return await service.delete(uid)


@router.post('/login')
async def login(uid: UUID, data: dict, service: Users = Depends(Users)) -> dict:
    return await service.login(uid, data)


@router.post('/logout')
async def logout(data: dict, service: Users = Depends(Users)) -> dict:
    return await service.logout(data)


@router.get('/fetch/{uid}')
async def fetch(uid: UUID, service: Users = Depends(Users)) -> dict:
    return await service.fetch(uid)
