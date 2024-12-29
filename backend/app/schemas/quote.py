from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class QuoteBase(BaseModel):
    content: str = Field(..., description="语录内容")
    source: Optional[str] = Field(None, description="语录来源")

class QuoteCreate(QuoteBase):
    pass

class QuoteResponse(QuoteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuoteGenerateRequest(BaseModel):
    prompt: str = Field(..., description="生成提示词")
    count: int = Field(default=10, ge=1, le=20, description="生成数量")

class QuoteList(BaseModel):
    items: List[QuoteResponse]
    total: int