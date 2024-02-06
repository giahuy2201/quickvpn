from fastapi import FastAPI

from app.routers import instances, providers

app = FastAPI()

app.include_router(instances.router, prefix="/api/instances")
app.include_router(providers.router, prefix="/api/providers")
