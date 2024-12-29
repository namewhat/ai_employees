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
import shutil
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class KelingService:
    def __init__(self):
        self.driver = None
        self.cookies_file = os.path.join(settings.COOKIE_DIR, 'keling_cookies.json')
        
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
            raise HTTPException(status_code=500, detail="保存cookies失败")
            
    def _load_cookies(self):
        """从文件加载cookies"""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载cookies失败: {e}")
        return None
        
    def save_cookies(self, cookies):
        """保存新的cookies"""
        try:
            self._save_cookies(cookies)
            return True
        except Exception as e:
            logger.error(f"保存cookies失败: {e}")
            return False
            
    def check_login(self):
        """检查登录状态"""
        driver = None
        try:
            # 加载cookies
            cookies = self._load_cookies()
            if not cookies:
                raise HTTPException(status_code=401, detail="未登录")
                
            # 创建浏览器实例
            driver = self._create_driver()
                
            # 访问网站
            driver.get(settings.KELING_URL)
            
            # 添加cookies
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    logger.error(f"添加cookie失败: {e}")
                    
            # 刷新页面
            driver.refresh()
            
            # 等待并检查是否存在用户头像
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar"))
                )
                return True
            except TimeoutException:
                # 登录失效
                if os.path.exists(self.cookies_file):
                    os.remove(self.cookies_file)
                raise HTTPException(status_code=401, detail="登录已失效")
                
        except HTTPException:
            raise
        except WebDriverException as e:
            logger.error(f"浏览器操作失败: {e}")
            raise HTTPException(status_code=500, detail="浏览器操作失败")
        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            raise HTTPException(status_code=500, detail="检查登录状态失败")
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                    
    async def generate_images(self, prompt: str, count: int = 1) -> list[str]:
        """生成图片"""
        driver = None
        try:
            # 加载cookies
            cookies = self._load_cookies()
            if not cookies:
                raise HTTPException(status_code=401, detail="未登录")
                
            # 创建浏览器实例
            driver = self._create_driver()
                
            # 访问网站
            driver.get(settings.KELING_URL)
            
            # 添加cookies
            for cookie in cookies:
                driver.add_cookie(cookie)
                
            # 刷新页面
            driver.refresh()
            
            # 等待并点击创作按钮
            create_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".create-btn"))
            )
            create_btn.click()
            
            # 输入提示词
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".prompt-input"))
            )
            input_box.clear()
            input_box.send_keys(prompt)
            
            # 设置生成数量
            count_input = driver.find_element(By.CSS_SELECTOR, ".count-input")
            count_input.clear()
            count_input.send_keys(str(count))
            
            # 点击生成按钮
            generate_btn = driver.find_element(By.CSS_SELECTOR, ".generate-btn")
            generate_btn.click()
            
            # 等待生成完成
            WebDriverWait(driver, 300).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result-image"))
            )
            
            # 获取生成的图片
            image_elements = driver.find_elements(By.CSS_SELECTOR, ".result-image")
            image_paths = []
            
            for i, img in enumerate(image_elements[:count]):
                # 获取图片URL
                img_url = img.get_attribute("src")
                
                # 下载图片
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    # 生成文件名
                    filename = f"keling_{int(time.time())}_{i}.png"
                    filepath = os.path.join(settings.IMAGE_DIR, filename)
                    
                    # 保存图片
                    with open(filepath, 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
                        
                    # 添加相对路径
                    image_paths.append(os.path.join("images", filename))
            
            return image_paths
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"生成图片失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

# 创建单例实例
keling_service = KelingService() 