from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), unique=True, index=True)
    phonetic = Column(String(255))
    meaning = Column(Text)
    type = Column(String(50))
    audio_url = Column(String(255))