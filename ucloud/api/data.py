from uuid import UUID

from fastapi import APIRouter


router = APIRouter()


@router.get('/get/{uid}')
def get(root: UUID, uid: UUID) -> dict:
    pass

@router.put('/get/{uid}')
def put(root: UUID, uid: UUID, data: dict) -> dict:
    pass

@router.post('/post')
def post(root: UUID, data: dict) -> UUID:
    pass

@router.delete('/delete/{uid}')
def delete(root: UUID, uid: UUID) -> dict:
    pass
