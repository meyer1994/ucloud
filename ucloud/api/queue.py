from uuid import UUID

from fastapi import APIRouter, Depends

from ucloud.models import QueueResponse, QueueResponseTotal
from ucloud.services.queue import Queue


router = APIRouter()


@router.post('/push', status_code=201)
async def push(data: dict, service: Queue = Depends(Queue)) -> QueueResponse:
    return await service.push(data)


@router.get('/pop')
async def pop(service: Queue = Depends(Queue)) -> QueueResponse | None:
    return await service.pop()


@router.get('/peek')
async def peek(service: Queue = Depends(Queue)) -> QueueResponse | None:
    return await service.peek()


@router.delete('/empty', status_code=206)
async def empty(service: Queue = Depends(Queue)) -> None:
    return await service.empty()


@router.get('/total')
async def total(service: Queue = Depends(Queue)) -> QueueResponseTotal:
    return await service.total()
