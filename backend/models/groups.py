from pydantic import BaseModel
from datetime import datetime


class Group(BaseModel):
    id: int
    name: str
    statistics: dict
    created_at: datetime
