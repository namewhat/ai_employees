from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import UploadFile
import random
import os
import shutil
from typing import List, Optional
from app.models.base import Image
from app.schemas.image import ImageCreate
from app.core.config import settings

async def create_image(db: Session, image: ImageCreate) -> Image:
    """创建单张图片记录"""
    db_image = Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

async def create_images_from_files(db: Session, files: List[UploadFile], source: Optional[str] = None) -> List[Image]:
    """从上传文件创建多张图片记录"""
    db_images = []
    
    # 确保图片目录存在
    os.makedirs(settings.IMAGE_DIR, exist_ok=True)
    
    for file in files:
        # 生成文件名
        ext = os.path.splitext(file.filename)[1]
        filename = f"{random.randint(10000000, 99999999)}{ext}"
        filepath = os.path.join(settings.IMAGE_DIR, filename)
        
        # 保存文件
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 创建数据库记录
        relative_path = os.path.join("images", filename)
        db_image = Image(
            path=relative_path,
            source=source or f"文件上传 - {file.filename}"
        )
        db.add(db_image)
        db_images.append(db_image)
    
    db.commit()
    for image in db_images:
        db.refresh(image)
    return db_images

def get_images(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[Image], int]:
    """获取图片列表"""
    total = db.query(Image).count()
    images = db.query(Image).order_by(desc(Image.created_at)).offset(skip).limit(limit).all()
    return images, total

def get_random_images(db: Session, count: int = 5) -> List[Image]:
    """随机获取指定数量的图片"""
    total = db.query(Image).count()
    if total == 0:
        return []
    
    # 如果总数小于请求数，返回所有图片
    if total <= count:
        return db.query(Image).all()
    
    # 随机选择不重复的ID
    all_ids = [id[0] for id in db.query(Image.id).all()]
    selected_ids = random.sample(all_ids, count)
    
    return db.query(Image).filter(Image.id.in_(selected_ids)).all() 