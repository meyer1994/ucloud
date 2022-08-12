from fastapi import FastAPI

from ucloud.api import router


app = FastAPI()
app.include_router(router)
