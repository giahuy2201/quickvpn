from fastapi import FastAPI

from app.routers import instances

app = FastAPI()

app.include_router(instances.router, prefix="/api/instances")
