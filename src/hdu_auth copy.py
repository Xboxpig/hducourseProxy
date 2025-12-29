import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class HduCrawler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # 精准路径（基于你之前测试成功的 CSS 路径）
        self.SELECTORS = {
            "user": "html > body > app-root > app-right-root > rg-page-container > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > app-login-auth-panel > div > div > app-login-normal > div > div:nth-of-type(2) > form > div > nz-input-group > input",
            "pass": "html > body > app-root > app-right-root > rg-page-container > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > app-login-auth-panel > div > div > app-login-normal > div > div:nth-of-type(2) > form > div:nth-of-type(2) > nz-input-group > input",
            "btn":  "html > body > app-root > app-right-root > rg-page-container > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > app-login-auth-panel > div > div > app-login-normal > div > div:nth-of-type(2) > form > div:nth-of-type(6) > div > button"
        }
        self.driver = self._init_driver()

    def _init_driver(self):
        opts = Options()
        # 核心配置：开启性能日志以捕获网络请求标头
        opts.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        return driver

    def get_session_credentials(self):
        try:
            print("[*] 正在加载页面并启动监听...")
            self.driver.get("https://course.hdu.edu.cn")
            
            wait = WebDriverWait(self.driver, 20)
            
            # 1. 执行登录逻辑
            user_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELECTORS["user"])))
            pass_el = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS["pass"])
            btn_el = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS["btn"])

            print(f"[*] 填充账号并登录...")
            self.driver.execute_script("""
                const fill = (el, val) => {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                };
                fill(arguments[0], arguments[2]);
                fill(arguments[1], arguments[3]);
            """, user_el, pass_el, self.username, self.password)
            
            time.sleep(0.5)
            btn_el.click()

            # 2. 关键：进入域名后，通过分析网络日志截获 Token
            print("[*] 正在监控网络流量以拦截 jwt-token...")
            jwt_token = None
            
            # 循环检查，直到抓到含有 jwt-token 的请求
            start_time = time.time()
            while time.time() - start_time < 30: # 最多监听 30 秒
                logs = self.driver.get_log('performance')
                for entry in logs:
                    log = json.loads(entry['message'])['message']
                    # 寻找“请求即将发送”的事件
                    if log.get('method') == 'Network.requestWillBeSent':
                        headers = log['params']['request'].get('headers', {})
                        # 检查你提到的 fetch 请求中的标头
                        if 'jwt-token' in headers:
                            jwt_token = headers['jwt-token']
                            print(f"[✓] 成功在 API 请求中捕获到 Token!")
                            break
                
                if jwt_token:
                    break
                time.sleep(1)

            # 3. 提取 Cookie
            all_cookies = self.driver.get_cookies()
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in all_cookies])
            
            return jwt_token, cookie_str

        except Exception as e:
            print(f"[X] 截获失败: {e}")
            return None, None
        finally:
            self.driver.quit()

if __name__ == "__main__":
    USER = "23060909"
    PWD = "lT80806a?"
    
    crawler = HduCrawler(USER, PWD)
    token, cookie = crawler.get_session_credentials()
    
    if token:
        print("\n" + "="*60)
        print(f"CAPTURED_TOKEN: {token}")
        print(f"CAPTURED_COOKIE: {cookie}")
        print("="*60)
        
        # 存入 json 供后续 API 使用
        with open("session.json", "w") as f:
            json.dump({"jwt-token": token, "cookie": cookie}, f)
    else:
        print("[X] 未能拦截到有效的 jwt-token")