from fastapi import FastAPI

from stats.api.routers import base

app = FastAPI()

app.include_router(base.router)
