from uuid import UUID

from fastapi import APIRouter, Depends

from ucloud.services.queue import Queue


router = APIRouter()


@router.post('/push')
async def push(data: dict, service: Queue = Depends(Queue)) -> UUID:
    return await service.push(data)


@router.get('/pop')
async def pop(service: Queue = Depends(Queue)) -> dict:
    return await service.pop()


@router.delete('/empty')
async def empty(service: Queue = Depends(Queue)) -> None:
    return await service.empty()


@router.get('/total')
async def total(service: Queue = Depends(Queue)) -> int:
    return await service.total()
