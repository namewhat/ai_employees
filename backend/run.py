import uvicorn
from app.scripts.init_db import init_db

if __name__ == "__main__":
    # 初始化数据库
    init_db()
    
    # 启动服务
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 