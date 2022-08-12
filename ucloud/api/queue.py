from uuid import UUID

from fastapi import APIRouter


router = APIRouter()


@router.post('/push')
async def push(root: UUID, data: dict) -> UUID:
    pass

@router.get('/pop')
async def pop(root: UUID, uid: UUID) -> dict:
    pass

@router.post('/empty')
async def empty(root: UUID, ) -> None:
    pass

@router.get('/total')
async def total(root: UUID, ) -> int:
    pass
