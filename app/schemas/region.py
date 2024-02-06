from pydantic import BaseModel


class Region(BaseModel):
    id: str
    label: str
    country: str
