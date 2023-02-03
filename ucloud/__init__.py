import asyncio

from fastapi import FastAPI

from ucloud.api import router
from ucloud.services import rest, files, queue
from ucloud.settings import config

app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await asyncio.gather(
        rest.startup(config),
        files.startup(config),
        queue.startup(config)
    )


@app.on_event('shutdown')
async def shutdown():
    await asyncio.gather(
        rest.shutdown(config),
        files.shutdown(config),
        queue.shutdown(config)
    )


@app.get('/ping')
async def ping():
    return 'pong'
