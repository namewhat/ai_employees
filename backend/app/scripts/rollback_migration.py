import pandas as pd
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')

def rollback_migration():
    try:
        # 创建数据库连接
        mysql_url = "mysql+pymysql://root:123456@localhost/ai_employees?charset=utf8mb4"
        engine = create_engine(mysql_url)
        
        with engine.connect() as conn:
            # 检查备份表是否存在
            result = conn.execute(text("SHOW TABLES LIKE 'words_old'"))
            if not result.fetchone():
                print("Error: Backup table 'words_old' not found!")
                return
            
            print("Starting rollback process...")
            
            # 删除当前的 words 表
            conn.execute(text("DROP TABLE IF EXISTS words"))
            
            # 将备份表恢复为主表
            conn.execute(text("RENAME TABLE words_old TO words"))
            
            conn.commit()
            
            # 验证数据
            df = pd.read_sql('SELECT * FROM words', engine)
            print("\nRollback completed successfully!")
            print(f"Total words restored: {len(df)}")
            
            print("\nWords count by type:")
            type_counts = df['word_type'].value_counts()
            for type_name, count in type_counts.items():
                print(f"{type_name}: {count}")
            
    except Exception as e:
        print(f"Error during rollback: {str(e)}")
    
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    rollback_migration() 