from pydantic import BaseModel, Field
from typing import List

class PublishItem(BaseModel):
    quote: str = Field(..., description="语录内容")
    image: str = Field(..., description="图片路径")

class PublishRequest(BaseModel):
    items: List[PublishItem]
    textPosition: str = Field(..., description="文字位置")

class PublishResponse(BaseModel):
    message: str
    articleUrl: str 