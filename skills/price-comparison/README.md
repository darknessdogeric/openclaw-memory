# Price Comparison Skill - 全网比价工具 v4.0

> 自动全网比价，找到最优购买选项
> 支持京东、淘宝、天猫、拼多多
> 包含Redis缓存、价格监控、Web界面

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 安装 ddddocr（可选，用于验证码识别）
pip install ddddocr

# 安装Redis（可选，用于缓存）
# Windows: https://github.com/microsoftarchive/redis/releases
# Linux: sudo apt-get install redis-server
# Mac: brew install redis
```

### 2. 命令行使用
```bash
# 基础比价
price-compare.bat "iPhone 16 Pro 256GB"

# 指定平台
price-compare.bat "Sony WH-1000XM5" --platforms jd,taobao

# 使用代理池
price-compare.bat "MacBook Air" --use-proxy

# 查看更多结果
price-compare.bat "AirPods Pro" --top-n 5

# JSON输出
price-compare.bat "Nintendo Switch" --json
```

### 3. Web界面
```bash
# 启动Web服务器
start-web.bat

# 然后访问 http://localhost:5000
```

### 4. Python API
```python
from universal_price_compare import UniversalPriceComparator
from price_cache import PriceCacheManager

# 基础比价
comparator = UniversalPriceComparator()
result = comparator.compare("iPhone 16 Pro")

# 带缓存的比价
from price_cache import PriceCacheManager
cache = PriceCacheManager()

# 检查缓存
cached = cache.get_cached_price("iPhone 16 Pro", "jd")
if cached:
    print(f"缓存价格: ¥{cached['price']}")

# 获取价格历史
history = cache.get_price_history("12345", "jd", days=7)
trend = cache.get_price_trend("12345", "jd")
```

## 📊 功能特性

| 功能 | 状态 | 说明 |
|------|------|------|
| **京东** | ✅ | HTTP API，快速稳定 |
| **淘宝** | ✅ | Playwright渲染 |
| **天猫** | ✅ | Playwright渲染 |
| **拼多多** | ✅ | 网页解析 |
| **代理池** | ✅ | 自动轮换、验证 |
| **验证码处理** | ✅ | OCR + 打码平台 |
| **Redis缓存** | ✅ | 价格缓存、历史记录 |
| **价格监控** | ✅ | 降价提醒、历史最低 |
| **Web界面** | ✅ | 可视化操作 |

## 📁 文件结构

```
price-comparison/
├── SKILL.md                      # 技能说明文档
├── README.md                     # 本文件
├── requirements.txt              # 依赖列表
├── proxies.txt                   # 代理列表
│
├── universal_price_compare.py    # ⭐ 主程序（统一接口）
├── jd_scraper.py                 # 京东抓取器
├── taobao_scraper.py             # 淘宝/天猫抓取器
├── pdd_scraper.py                # 拼多多抓取器
├── proxy_pool.py                 # 代理池管理
├── captcha_solver.py             # 验证码处理
├── price_cache.py                # ⭐ Redis缓存系统
├── web_ui.py                     # ⭐ Web界面
├── price_comparison.py           # 基础版本
├── anti-crawler-strategy.md      # 反爬策略文档
│
├── price-compare.bat             # 命令行启动脚本
├── start-web.bat                 # Web界面启动脚本
└── demo.py                       # 演示脚本
```

## 🗄️ Redis缓存系统

### 功能
- **价格缓存** - 避免重复抓取，默认1小时
- **历史记录** - 保存30天价格历史
- **趋势分析** - 自动计算价格趋势
- **智能更新** - 过期自动刷新

### 使用
```python
from price_cache import PriceCacheManager, PriceMonitor

# 创建缓存管理器
cache = PriceCacheManager(host='localhost', port=6379)

# 缓存价格
cache.cache_price('iPhone', 'jd', product_data)

# 读取缓存
cached = cache.get_cached_price('iPhone', 'jd')

# 获取历史
history = cache.get_price_history('sku123', 'jd', days=7)

# 趋势分析
trend = cache.get_price_trend('sku123', 'jd')
print(f"趋势: {trend['trend']}")  # up/down/stable
print(f"最低价: ¥{trend['lowest_price']}")

# 价格监控
monitor = PriceMonitor(cache)
alert = monitor.check_price_drop('iPhone', 'jd', current_price=8999)
if alert:
    print(f"降价了！从 ¥{alert['old_price']} 降到 ¥{alert['new_price']}")
```

## 🌐 Web界面

### 启动
```bash
start-web.bat
```

### 功能
- 🔍 可视化搜索
- 📊 结果展示
- 🏆 最佳选项推荐
- 📈 价格对比

### 截图
```
┌─────────────────────────────────────────┐
│         🔍 全网比价工具                  │
│    支持京东、淘宝、天猫、拼多多          │
├─────────────────────────────────────────┤
│  [iPhone 16 Pro 256GB    ] [开始比价]   │
├─────────────────────────────────────────┤
│ 📦 京东                                 │
│ ┌─────────────────────────────────────┐ │
│ │ iPhone 16 Pro 256GB...              │ │
│ │ ¥8999 (原价¥9999) [10% off]         │ │
│ │ 🏪 Apple京东自营旗舰店              │ │
│ │ ⭐ 推荐度: 95/100                   │ │
│ └─────────────────────────────────────┘ │
│ 📦 拼多多                               │
│ ┌─────────────────────────────────────┐ │
│ │ iPhone 16 Pro 256GB 百亿补贴...     │ │
│ │ ¥8599 (原价¥9999) [14% off]         │ │
│ │ ⭐ 推荐度: 92/100                   │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ 🏆 最佳选项                             │
│ 京东 - ¥8999 - 京东自营，优惠10%        │
└─────────────────────────────────────────┘
```

## 🛡️ 反爬策略

### 多层防护
```
网络层: 代理池轮换
├── 自动验证代理可用性
├── 智能评分系统
└── 平台隔离（被ban自动屏蔽）

应用层: 请求伪装
├── User-Agent轮换
├── Cookie管理
└── 请求频率控制

浏览器层: 反检测
├── Playwright渲染
├── WebDriver特征隐藏
├── 指纹伪装
└── 人类行为模拟

验证码层: 自动处理
├── 本地OCR (ddddocr)
├── 打码平台 (2captcha)
└── 滑块轨迹生成
```

## 📈 输出示例

### 命令行
```
======================================================================
🔍 全网比价结果: iPhone 16 Pro 256GB
⏰ 查询时间: 2026-03-13 23:00:00
📊 查询平台: 京东, 淘宝, 天猫, 拼多多
======================================================================

📦 京东
----------------------------------------------------------------------
  Apple iPhone 16 Pro 256GB 黑色钛金属...
  💰 ¥8999 (原价 ¥9999) [10% off]
  🏪 Apple产品京东自营旗舰店 (自营)
  🚚 京东配送
  ⭐ 推荐度: 95/100

📦 拼多多
----------------------------------------------------------------------
  iPhone 16 Pro 256GB 百亿补贴...
  💰 ¥8599 (原价 ¥9999) [14% off]
  🏪 Apple品牌好货 (旗舰店)
  ⭐ 推荐度: 92/100

======================================================================
🏆 最佳购买选项
======================================================================
平台: 京东
价格: ¥8999
理由: 京东自营，优惠10%，高推荐度

======================================================================
📊 价格分析
======================================================================
全网最低价: ¥8599 (拼多多)
全网最高价: ¥9199 (天猫)
可节省: ¥600 (6.5%)
======================================================================
```

## 🛠️ 故障排除

### Redis连接失败
```bash
# Windows启动Redis
redis-server.exe

# 或使用内存缓存（无需Redis）
# 程序会自动降级到内存缓存
```

### Playwright安装失败
```bash
pip install --upgrade playwright
playwright install chromium
```

### 验证码处理
- 使用 `--no-headless` 显示浏览器手动处理
- 或安装 ddddocr: `pip install ddddocr`

## 📝 更新日志

### v4.0.0 (2026-03-13) - Phase 4
- ✅ Redis缓存系统
- ✅ 价格历史记录
- ✅ 趋势分析
- ✅ 价格监控告警
- ✅ Web可视化界面

### v3.0.0 (2026-03-13) - Phase 3
- ✅ 代理池系统
- ✅ 验证码处理
- ✅ 拼多多抓取器

### v2.0.0 (2026-03-13) - Phase 2
- ✅ Playwright浏览器
- ✅ 淘宝/天猫抓取

### v1.0.0 (2026-03-13) - Phase 1
- ✅ 京东抓取器
- ✅ 统一接口

## 🎯 完整架构

```
全网比价系统 v4.0
├── 数据层
│   ├── Redis缓存
│   ├── 价格历史
│   └── 趋势分析
│
├── 服务层
│   ├── 京东抓取器
│   ├── 淘宝/天猫抓取器
│   ├── 拼多多抓取器
│   ├── 代理池
│   └── 验证码处理
│
├── 接口层
│   ├── 命令行工具
│   ├── Python API
│   └── Web界面
│
└── 展示层
    ├── 最佳选项推荐
    ├── 价格对比
    ├── 历史趋势
    └── 监控告警
```

---

**作者**: B166ER  
**版本**: v4.0.0  
**更新日期**: 2026-03-13
