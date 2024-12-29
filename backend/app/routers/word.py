from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.word_service import WordService
from app.schemas.word import WordResponse

router = APIRouter()

@router.get("/random")
def get_random_word(
    word_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取随机单词"""
    word_service = WordService(db)
    word = word_service.get_random_word(word_type)
    if not word:
        raise HTTPException(status_code=404, detail="No words found")
    return word

@router.get("/types")
def get_word_types(db: Session = Depends(get_db)):
    """获取所有单词类型"""
    word_service = WordService(db)
    return word_service.get_word_types()

@router.get("/list/{word_type}")
def get_words_by_type(
    word_type: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取指定类型的单词列表"""
    word_service = WordService(db)
    return word_service.get_words_by_type(word_type, page, per_page)

@router.get("/progress/{word_id}")
def get_word_progress(
    word_id: int,
    db: Session = Depends(get_db)
):
    """获取单词学习进度"""
    word_service = WordService(db)
    return word_service.get_word_progress(word_id)

@router.get("/daily-word")
async def get_daily_word(
    word: Optional[str] = Query(None, description="用户输入的英文单词"),
    chinese: Optional[str] = Query(None, description="用户输入的中文释义")
):
    if word or chinese:
        # 如果有用户输入，优先使用用户输入
        return await word_service.get_word_by_input(word, chinese)
    else:
        # 否则从数据库随机获取
        return await word_service.get_random_word()

@router.get("/list")
def get_word_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),  # 限制每页最多100条
    db: Session = Depends(get_db)
):
    word_service = WordService(db)
    return word_service.get_word_list(page, per_page)