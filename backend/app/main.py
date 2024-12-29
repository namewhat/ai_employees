from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import word

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # 允许的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(word.router, prefix="/api/word")

@app.get("/")
async def root():
    return {"message": "API 服务运行正常"} 