from pydantic import BaseModel
from typing import Optional

class WordBase(BaseModel):
    word: str
    phonetic: str
    meaning: str
    type: str
    audio_url: Optional[str] = None

class WordCreate(WordBase):
    pass

class WordResponse(WordBase):
    id: int

    class Config:
        from_attributes = True 