from uuid import UUID

from fastapi import APIRouter


router = APIRouter()


@router.post('/create')
def create(root: UUID, data: dict) -> UUID:
    pass

@router.delete('/delete/{uid}')
def delete(root: UUID, uid: UUID) -> dict:
    pass

@router.post('/login')
def login(root: UUID, data: dict) -> dict:
    pass

@router.post('/logout')
def logout(root: UUID, data: dict) -> dict:
    pass

@router.get('/fetch/{uid}')
def fetch(root: UUID, uid: UUID) -> dict:
    pass
