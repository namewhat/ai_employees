from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    source = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), nullable=False)
    source = Column(String(255))
    prompt = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # 活动类型：generate, upload, publish
    content = Column(Text, nullable=False)     # 活动描述
    created_at = Column(DateTime, default=datetime.now)

class PublishRecord(Base):
    __tablename__ = "publish_records"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    image_ids = Column(String(255))  # 逗号分隔的图片ID
    quote_ids = Column(String(255))  # 逗号分隔的语录ID
    status = Column(String(50))      # 发布状态
    created_at = Column(DateTime, default=datetime.now) 