# B166ER Playwright 快速使用指南

**安装状态**: ⏳ 安装中 (playwright-1.58.0, 36.8MB)

---

## 安装步骤

```bash
# 步骤1: 安装playwright包
pip install playwright

# 步骤2: 安装浏览器 (必需)
playwright install chromium

# 步骤3: 验证安装
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

---

## 基础使用示例

### 示例1: 读取网页内容

```python
from playwright.sync_api import sync_playwright

def read_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return content

# 使用
html = read_page("https://example.com")
print(html[:1000])
```

### 示例2: 截图

```python
from playwright.sync_api import sync_playwright

def screenshot(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=output_file, full_page=True)
        browser.close()

# 使用
screenshot("https://example.com", "screenshot.png")
```

### 示例3: 提取文本

```python
from playwright.sync_api import sync_playwright

def extract_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        text = page.inner_text('body')
        browser.close()
        return text

# 使用
text = extract_text("https://example.com")
print(text[:1000])
```

### 示例4: 等待JS渲染

```python
from playwright.sync_api import sync_playwright

def read_js_page(url, wait_for=None):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # 等待特定元素加载
        if wait_for:
            page.wait_for_selector(wait_for)
        else:
            # 等待网络空闲
            page.wait_for_load_state('networkidle')
        
        content = page.content()
        browser.close()
        return content

# 使用 (等待文章加载)
html = read_js_page("https://spa-site.com", wait_for="article")
```

---

## 高级用法

### 模拟真实用户

```python
from playwright.sync_api import sync_playwright

def human_like_browsing(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        # 模拟人类行为
        page.goto(url)
        page.mouse.move(100, 200)
        page.wait_for_timeout(1000)  # 等待1秒
        page.mouse.wheel(0, 500)  # 滚动
        
        content = page.content()
        browser.close()
        return content
```

### 处理登录

```python
from playwright.sync_api import sync_playwright

def login_and_read(url, username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 登录
        page.goto(url)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        
        # 等待登录成功
        page.wait_for_url('**/dashboard')
        
        content = page.content()
        browser.close()
        return content
```

---

## 集成到B166ERCrawler

```python
# 添加到 b166er_crawler.py

def _playwright_read(self, url, wait_for=None):
    """使用Playwright读取URL (支持JS渲染)"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=30000)
            
            # 等待页面加载
            if wait_for:
                page.wait_for_selector(wait_for, timeout=10000)
            else:
                page.wait_for_load_state('networkidle', timeout=10000)
            
            content = page.content()
            browser.close()
            
            return content, 'success'
            
    except Exception as e:
        return None, f"Playwright Error: {str(e)}"
```

---

## 常见问题

### Q: 安装失败怎么办?
```bash
# 尝试使用国内镜像
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装浏览器时失败
python -m playwright install chromium --with-deps
```

### Q: 内存占用过高?
```python
# 及时关闭浏览器
browser.close()

# 使用上下文隔离
context = browser.new_context()
page = context.new_page()
# ... 操作
context.close()
```

### Q: 被反爬虫检测?
```python
# 添加更多伪装
context = browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    locale='zh-CN',
    timezone_id='Asia/Shanghai'
)
```

---

**Playwright安装完成后，即可使用以上代码进行JS渲染页面爬取。**
