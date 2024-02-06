from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import instances, providers

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(instances.router, prefix="/api/instances")
app.include_router(providers.router, prefix="/api/providers")
