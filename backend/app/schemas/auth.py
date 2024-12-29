from pydantic import BaseModel, Field

class CookieData(BaseModel):
    cookies: str = Field(..., description="Cookie字符串") 