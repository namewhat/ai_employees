from fastapi import APIRouter, HTTPException
from app.services.wechat_service import wechat_service
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PublishItem(BaseModel):
    quote: str
    image: str

class PublishRequest(BaseModel):
    items: List[PublishItem]
    textPosition: str

@router.get("/qrcode")
async def get_qrcode():
    """获取登录二维码"""
    return wechat_service.get_qrcode()

@router.get("/status")
async def check_login():
    """检查登录状态"""
    wechat_service.check_login()
    return {"message": "已登录"}

@router.post("/publish")
async def publish_article(request: PublishRequest):
    """发布图文"""
    return wechat_service.publish_article(request.items, request.textPosition)