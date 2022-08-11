from uuid import UUID

from fastapi import APIRouter


router = APIRouter()


@router.post('/push')
def push(root: UUID, data: dict) -> UUID:
    pass

@router.get('/pop')
def pop(root: UUID, uid: UUID) -> dict:
    pass

@router.post('/empty')
def empty(root: UUID, ) -> None:
    pass

@router.get('/total')
def total(root: UUID, ) -> int:
    pass
