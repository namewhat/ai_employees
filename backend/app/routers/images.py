from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.keling_service import keling_service
from app.schemas.image import ImageCreate, ImageResponse, ImageGenerateRequest, ImageList
from app.crud import image as image_crud

router = APIRouter()

@router.post("/upload", response_model=List[ImageResponse])
async def upload_images(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """上传图片文件"""
    # 验证文件类型
    for file in files:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="只支持PNG、JPG格式的图片")
    
    return await image_crud.create_images_from_files(db, files)

@router.post("/generate", response_model=List[ImageResponse])
async def generate_images(request: ImageGenerateRequest, db: Session = Depends(get_db)):
    """使用可灵AI生成图片"""
    image_paths = await keling_service.generate_images(request.prompt, request.count)
    
    # 创建图片记录
    images = []
    for path in image_paths:
        image = ImageCreate(
            path=path,
            source="可灵AI",
            prompt=request.prompt
        )
        db_image = await image_crud.create_image(db, image)
        images.append(db_image)
    
    return images

@router.get("/", response_model=ImageList)
async def get_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取图片列表"""
    images, total = image_crud.get_images(db, skip=skip, limit=limit)
    return {"items": images, "total": total}

@router.get("/random", response_model=List[ImageResponse])
async def get_random_images(count: int = 5, db: Session = Depends(get_db)):
    """随机获取指定数量的图片"""
    return image_crud.get_random_images(db, count) 