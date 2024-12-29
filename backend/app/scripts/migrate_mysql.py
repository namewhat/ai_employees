import pymysql
from pymysql.cursors import DictCursor

def migrate_database():
    try:
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='ai_employees',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        with connection.cursor() as cursor:
            # 1. 创建备份表
            print("Creating backup...")
            cursor.execute("CREATE TABLE IF NOT EXISTS words_backup LIKE words")
            cursor.execute("INSERT INTO words_backup SELECT * FROM words")
            
            # 2. 创建新表
            print("Creating new table structure...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS words_new (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    word VARCHAR(255) NOT NULL,
                    phonetic VARCHAR(255) DEFAULT '',
                    meaning TEXT,
                    type VARCHAR(50),
                    audio_url VARCHAR(255),
                    UNIQUE KEY unique_word (word)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 3. 先查找重复的单词
            print("Checking for duplicates...")
            cursor.execute("""
                SELECT word, GROUP_CONCAT(translate) as meanings, 
                       GROUP_CONCAT(word_type) as types
                FROM words 
                WHERE word IS NOT NULL AND TRIM(word) != ''
                GROUP BY word 
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()
            
            if duplicates:
                print("\nFound duplicate words:")
                for dup in duplicates:
                    print(f"Word: {dup['word']}")
                    print(f"Meanings: {dup['meanings']}")
                    print(f"Types: {dup['types']}\n")
            
            # 4. 迁移数据，对于重复的单词，合并释义和类型
            print("Migrating data...")
            cursor.execute("""
                INSERT INTO words_new (word, meaning, type, audio_url)
                SELECT 
                    TRIM(word),
                    GROUP_CONCAT(DISTINCT TRIM(translate) SEPARATOR '; '),
                    CASE 
                        WHEN COUNT(DISTINCT word_type) = 1 THEN
                            CASE word_type
                                WHEN '初中' THEN 'JUNIOR'
                                WHEN '高中' THEN 'SENIOR'
                                WHEN '四级' THEN 'CET4'
                                WHEN '六级' THEN 'CET6'
                                WHEN '考研' THEN 'GRE'
                                WHEN '托福' THEN 'TOEFL'
                                ELSE word_type
                            END
                        ELSE 'MULTIPLE'
                    END,
                    CONCAT('https://dict.youdao.com/dictvoice?audio=', TRIM(word), '&type=1')
                FROM words
                WHERE word IS NOT NULL AND TRIM(word) != ''
                GROUP BY TRIM(word)
            """)
            
            # 5. 重命名表
            print("Replacing old table...")
            cursor.execute("DROP TABLE IF EXISTS words_old")
            cursor.execute("RENAME TABLE words TO words_old")
            cursor.execute("RENAME TABLE words_new TO words")
            
            # 提交更改
            connection.commit()
            
            # 6. 显示统计信息
            cursor.execute("SELECT COUNT(*) as count FROM words")
            total = cursor.fetchone()['count']
            print(f"\nMigration completed successfully!")
            print(f"Total words in new table: {total}")
            
            # 显示每种类型的单词数量
            cursor.execute("""
                SELECT type, COUNT(*) as count 
                FROM words 
                GROUP BY type 
                ORDER BY count DESC
            """)
            print("\nWords count by type:")
            for row in cursor.fetchall():
                print(f"{row['type']}: {row['count']}")
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Rolling back changes...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS words")
                cursor.execute("RENAME TABLE words_old TO words")
                connection.commit()
        except:
            print("Rollback failed!")
    
    finally:
        if 'connection' in locals():
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    migrate_database()