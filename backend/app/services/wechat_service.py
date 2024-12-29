from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
import base64
import qrcode
from io import BytesIO

logger = logging.getLogger(__name__)

class WechatService:
    def __init__(self):
        self.driver = None
        self.cookies_file = os.path.join(settings.COOKIE_DIR, 'wechat_cookies.json')
        
    def _create_driver(self):
        """创建浏览器实例"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
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
        
    def get_qrcode(self):
        """获取登录二维码"""
        try:
            driver = self._create_driver()
            
            # 访问登录页面
            driver.get("https://mp.weixin.qq.com/")
            
            # 等待二维码出现
            qr_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "qrcode"))
            )
            
            # 获取二维码图片
            qr_img = qr_element.screenshot_as_png
            
            # 转换为base64
            qr_base64 = base64.b64encode(qr_img).decode()
            
            return {
                "url": f"data:image/png;base64,{qr_base64}",
                "key": str(int(time.time()))
            }
            
        except Exception as e:
            logger.error(f"获取二维码失败: {e}")
            raise HTTPException(status_code=500, detail="获取二维码失败")
        finally:
            if driver:
                driver.quit()
                
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
            driver.get("https://mp.weixin.qq.com/")
            
            # 添加cookies
            for cookie in cookies:
                driver.add_cookie(cookie)
                
            # 刷新页面
            driver.refresh()
            
            # 等待并检查是否存在用户头像
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "user_avatar"))
                )
                return True
            except TimeoutException:
                # 登录失效
                if os.path.exists(self.cookies_file):
                    os.remove(self.cookies_file)
                raise HTTPException(status_code=401, detail="登录已失效")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            raise HTTPException(status_code=500, detail="检查登录状态失败")
        finally:
            if driver:
                driver.quit()
                
    def publish_article(self, items, text_position):
        """发布图文"""
        driver = None
        try:
            # 检查登录状态
            self.check_login()
            
            # 创建浏览器实例
            driver = self._create_driver()
            
            # 访问发布页面
            driver.get("https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit")
            
            # 等待编辑器加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "edui-editor-body"))
            )
            
            # 上传图片并插入文字
            for item in items:
                # TODO: 实现图文合成和发布逻辑
                pass
            
            # 点击发布按钮
            publish_btn = driver.find_element(By.CLASS_NAME, "publish_btn")
            publish_btn.click()
            
            # 等待发布完成
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "publish_success"))
            )
            
            # 获取文章链接
            article_url = driver.find_element(By.CLASS_NAME, "article_url").get_attribute("href")
            
            return {
                "message": "发布成功",
                "articleUrl": article_url
            }
            
        except Exception as e:
            logger.error(f"发布图文失败: {e}")
            raise HTTPException(status_code=500, detail="发布图文失败")
        finally:
            if driver:
                driver.quit()

# 创建单例实例
wechat_service = WechatService() 