from typing import Optional
from pydantic import BaseModel
import datetime


class InstanceBase(BaseModel):
    region: str
    type: str
    image: str


class InstanceCreate(InstanceBase):
    expiration: int = 1


class Instance(InstanceCreate):
    label: str
    status: str
    expiration: str
    ipv4: str
    ipv6: str
