from fastapi import APIRouter

from .data import router as router_data
from .files import router as router_files
from .queue import router as router_queue
from .users import router as router_users


router = APIRouter(prefix='/{root}')
router.include_router(router_data, prefix='/data')
router.include_router(router_files, prefix='/files')
router.include_router(router_queue, prefix='/queue')
router.include_router(router_users, prefix='/users')
