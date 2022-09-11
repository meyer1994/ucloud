from fastapi import FastAPI, Depends
from databases import Database

from ucloud.api import router
from ucloud.services import rest, files, queue
from ucloud.settings import config

app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await rest.startup(config)
    await files.startup(config)
    await queue.startup(config)


@app.on_event('shutdown')
async def shutdown():
    await rest.shutdown(config)
    await files.shutdown(config)
    await queue.shutdown(config)


@app.get('/ping')
async def ping():
    return 'pong'


from fastapi import UploadFile

@app.put('/fi')
async def fi(f: UploadFile):
    print(f)
    return 123
