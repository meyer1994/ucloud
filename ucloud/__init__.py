from fastapi import FastAPI, Depends
from databases import Database

from ucloud.api import router
from ucloud.services import rest
from ucloud.settings import config

app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await rest.startup(config)


@app.on_event('shutdown')
async def shutdown():
    await rest.shutdown(config)


@app.get('/ping')
async def ping():
    return 'pong'
