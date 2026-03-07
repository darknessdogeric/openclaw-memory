# B166ER 爬虫工具 - API申请指南

**文档用途**: 申请免费API Key，扩展爬虫能力  
**更新日期**: 2026-03-07  

---

## 一、Brave Search API (推荐)

### 1.1 申请信息

| 项目 | 详情 |
|------|------|
| **申请地址** | https://brave.com/search/api/ |
| **免费额度** | 每月2,000次查询 |
| **费用** | 完全免费 |
| **用途** | 高质量搜索，替代Google |

### 1.2 申请步骤

```
步骤1: 访问 https://brave.com/search/api/
步骤2: 点击 "Get Started for Free"
步骤3: 注册账号（可用Google账号）
步骤4: 验证邮箱
步骤5: 进入Dashboard
步骤6: 创建API Key
步骤7: 复制Key保存
```

### 1.3 使用方法

```python
import requests

BRAVE_API_KEY = "your-api-key"

def brave_search(query, count=10):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {"X-Subscription-Token": BRAVE_API_KEY}
    params = {"q": query, "count": count}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 使用示例
results = brave_search("Marriott brand standards")
```

### 1.4 额度管理

- 每月1日重置额度
- 2000次/月 = 约66次/天
- 适合中等频率使用
- 超出后可购买付费计划

---

## 二、FireCrawl API (推荐)

### 2.1 申请信息

| 项目 | 详情 |
|------|------|
| **申请地址** | https://firecrawl.dev/app/api-keys |
| **免费额度** | 每月500积分 |
| **费用** | 完全免费 |
| **用途** | 网页爬取、结构化提取 |

### 2.2 申请步骤

```
步骤1: 访问 https://firecrawl.dev
步骤2: 点击 "Get Started"
步骤3: 用GitHub或邮箱注册
步骤4: 验证账号
步骤5: 进入API Keys页面
步骤6: 创建新API Key
步骤7: 复制保存
```

### 2.3 使用方法

```python
from firecrawl import FirecrawlApp

FIRECRAWL_API_KEY = "your-api-key"
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# 爬取单页
result = app.scrape_url("https://example.com")

# 搜索
results = app.search("query")

# 批量爬取
results = app.crawl_url("https://example.com", params={"limit": 10})
```

### 2.4 积分消耗

| 操作 | 消耗积分 |
|------|---------|
| 爬取单页 | 1-5积分 |
| 搜索 | 1积分/次 |
| 批量爬取 | 1积分/页 |
| 截图 | 2-5积分 |

**500积分 = 约100-500次请求**

---

## 三、Google Custom Search API (备选)

### 3.1 申请信息

| 项目 | 详情 |
|------|------|
| **申请地址** | https://developers.google.com/custom-search/v1/overview |
| **免费额度** | 每日100次查询 |
| **费用** | 免费额度外$5/1000次 |
| **用途** | Google搜索能力 |

### 3.2 申请步骤

```
步骤1: 访问 Google Cloud Console
步骤2: 创建新项目
步骤3: 启用 Custom Search API
步骤4: 创建API Key
步骤5: 创建Custom Search Engine
步骤6: 获取Search Engine ID
步骤7: 保存API Key和Engine ID
```

### 3.3 使用方法

```python
import requests

GOOGLE_API_KEY = "your-api-key"
SEARCH_ENGINE_ID = "your-engine-id"

def google_search(query, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num
    }
    
    response = requests.get(url, params=params)
    return response.json()
```

---

## 四、Bing Search API (备选)

### 4.1 申请信息

| 项目 | 详情 |
|------|------|
| **申请地址** | https://www.microsoft.com/en-us/bing/apis/bing-web-search-api |
| **免费额度** | 每月1,000次查询 |
| **费用** | 免费额度外付费 |
| **用途** | Bing搜索能力 |

### 4.2 申请步骤

```
步骤1: 访问 Azure Portal
步骤2: 创建Bing Search资源
步骤3: 获取API Key
步骤4: 保存备用
```

---

## 五、API Key管理建议

### 5.1 配置环境变量

```bash
# Windows PowerShell
$env:BRAVE_API_KEY = "your-key"
$env:FIRECRAWL_API_KEY = "your-key"

# Windows CMD
set BRAVE_API_KEY=your-key
set FIRECRAWL_API_KEY=your-key

# Linux/Mac
export BRAVE_API_KEY="your-key"
export FIRECRAWL_API_KEY="your-key"
```

### 5.2 多API轮换策略

```python
# 当某个API额度用完时自动切换
class APIRotation:
    def __init__(self):
        self.apis = {
            'tavily': {'key': 'tvly-xxx', 'quota': 1000, 'used': 0},
            'brave': {'key': 'brave-xxx', 'quota': 2000, 'used': 0},
            'firecrawl': {'key': 'fc-xxx', 'quota': 500, 'used': 0},
        }
    
    def get_available_api(self):
        for name, config in self.apis.items():
            if config['used'] < config['quota']:
                return name
        return None
```

### 5.3 额度监控

```python
import json
import os

class QuotaMonitor:
    def __init__(self, quota_file="quota.json"):
        self.quota_file = quota_file
        self.load_quota()
    
    def load_quota(self):
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                self.quota = json.load(f)
        else:
            self.quota = {}
    
    def save_quota(self):
        with open(self.quota_file, 'w') as f:
            json.dump(self.quota, f)
    
    def use_quota(self, api_name):
        if api_name not in self.quota:
            self.quota[api_name] = 0
        self.quota[api_name] += 1
        self.save_quota()
        return self.quota[api_name]
    
    def get_usage(self, api_name, monthly_limit):
        used = self.quota.get(api_name, 0)
        remaining = monthly_limit - used
        return {
            'used': used,
            'limit': monthly_limit,
            'remaining': remaining,
            'percentage': (used / monthly_limit) * 100
        }
```

---

## 六、申请优先级建议

### 6.1 立即申请 (P0)

1. **Brave Search API**
   - 免费额度高 (2000次/月)
   - 搜索质量好
   - 申请简单

2. **FireCrawl API**
   - 爬取能力强
   - 支持结构化提取
   - 免费额度够用

### 6.2 稍后申请 (P1)

3. **Google Custom Search**
   - 每日100次可能不够
   - 需要信用卡验证
   - 配置较复杂

4. **Bing Search API**
   - 免费额度较低
   - Azure配置复杂

---

## 七、申请完成检查清单

- [ ] 申请Brave Search API Key
- [ ] 申请FireCrawl API Key
- [ ] 测试Brave API可用性
- [ ] 测试FireCrawl API可用性
- [ ] 更新b166er_crawler.py配置
- [ ] 设置环境变量
- [ ] 创建额度监控系统

---

## 八、参考链接

- Brave Search API: https://brave.com/search/api/
- FireCrawl: https://firecrawl.dev
- Tavily: https://tavily.com
- Google Custom Search: https://developers.google.com/custom-search

---

**下一步**: 立即申请Brave和FireCrawl API Key
