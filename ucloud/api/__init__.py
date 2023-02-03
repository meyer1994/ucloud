from fastapi import APIRouter

from ucloud.api.rest import router as router_rest
from ucloud.api.files import router as router_files
from ucloud.api.queue import router as router_queue
from ucloud.api.users import router as router_users


router = APIRouter(prefix='/{root}')
router.include_router(router_rest, prefix='/rest', tags=['rest'])
router.include_router(router_files, prefix='/files', tags=['files'])
router.include_router(router_queue, prefix='/queue', tags=['queue'])
router.include_router(router_users, prefix='/users', tags=['users'])
