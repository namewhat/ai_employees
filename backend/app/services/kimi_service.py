from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import HTTPException
from app.core.config import settings
import time
import logging
import json
import os

logger = logging.getLogger(__name__)

class KimiService:
    def __init__(self):
        self.driver = None
        self.cookies_file = os.path.join(settings.COOKIE_DIR, 'kimi_cookies.json')
        
    def _create_driver(self):
        """创建浏览器实例"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--start-maximized')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
        
    def _save_cookies(self, cookies):
        """保存cookies到文件"""
        try:
            os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f)
        except Exception as e:
            logger.error(f"保存cookies失败: {e}")
            raise HTTPException(status_code=500, detail="保存登录状态失败")
            
    def _load_cookies(self):
        """从文件加载cookies"""
        try:
            if not os.path.exists(self.cookies_file):
                return None
            with open(self.cookies_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载cookies失败: {e}")
            return None
            
    def check_login(self):
        """检查登录状态"""
        try:
            driver = self._create_driver()
            
            # 先访问主页
            driver.get(settings.KIMI_URL)
            
            # 加载cookies
            cookies = self._load_cookies()
            if not cookies:
                raise HTTPException(status_code=401, detail="未登录")
                
            # 添加cookies
            for cookie in cookies:
                driver.add_cookie(cookie)
                
            # 刷新页面
            driver.refresh()
            
            # 等待并检查登录状态
            try:
                # 等待聊天输入框出现，这表示已登录
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".chat-input"))
                )
                return True
            except TimeoutException:
                # 如果超时未找到元素，说明未登录
                raise HTTPException(status_code=401, detail="未登录")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if driver:
                driver.quit()
                
    def save_cookies(self, cookies_str):
        """保存登录cookies"""
        try:
            # 解析 document.cookie 格式的字符串
            cookies = []
            for cookie in cookies_str.split(';'):
                cookie = cookie.strip()
                if cookie:
                    name, value = cookie.split('=', 1)
                    cookies.append({
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': '.moonshot.cn'
                    })
            self._save_cookies(cookies)
        except Exception as e:
            logger.error(f"保存cookies失败: {e}")
            raise HTTPException(status_code=500, detail="保存登录状态失败")

    def generate_quotes(self, prompt: str, count: int = 10):
        """生成语录"""
        driver = None
        try:
            driver = self._create_driver()
            
            # 访问主页
            driver.get(settings.KIMI_URL)
            
            # 加载cookies
            cookies = self._load_cookies()
            if not cookies:
                raise HTTPException(status_code=401, detail="未登录")
            
            # 添加cookies
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            # 刷新页面
            driver.refresh()
            
            # 等待输入框加载
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".chat-input"))
            )
            
            # 输入提示词
            prompt_text = f'请生成{count}条关于"{prompt}"的优质语录，直接输出语录内容，每条语录用换行分隔，不要带序号。'
            input_box.send_keys(prompt_text)
            
            # 点击发送按钮
            send_btn = driver.find_element(By.CSS_SELECTOR, ".send-btn")
            send_btn.click()
            
            # 等待回复完成
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".message-done"))
            )
            
            # 获取最后一条回复
            last_message = driver.find_elements(By.CSS_SELECTOR, ".message-content")[-1]
            content = last_message.text
            
            # 分割并清理语录
            quotes = [
                line.strip()
                for line in content.split('\n')
                if line.strip() and not line.strip().isdigit()
            ]
            
            return quotes[:count]
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"生成语录失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

# 创建单例实例
kimi_service = KimiService() 