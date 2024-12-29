from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.base import Quote, Image, Activity
from app.schemas.stats import Stats, Activity as ActivitySchema
from typing import List

router = APIRouter()

@router.get("/", response_model=Stats)
async def get_stats(db: Session = Depends(get_db)):
    """获取统计数据"""
    quotes_count = db.query(Quote).count()
    images_count = db.query(Image).count()
    published_count = db.query(Activity).filter(Activity.type == "publish").count()
    
    return {
        "quotes": quotes_count,
        "images": images_count,
        "published": published_count
    }

@router.get("/activities", response_model=List[ActivitySchema])
async def get_activities(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取最近活动"""
    activities = db.query(Activity)\
        .order_by(Activity.created_at.desc())\
        .limit(limit)\
        .all()
    return activities 