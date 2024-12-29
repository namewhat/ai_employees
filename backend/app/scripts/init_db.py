from sqlalchemy import inspect
from app.database import engine, Base
from app.models.word import Word
from app.models.word_progress import WordProgress

def init_db():
    inspector = inspect(engine)
    
    # 获取所有已存在的表
    existing_tables = inspector.get_table_names()
    
    try:
        # 如果 word_progress 表不存在，创建所有表
        if 'word_progress' not in existing_tables:
            print("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully!")
        else:
            print("Tables already exist, skipping creation.")
            
        # 验证表是否创建成功
        tables = inspector.get_table_names()
        print("\nExisting tables:")
        for table in tables:
            print(f"- {table}")
            
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise e

if __name__ == "__main__":
    init_db() 