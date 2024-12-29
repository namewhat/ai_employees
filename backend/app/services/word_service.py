from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, text
from app.models.word import Word
from app.models.word_progress import WordProgress
from app.scripts.update_words import get_word_details
import random

class WordService:
    def __init__(self, db: Session):
        self.db = db

    def get_random_word(self, word_type: Optional[str] = None) -> dict:
        # 构建基础查询，包含id字段
        query = self.db.query(Word.id, Word.word, Word.type)
        
        # 如果指定了类型，添加类型过滤
        if word_type:
            if word_type == 'MULTIPLE':
                query = query.filter(Word.type == 'MULTIPLE')
            else:
                query = query.filter(
                    (Word.type == word_type) | (Word.type == 'MULTIPLE')
                )
        
        # 获取学习次数最少的10个单词
        subquery = self.db.query(
            WordProgress.word_id,
            func.count(WordProgress.id).label('study_count')
        ).group_by(WordProgress.word_id).subquery()
        
        words = query.outerjoin(
            subquery, Word.id == subquery.c.word_id
        ).order_by(
            func.coalesce(subquery.c.study_count, 0)
        ).limit(10).all()
        
        if not words:
            return None
            
        # 随机选择一个单词
        selected = random.choice(words)
        
        # 从有道词典获取详细信息
        word_info = get_word_details(selected.word)
        if not word_info:
            return None
            
        # 处理释义，确保只取第一个最常用的释义
        if word_info['meaning']:
            # 处理可能的分隔符
            separators = [';', '；', ',', '，']
            meaning = word_info['meaning']
            for sep in separators:
                if sep in meaning:
                    meaning = meaning.split(sep)[0]
            word_info['meaning'] = meaning.strip()
        
        # 添加类型信息和ID
        word_info['type'] = selected.type
        word_info['id'] = selected.id
        
        # 记录学习进度
        self.record_study(selected.id)
        
        return word_info

    def record_study(self, word_id: int):
        # 记录学习进度
        progress = WordProgress(word_id=word_id)
        self.db.add(progress)
        try:
            self.db.commit()
        except:
            self.db.rollback()

    def get_word_types(self) -> List[str]:
        # 获取所有可用的单词类型
        result = self.db.execute(
            text("SELECT DISTINCT type FROM words ORDER BY type")
        )
        return [row[0] for row in result]

    def get_word_progress(self, word_id: int) -> dict:
        # 获取单词的学习进度
        result = self.db.query(
            func.count(WordProgress.id).label('study_count'),
            func.max(WordProgress.last_study_time).label('last_study')
        ).filter(WordProgress.word_id == word_id).first()
        
        return {
            'study_count': result.study_count if result else 0,
            'last_study': result.last_study if result else None
        }

    def get_words_by_type(self, word_type: str, page: int = 1, per_page: int = 20) -> dict:
        # 分页获取指定类型的单词列表
        query = self.db.query(Word)
        
        if word_type != 'ALL':
            if word_type == 'MULTIPLE':
                query = query.filter(Word.type == 'MULTIPLE')
            else:
                query = query.filter(
                    (Word.type == word_type) | (Word.type == 'MULTIPLE')
                )
        
        total = query.count()
        words = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'total': total,
            'words': [
                {
                    'id': word.id,
                    'word': word.word,
                    'phonetic': word.phonetic or "",
                    'meaning': word.meaning,
                    'type': word.type,
                    'audio_url': word.audio_url
                }
                for word in words
            ]
        }

    async def get_word_by_input(self, word: Optional[str], chinese: Optional[str]) -> dict:
        """根据用户输入返回单词信息"""
        if word:
            # 如果输入了英文单词，查找对应的中文释义
            db_word = await Word.filter(word=word).first()
            if db_word:
                return {
                    "word": db_word.word,
                    "phonetic": db_word.phonetic,
                    "translation": db_word.translation,
                    "audio_url": db_word.audio_url
                }
        elif chinese:
            # 如果输入了中文，查找对应的英文单词
            db_word = await Word.filter(translation__contains=chinese).first()
            if db_word:
                return {
                    "word": db_word.word,
                    "phonetic": db_word.phonetic,
                    "translation": db_word.translation,
                    "audio_url": db_word.audio_url
                }
        
        # 如果没有找到匹配的单词，返回空结果
        return {
            "word": word or "",
            "phonetic": "",
            "translation": chinese or "",
            "audio_url": ""
        }

    def get_word_list(self, page: int = 1, per_page: int = 20):
        try:
            # 计算总数
            total = self.db.query(Word).count()
            
            # 使用分页查询
            words = self.db.query(Word)\
                .order_by(Word.id)\
                .offset((page - 1) * per_page)\
                .limit(per_page)\
                .all()
            
            return {
                "success": True,
                "data": [
                    {
                        "id": word.id,
                        "word": word.word,
                        "translation": word.meaning,
                        "phonetic": word.phonetic or "",
                        "type": word.type
                    }
                    for word in words
                ],
                "pagination": {
                    "total": total,
                    "current_page": page,
                    "per_page": per_page,
                    "total_pages": (total + per_page - 1) // per_page
                }
            }
        except Exception as e:
            print(f"Error fetching word list: {e}")
            return {
                "success": False,
                "data": [],
                "message": str(e)
            }