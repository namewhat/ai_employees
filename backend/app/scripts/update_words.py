import requests
import time
import json
from sqlalchemy.orm import Session
from app.database import engine
from app.models.word import Word
from typing import Optional

class YoudaoDict:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1878227274@10.105.137.203;'  # 添加Cookie可能有助于提高成功率
        })

    def get_word_info(self, word: str, max_retries: int = 3) -> Optional[dict]:
        for attempt in range(max_retries):
            try:
                url = f'https://dict.youdao.com/jsonapi?q={word}&dicts={"{"}"count":99,"dicts":[["ec"]]{"}"}'
                response = self.session.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                result = {
                    'word': word,
                    'phonetic': '',
                    'meaning': '',
                    'audio_url': f'https://dict.youdao.com/dictvoice?audio={word}&type=1'
                }

                # 检查词典数据
                if 'ec' in data and 'word' in data['ec']:
                    entries = data['ec']['word'][0]
                    
                    # 获取音标
                    if 'ukphone' in entries:
                        result['phonetic'] = f"/{entries['ukphone']}/"
                    elif 'phone' in entries:
                        result['phonetic'] = f"/{entries['phone']}/"
                    
                    # 获取释义 - 只取第一个（最常用的）释义
                    if 'trs' in entries and entries['trs']:
                        for tr in entries['trs']:
                            if 'tr' in tr and tr['tr']:
                                for t in tr['tr']:
                                    if 'l' in t and 'i' in t['l']:
                                        meaning = t['l']['i'][0]
                                        # 处理可能的分隔符
                                        separators = [';', '；', ',', '，']
                                        for sep in separators:
                                            if sep in meaning:
                                                meaning = meaning.split(sep)[0]
                                        result['meaning'] = meaning.strip()
                                        break
                                if result['meaning']:
                                    break

                # 如果主API没有找到释义，尝试备用API
                if not result['meaning']:
                    backup_url = f'https://dict.youdao.com/suggest?q={word}&num=1&doctype=json'
                    backup_response = self.session.get(backup_url, timeout=5)
                    backup_data = backup_response.json()
                    
                    if 'entries' in backup_data and backup_data['entries']:
                        entry = backup_data['entries'][0]
                        if 'explain' in entry:
                            meaning = entry['explain']
                            # 处理可能的分隔符
                            separators = [';', '；', ',', '，']
                            for sep in separators:
                                if sep in meaning:
                                    meaning = meaning.split(sep)[0]
                            result['meaning'] = meaning.strip()

                # 验证结果
                if result['phonetic'] or result['meaning']:
                    return result
                
                # 如果还是没有数据，等待后重试
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))
                    continue
                
                print(f"Warning: No data found for word '{word}' after {max_retries} attempts")
                return result

            except Exception as e:
                print(f"Attempt {attempt + 1} failed for word '{word}': {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))
                    continue
                print(f"Error: Failed to fetch info for word '{word}' after {max_retries} attempts")
                return None

def get_word_details(word: str) -> Optional[dict]:
    """获取单词详细信息的公共函数"""
    youdao = YoudaoDict()
    result = youdao.get_word_info(word)
    
    # 如果获取失败，返回基本信息
    if not result:
        return {
            'word': word,
            'phonetic': '',
            'meaning': '获取释义失败',
            'audio_url': f'https://dict.youdao.com/dictvoice?audio={word}&type=1'
        }
    
    return result

if __name__ == "__main__":
    # 测试函数
    test_words = ["hello", "world", "abed", "computer", "python"]
    for word in test_words:
        print(f"\nTesting word: {word}")
        result = get_word_details(word)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        time.sleep(1)  # 避免请求过快 