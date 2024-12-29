from pathlib import Path
import sqlite3
import re

def execute_sql_file(cursor: sqlite3.Cursor, file_path: Path):
    sql_content = file_path.read_text(encoding='utf-8')
    # 分割多条SQL语句
    for statement in sql_content.split(';'):
        if statement.strip():
            cursor.execute(statement)

def extract_type_from_filename(filename: str) -> str:
    # 从文件名中提取类型 (例如: "w_CET4_words.sql" -> "CET4")
    match = re.search(r'w_([A-Z0-9]+)_words\.sql', filename)
    return match.group(1) if match else 'UNKNOWN'

def main():
    # 获取路径
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent
    data_dir = project_root / 'data'
    db_path = current_file.parent.parent / 'app.db'
    
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        return
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建最终的单词表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            phonetic TEXT,
            meaning TEXT,
            type TEXT,
            audio_url TEXT
        )
        ''')
        
        # 处理每个SQL文件
        for file_path in data_dir.iterdir():
            if file_path.suffix.lower() == '.sql':
                try:
                    word_type = extract_type_from_filename(file_path.name)
                    print(f"Processing {file_path.name}...")
                    
                    # 创建临时表
                    cursor.execute('''
                    CREATE TEMP TABLE IF NOT EXISTS temp_words (
                        id INTEGER PRIMARY KEY,
                        word TEXT,
                        phonetic TEXT,
                        meaning TEXT
                    )
                    ''')
                    
                    # 执行SQL文件内容
                    execute_sql_file(cursor, file_path)
                    
                    # 从临时表导入数据到主表
                    cursor.execute('''
                    INSERT OR IGNORE INTO words (word, phonetic, meaning, type, audio_url)
                    SELECT 
                        word,
                        phonetic,
                        meaning,
                        ?,
                        'https://dict.youdao.com/dictvoice?audio=' || word || '&type=1'
                    FROM temp_words
                    ''', (word_type,))
                    
                    # 获取插入的行数
                    rows_affected = cursor.rowcount
                    print(f"Imported {rows_affected} words from {word_type}")
                    
                    # 清理临时表
                    cursor.execute('DROP TABLE IF EXISTS temp_words')
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {str(e)}")
                    raise e
        
        # 提交更改
        conn.commit()
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) FROM words")
        total_words = cursor.fetchone()[0]
        print(f"\nTotal words imported: {total_words}")
        
        # 显示每种类型的单词数量
        cursor.execute('''
        SELECT type, COUNT(*) as count 
        FROM words 
        GROUP BY type
        ORDER BY count DESC
        ''')
        print("\nWords count by type:")
        for type_name, count in cursor.fetchall():
            print(f"{type_name}: {count}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main() 