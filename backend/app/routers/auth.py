from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.kimi_service import kimi_service
from app.services.keling_service import keling_service
from app.schemas.auth import CookieData

router = APIRouter()

@router.get("/kimi/status")
async def check_kimi_status():
    """检查 Kimi 登录状态"""
    try:
        kimi_service.check_login()
        return {"message": "已登录"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keling/status")
async def check_keling_status():
    """检查可灵登录状态"""
    try:
        keling_service.check_login()
        return {"message": "已登录"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/kimi/cookies")
async def save_kimi_cookies(data: CookieData):
    """保存 Kimi Cookies"""
    try:
        kimi_service.save_cookies(data.cookies)
        return {"message": "保存成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keling/cookies")
async def save_keling_cookies(data: CookieData):
    """保存可灵 Cookies"""
    try:
        keling_service.save_cookies(data.cookies)
        return {"message": "保存成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 