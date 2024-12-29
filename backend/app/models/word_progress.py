from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class WordProgress(Base):
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"))
    last_study_time = Column(DateTime(timezone=True), server_default=func.now()) 