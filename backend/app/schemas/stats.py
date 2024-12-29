from pydantic import BaseModel
from datetime import datetime
from typing import List

class Stats(BaseModel):
    quotes: int
    images: int
    published: int

class Activity(BaseModel):
    id: int
    type: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True 