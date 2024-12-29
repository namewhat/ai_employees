from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import UploadFile
import random
from typing import List, Optional
from app.models.base import Quote
from app.schemas.quote import QuoteCreate

async def create_quote(db: Session, quote: QuoteCreate) -> Quote:
    """创建单条语录"""
    db_quote = Quote(**quote.model_dump())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote

async def create_quotes_from_list(db: Session, quotes: List[str], source: Optional[str] = None) -> List[Quote]:
    """从字符串列表创建多条语录"""
    db_quotes = []
    for content in quotes:
        db_quote = Quote(content=content, source=source)
        db.add(db_quote)
        db_quotes.append(db_quote)
    db.commit()
    for quote in db_quotes:
        db.refresh(quote)
    return db_quotes

async def create_quotes_from_file(db: Session, file: UploadFile) -> List[Quote]:
    """从文件创建多条语录"""
    content = await file.read()
    text = content.decode('utf-8')
    quotes = [line.strip() for line in text.split('\n') if line.strip()]
    return await create_quotes_from_list(db, quotes, f"文件导入 - {file.filename}")

def get_quotes(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[Quote], int]:
    """获取语录列表"""
    total = db.query(Quote).count()
    quotes = db.query(Quote).order_by(desc(Quote.created_at)).offset(skip).limit(limit).all()
    return quotes, total

def get_random_quotes(db: Session, count: int = 5) -> List[Quote]:
    """随机获取指定数量的语录"""
    total = db.query(Quote).count()
    if total == 0:
        return []
    
    # 如果总数小于请求数，返回所有语录
    if total <= count:
        return db.query(Quote).all()
    
    # 随机选择不重复的ID
    all_ids = [id[0] for id in db.query(Quote.id).all()]
    selected_ids = random.sample(all_ids, count)
    
    return db.query(Quote).filter(Quote.id.in_(selected_ids)).all()