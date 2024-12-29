from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ImageBase(BaseModel):
    path: str = Field(..., description="图片路径")
    source: Optional[str] = Field(None, description="图片来源")
    prompt: Optional[str] = Field(None, description="生成提示词")

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., description="生成提示词")
    count: int = Field(default=1, ge=1, le=4, description="生成数量")

class ImageList(BaseModel):
    items: List[ImageResponse]
    total: int 