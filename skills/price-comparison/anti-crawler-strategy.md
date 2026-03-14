# 电商平台反爬虫机制应对策略

> **文档类型**: 技术研究报告  
> **适用场景**: PriceComparison SKILL 反爬对抗  
> **版本**: v1.0  
> **更新日期**: 2026-03-13  
> **法律声明**: 本研究仅供学习交流，请遵守各平台服务条款和 robots.txt 协议

---

## 目录

1. [电商平台反爬机制概览](#一电商平台反爬机制概览)
2. [常见反爬手段分析](#二常见反爬手段分析)
3. [应对策略体系](#三应对策略体系)
4. [各平台特殊应对](#四各平台特殊应对)
5. [技术实现方案](#五技术实现方案)
6. [合规与风险控制](#六合规与风险控制)
7. [推荐架构设计](#七推荐架构设计)

---

## 一、电商平台反爬机制概览

### 1.1 反爬目的

电商平台部署反爬机制的核心目的：
- **保护商业数据**: 价格、库存、销量等核心商业信息
- **防止恶意竞争**: 阻止竞争对手批量获取数据
- **保障用户体验**: 避免爬虫占用过多服务器资源
- **防范欺诈行为**: 防止虚假交易、刷单等

### 1.2 反爬层级

```
┌─────────────────────────────────────────┐
│  Layer 4: 业务层反爬                     │
│  - 验证码、滑块、点选验证                 │
│  - 登录态检测、行为分析                   │
├─────────────────────────────────────────┤
│  Layer 3: 应用层反爬                     │
│  - 请求频率限制、IP封禁                   │
│  - User-Agent检测、Cookie验证             │
├─────────────────────────────────────────┤
│  Layer 2: 传输层反爬                     │
│  - TLS指纹检测、HTTP/2指纹                │
│  - 协议特征分析                           │
├─────────────────────────────────────────┤
│  Layer 1: 网络层反爬                     │
│  - IP黑名单、地理围栏                     │
│  - CDN防护、WAF拦截                       │
└─────────────────────────────────────────┘
```

---

## 二、常见反爬手段分析

### 2.1 请求层面检测

| 检测维度 | 检测内容 | 触发条件 |
|---------|---------|---------|
| **IP频率** | 同一IP请求次数 | >100次/分钟 |
| **User-Agent** | 浏览器指纹 | 非标准UA或缺失 |
| **Referer** | 来源页面 | 直接访问无Referer |
| **Cookie** | 会话状态 | 缺失或异常 |
| **请求头** | 完整性检查 | 缺少Accept等标准头 |

### 2.2 行为层面检测

| 检测维度 | 检测内容 | 触发条件 |
|---------|---------|---------|
| **访问模式** | 请求路径规律 | 固定间隔、固定顺序 |
| **鼠标轨迹** | 人机交互验证 | 无鼠标移动直接点击 |
| **页面停留** | 停留时间 | <1秒即跳转 |
| **滚动行为** | 页面滚动检测 | 无滚动直接请求下一页 |
| **点击热区** | 点击位置分析 | 点击坐标规律性 |

### 2.3 验证码类型

```
验证码类型演进:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  传统验证码  │ → │  滑块验证码  │ → │  行为验证码  │
│  数字/字母   │    │  滑动拼图    │    │  无感验证    │
└─────────────┘    └─────────────┘    └─────────────┘
       ↓                  ↓                  ↓
   容易识别            需要模拟            AI行为分析
   (OCR解决)          (轨迹模拟)          (极难绕过)
```

**主流验证码服务商**:
- 极验 (Geetest) - 滑块、点选、行为验证
- 阿里云验证码 - 智能验证、无痕验证
- 腾讯云验证码 - 滑块、文字点选
- 网易易盾 - 行为式验证码

### 2.4 各平台反爬特点

#### 京东 (JD)
| 反爬手段 | 强度 | 应对难度 |
|---------|------|---------|
| IP频率限制 | ⭐⭐⭐ | 中等 |
| 滑块验证码 | ⭐⭐⭐⭐ | 较难 |
| 登录态检测 | ⭐⭐⭐⭐⭐ | 难 |
| 数据加密 | ⭐⭐⭐⭐ | 较难 |

**特点**: 
- 搜索接口需要 `__jda` 等Cookie参数
- 价格数据有时通过 separate API 返回
- 频繁访问会触发滑块验证

#### 淘宝/天猫 (Taobao/Tmall)
| 反爬手段 | 强度 | 应对难度 |
|---------|------|---------|
| 滑块验证码 | ⭐⭐⭐⭐⭐ | 很难 |
| 登录态检测 | ⭐⭐⭐⭐⭐ | 很难 |
| 数据混淆 | ⭐⭐⭐⭐ | 较难 |
| 风控系统 | ⭐⭐⭐⭐⭐ | 极难 |

**特点**:
- 阿里系风控系统非常严格
- 需要淘宝账号登录态
- 价格数据动态加载，需要执行JS
- 有专门的反爬团队

#### 拼多多 (PDD)
| 反爬手段 | 强度 | 应对难度 |
|---------|------|---------|
| 防抓包 | ⭐⭐⭐⭐ | 较难 |
| 数据加密 | ⭐⭐⭐⭐ | 较难 |
| 设备指纹 | ⭐⭐⭐⭐ | 较难 |
| 行为检测 | ⭐⭐⭐ | 中等 |

**特点**:
- App端API更难抓取
- 使用 protobuf 加密传输
- 需要模拟设备指纹

#### 亚马逊 (Amazon)
| 反爬手段 | 强度 | 应对难度 |
|---------|------|---------|
| IP限制 | ⭐⭐⭐ | 中等 |
| 验证码 | ⭐⭐⭐ | 中等 |
| 数据一致性检查 | ⭐⭐⭐⭐ | 较难 |
| 机器人检测 | ⭐⭐⭐⭐ | 较难 |

**特点**:
- 对国外IP相对宽松
- 会返回不一致数据迷惑爬虫
- 需要处理Cookie和Session

---

## 三、应对策略体系

### 3.1 基础策略层

#### 3.1.1 请求头伪装
```python
# 标准浏览器请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}
```

#### 3.1.2 IP代理池
```python
# 代理池架构
class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.failed_proxies = set()
    
    def get_proxy(self):
        """获取可用代理"""
        # 轮换策略：随机、轮询、加权
        pass
    
    def mark_failed(self, proxy):
        """标记失效代理"""
        self.failed_proxies.add(proxy)
    
    def validate_proxy(self, proxy):
        """验证代理可用性"""
        # 测试访问目标网站
        pass
```

**代理类型选择**:
| 代理类型 | 匿名度 | 稳定性 | 成本 | 适用场景 |
|---------|--------|--------|------|---------|
| 数据中心代理 | 低 | 高 | 低 | 低频抓取 |
| 住宅代理 | 高 | 中 | 高 | 高频抓取 |
| 移动代理 | 极高 | 中 | 极高 | 严格风控平台 |

#### 3.1.3 请求频率控制
```python
import random
import time

class RequestThrottler:
    def __init__(self, min_delay=1, max_delay=5):
        self.min_delay = min_delay
        self.max_delay = max_delay
    
    def wait(self):
        """随机延迟，模拟人类行为"""
        # 正态分布延迟更自然
        delay = random.gauss(3, 1)
        delay = max(self.min_delay, min(self.max_delay, delay))
        time.sleep(delay)
    
    def adaptive_wait(self, response_time):
        """根据响应时间自适应调整"""
        base_delay = random.uniform(2, 5)
        # 响应慢时增加延迟，避免被封
        if response_time > 2:
            base_delay += random.uniform(1, 3)
        time.sleep(base_delay)
```

### 3.2 中级策略层

#### 3.2.1 Cookie管理
```python
import pickle
from pathlib import Path

class CookieManager:
    def __init__(self, storage_dir="cookies"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def save_cookies(self, platform, cookies):
        """保存Cookie到文件"""
        cookie_file = self.storage_dir / f"{platform}.pkl"
        with open(cookie_file, 'wb') as f:
            pickle.dump(cookies, f)
    
    def load_cookies(self, platform):
        """加载Cookie"""
        cookie_file = self.storage_dir / f"{platform}.pkl"
        if cookie_file.exists():
            with open(cookie_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def is_cookie_valid(self, cookies):
        """检查Cookie是否有效"""
        # 检查过期时间等
        pass
```

#### 3.2.2 浏览器指纹模拟
```python
from playwright.sync_api import sync_playwright

class StealthBrowser:
    def __init__(self):
        self.playwright = sync_playwright().start()
    
    def create_browser(self, proxy=None):
        """创建防检测浏览器"""
        browser = self.playwright.chromium.launch(
            headless=True,
            proxy=proxy,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        # 注入 stealth 脚本隐藏自动化特征
        self._inject_stealth_scripts(context)
        
        return browser, context
    
    def _inject_stealth_scripts(self, context):
        """注入反检测脚本"""
        stealth_js = """
        // 隐藏 webdriver 属性
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // 伪装 plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // 伪装 languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en']
        });
        """
        context.add_init_script(stealth_js)
```

#### 3.2.3 验证码处理
```python
# 验证码识别方案
class CaptchaSolver:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def solve_slider(self, image_path, background_path):
        """解决滑块验证码"""
        # 方案1: 使用第三方打码平台 (如 2captcha、超级鹰)
        # 方案2: 本地深度学习模型 (YOLO + 图像匹配)
        # 方案3: 轨迹模拟 (针对简单滑块)
        pass
    
    def solve_click(self, image_path, question):
        """解决点选验证码"""
        # 需要图像识别 + 文字理解
        pass
    
    def solve_geetest(self, challenge, gt):
        """解决极验验证码"""
        # 极验需要专门的处理流程
        pass
```

### 3.3 高级策略层

#### 3.3.1 分布式抓取架构
```
┌─────────────────────────────────────────┐
│           任务调度中心 (Scheduler)        │
│  - 任务分发、优先级管理、去重            │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌───▼───┐    ┌───▼───┐
│Worker1│    │Worker2│    │WorkerN│
│- 代理1 │    │- 代理2 │    │- 代理N│
│- 账号1 │    │- 账号2 │    │- 账号N│
└───┬───┘    └───┬───┘    └───┬───┘
    │             │             │
    └─────────────┼─────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           数据存储 & 去重                │
│  - Redis (去重队列)                      │
│  - MySQL/MongoDB (数据存储)              │
└─────────────────────────────────────────┘
```

#### 3.3.2 账号池管理
```python
class AccountPool:
    """管理多个平台账号"""
    
    def __init__(self):
        self.accounts = {
            'jd': [],
            'taobao': [],
            'pdd': []
        }
    
    def get_account(self, platform):
        """获取可用账号"""
        # 轮询策略，避开风控账号
        pass
    
    def mark_limited(self, platform, account):
        """标记账号受限"""
        # 暂时停用，冷却一段时间
        pass
    
    def login_and_save(self, platform, username, password):
        """登录并保存Cookie"""
        # 自动化登录流程
        pass
```

#### 3.3.3 数据缓存与增量更新
```python
import hashlib
import redis

class SmartCache:
    def __init__(self):
        self.redis_client = redis.Redis()
    
    def get_cache_key(self, platform, query):
        """生成缓存key"""
        return f"price:{platform}:{hashlib.md5(query.encode()).hexdigest()}"
    
    def get_cached_price(self, platform, query):
        """获取缓存价格"""
        key = self.get_cache_key(platform, query)
        cached = self.redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def cache_price(self, platform, query, data, ttl=3600):
        """缓存价格数据"""
        key = self.get_cache_key(platform, query)
        self.redis_client.setex(key, ttl, json.dumps(data))
    
    def needs_update(self, platform, query, threshold=0.05):
        """判断是否需要更新"""
        # 对比新旧数据，变化超过阈值才更新
        pass
```

---

## 四、各平台特殊应对

### 4.1 京东 (JD) 专项

```python
class JDScraper:
    """京东专用抓取器"""
    
    BASE_URL = "https://search.jd.com/Search"
    
    def __init__(self):
        self.session = requests.Session()
        self._init_session()
    
    def _init_session(self):
        """初始化会话，获取必要Cookie"""
        # 访问首页获取 __jda, __jdb 等Cookie
        self.session.get("https://www.jd.com")
    
    def search(self, keyword):
        """搜索商品"""
        params = {
            'keyword': keyword,
            'enc': 'utf-8',
            'page': 1
        }
        
        response = self.session.get(
            self.BASE_URL,
            params=params,
            headers=self._get_headers()
        )
        
        return self._parse_results(response.text)
    
    def _get_headers(self):
        """京东专用请求头"""
        return {
            'Referer': 'https://search.jd.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }
    
    def _parse_results(self, html):
        """解析搜索结果"""
        # 处理动态加载的价格数据
        # 京东价格通过 separate API: p.3.cn/prices/mgets
        pass
```

### 4.2 淘宝/天猫 (Taobao/Tmall) 专项

```python
class TaobaoScraper:
    """淘宝专用抓取器"""
    
    def __init__(self):
        self.browser = None
        self.context = None
    
    def init_browser(self):
        """初始化浏览器（淘宝需要JS渲染）"""
        # 使用 Playwright 或 Selenium
        # 需要处理滑块验证
        pass
    
    def search_with_login(self, keyword):
        """登录后搜索"""
        # 淘宝搜索需要登录态
        # 1. 扫码登录或Cookie登录
        # 2. 访问搜索页面
        # 3. 处理可能出现的滑块
        pass
    
    def handle_slider(self, page):
        """处理淘宝滑块"""
        # 淘宝滑块检测非常严格
        # 方案1: 人工介入打码
        # 方案2: 使用打码平台API
        # 方案3: 轨迹模拟（成功率低）
        pass
```

### 4.3 拼多多 (PDD) 专项

```python
class PDDScraper:
    """拼多多专用抓取器"""
    
    API_BASE = "https://api.pinduoduo.com"
    
    def __init__(self):
        self.device_id = self._generate_device_id()
        self.headers = self._get_app_headers()
    
    def _generate_device_id(self):
        """生成设备ID"""
        # 拼多多有严格的设备指纹检测
        import uuid
        return str(uuid.uuid4()).replace('-', '')
    
    def _get_app_headers(self):
        """模拟App请求头"""
        return {
            'User-Agent': 'android/5.1.1 (Linux; U; Android 5.1.1; zh-CN)',
            'Content-Type': 'application/json',
            'Verify-Auth': self._generate_auth_token()
        }
    
    def search(self, keyword):
        """搜索商品"""
        # 拼多多使用 protobuf 传输
        # 需要逆向APP获取API接口和加密方式
        pass
```

---

## 五、技术实现方案

### 5.1 推荐技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **浏览器自动化** | Playwright / Selenium | Playwright更现代，检测更少 |
| **HTTP请求** | requests + urllib3 | 配合代理池使用 |
| **验证码识别** | ddddocr / 第三方API | 本地OCR或打码平台 |
| **代理管理** | scrapy-rotating-proxies | 代理轮换 |
| **数据存储** | Redis + MongoDB | 缓存 + 持久化 |
| **任务调度** | Celery / APScheduler | 分布式任务 |

### 5.2 核心代码框架

```python
# price_comparison_v2.py - 反爬增强版

import asyncio
import random
from dataclasses import dataclass
from typing import List, Optional
from playwright.async_api import async_playwright

@dataclass
class ScrapingConfig:
    """抓取配置"""
    use_proxy: bool = True
    use_browser: bool = True
    headless: bool = True
    max_retries: int = 3
    request_delay: tuple = (2, 5)

class AntiDetectScraper:
    """反检测抓取器"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.proxy_pool = ProxyPool() if config.use_proxy else None
        self.browser_pool = None
    
    async def init_browser_pool(self):
        """初始化浏览器池"""
        self.playwright = await async_playwright().start()
        self.browser_pool = []
        for _ in range(3):  # 3个浏览器实例
            browser = await self.playwright.chromium.launch(
                headless=self.config.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.browser_pool.append(browser)
    
    async def scrape_with_fallback(self, platform, query):
        """带降级策略的抓取"""
        for attempt in range(self.config.max_retries):
            try:
                # 尝试直接HTTP请求（最快）
                result = await self._http_request(platform, query)
                if result:
                    return result
            except Exception as e:
                print(f"HTTP attempt {attempt + 1} failed: {e}")
            
            try:
                # HTTP失败，使用浏览器渲染
                result = await self._browser_scrape(platform, query)
                if result:
                    return result
            except Exception as e:
                print(f"Browser attempt {attempt + 1} failed: {e}")
            
            # 指数退避
            await asyncio.sleep(2 ** attempt + random.uniform(1, 3))
        
        return None
    
    async def _http_request(self, platform, query):
        """HTTP直接请求"""
        # 使用 requests 快速获取
        pass
    
    async def _browser_scrape(self, platform, query):
        """浏览器渲染抓取"""
        browser = random.choice(self.browser_pool)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        try:
            # 访问搜索页面
            await page.goto(self._get_search_url(platform, query))
            
            # 等待内容加载
            await page.wait_for_selector('.gl-item', timeout=10000)
            
            # 提取数据
            results = await self._extract_data(page, platform)
            
            return results
        finally:
            await context.close()
    
    def _get_search_url(self, platform, query):
        """获取搜索URL"""
        urls = {
            'jd': f'https://search.jd.com/Search?keyword={query}',
            'taobao': f'https://s.taobao.com/search?q={query}',
            'tmall': f'https://list.tmall.com/search_product.htm?q={query}',
            'pdd': f'https://mobile.yangkeduo.com/search_result.html?search_key={query}'
        }
        return urls.get(platform)
    
    async def _extract_data(self, page, platform):
        """提取价格数据"""
        # 各平台选择器不同
        selectors = {
            'jd': '.gl-item',
            'taobao': '.item',
            'tmall': '.product-iWrap',
            'pdd': '.goods-item'
        }
        
        items = await page.query_selector_all(selectors.get(platform))
        results = []
        
        for item in items[:5]:  # 前5个结果
            data = await self._parse_item(item, platform)
            if data:
                results.append(data)
        
        return results
    
    async def _parse_item(self, item, platform):
        """解析单个商品"""
        # 各平台字段映射
        pass


# 使用示例
async def main():
    config = ScrapingConfig(
        use_proxy=True,
        use_browser=True,
        headless=True
    )
    
    scraper = AntiDetectScraper(config)
    await scraper.init_browser_pool()
    
    results = await scraper.scrape_with_fallback('jd', 'iPhone 16 Pro')
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 六、合规与风险控制

### 6.1 法律合规要点

| 合规项 | 要求 | 风险 |
|--------|------|------|
| **robots.txt** | 遵守各平台爬虫协议 | 民事纠纷 |
| **数据使用** | 仅个人使用，不商用 | 法律责任 |
| **请求频率** | 不造成服务器负担 | IP封禁 |
| **隐私保护** | 不抓取用户隐私数据 | 刑事责任 |

### 6.2 风险控制策略

```python
class RiskController:
    """风险控制管理"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = 0
    
    def check_rate_limit(self):
        """检查请求频率"""
        # 每分钟不超过20次
        pass
    
    def check_error_rate(self):
        """检查错误率"""
        # 错误率超过30%暂停抓取
        if self.error_count / self.request_count > 0.3:
            self._pause_and_alert()
    
    def _pause_and_alert(self):
        """暂停并告警"""
        # 发送通知，人工介入
        pass
```

### 6.3 推荐行为准则

1. **请求频率**: 每秒不超过1次，每天不超过1000次
2. **数据缓存**: 价格数据缓存1小时，避免重复抓取
3. **时间段**: 避开高峰期（10:00-12:00, 20:00-22:00）
4. **用户代理**: 轮换User-Agent，模拟真实浏览器
5. **失败处理**: 连续失败3次后切换代理/账号

---

## 七、推荐架构设计

### 7.1 最终推荐架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户请求层                            │
│  用户: "帮我比价 iPhone 16 Pro"                          │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   智能调度中心                           │
│  - 查询缓存（Redis）                                     │
│  - 任务分发                                              │
│  - 结果聚合                                              │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│   京东抓取器  │  │  淘宝抓取器  │  │  拼多多抓取器│
│  - HTTP优先   │  │  - 浏览器渲染│  │  - App模拟   │
│  - 降级浏览器 │  │  - 登录态    │  │  - 设备指纹  │
└───────┬──────┘  └──────┬──────┘  └──────┬──────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   数据清洗 & 分析                        │
│  - 价格归一化                                           │
│  - 优惠券计算                                           │
│  - 推荐评分                                             │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   结果呈现                               │
│  - 最优选项推荐                                         │
│  - 价格趋势图表                                         │
│  - 购买建议                                             │
└─────────────────────────────────────────────────────────┘
```

### 7.2 实施路线图

| 阶段 | 时间 | 目标 | 优先级 |
|------|------|------|--------|
| **Phase 1** | 1周 | 基础HTTP抓取 + 简单反爬 | ⭐⭐⭐ |
| **Phase 2** | 2周 | 浏览器渲染 + 验证码处理 | ⭐⭐⭐⭐ |
| **Phase 3** | 2周 | 代理池 + 账号池 + 分布式 | ⭐⭐⭐⭐ |
| **Phase 4** | 1周 | 缓存优化 + 监控告警 | ⭐⭐⭐ |

---

## 总结

### 核心要点

1. **分层对抗**: 从请求层到行为层的全方位伪装
2. **动态降级**: HTTP失败自动降级到浏览器渲染
3. **资源池化**: 代理池、账号池、浏览器池提高稳定性
4. **合规优先**: 遵守robots.txt，控制频率，避免法律风险

### 技术选型建议

- **轻度抓取**: requests + 代理轮换
- **中度抓取**: Playwright + stealth脚本
- **重度抓取**: 分布式架构 + 住宅代理 + 打码平台

### 下一步行动

1. 实现基础版HTTP抓取器（京东优先）
2. 集成Playwright浏览器渲染
3. 搭建代理池和缓存系统
4. 逐步完善各平台适配器

---

**文档位置**: `skills/price-comparison/anti-crawler-strategy.md`