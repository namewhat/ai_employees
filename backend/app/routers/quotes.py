from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.kimi_service import kimi_service
from app.schemas.quote import QuoteCreate, QuoteResponse, QuoteGenerateRequest, QuoteList
from app.crud import quote as quote_crud

router = APIRouter()

@router.post("/upload", response_model=List[QuoteResponse])
async def upload_quotes(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传TXT文件导入语录"""
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="只支持TXT文件")
    return await quote_crud.create_quotes_from_file(db, file)

@router.post("/generate", response_model=List[QuoteResponse])
async def generate_quotes(request: QuoteGenerateRequest, db: Session = Depends(get_db)):
    """使用Kimi AI生成语录"""
    quotes = await kimi_service.generate_quotes(request.prompt, request.count)
    return await quote_crud.create_quotes_from_list(db, quotes, f"Kimi AI - {request.prompt}")

@router.get("/", response_model=QuoteList)
async def get_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取语录列表"""
    quotes, total = quote_crud.get_quotes(db, skip=skip, limit=limit)
    return {"items": quotes, "total": total}

@router.get("/random", response_model=List[QuoteResponse])
async def get_random_quotes(count: int = 5, db: Session = Depends(get_db)):
    """随机获取指定数量的语录"""
    return quote_crud.get_random_quotes(db, count)