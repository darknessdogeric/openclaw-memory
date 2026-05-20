# Multi-OTA 酒店数据监控 — 第一批状态报告

**生成时间**: 2026-05-12 09:30 CST  
**版本**: v0.1.0

---

## 一、项目概述

为 AHL-LLM 去中心化民宿交易协议建立跨 OTA 酒店价格/房态监控能力。第一批覆盖 4 个平台。

---

## 二、四平台连通性测试结果

| 平台 | URL | web_fetch | scrap_tools | Playwright | Playwright+stealth | 结论 |
|------|-----|-----------|-------------|------------|-------------------|------|
| **猫途鹰** | tripadvisor.cn | ❌ JS渲染 | ✅ **成功** | ✅ | — | 静态HTML即可采集 |
| **美团** | hotel.meituan.com | ❌ 403 | ❌ 403 | ❌ 403 | ❌ 403 | 需更强反检测方案 |
| **去哪儿** | hotel.qunar.com | ❌ JS渲染 | 🔄 asyncio冲突 | ⚠️ 部分(仅footer) | — | content未完全加载 |
| **飞猪** | fliggy.com | ⚠️ 首页内容 | — | 🔄 待完善 | — | 可能需要登录态 |

### 详细说明

#### ✅ 猫途鹰 (tripadvisor.cn) — 已验证可用
- **采集方案**: scrap_tools.py (scrapling Fetcher) 静态抓取
- **测试城市**: 襄阳 (geocode: g494931)
- **采集结果**: 27家酒店，1秒内完成
- **数据字段**: 酒店名、排名、评论数、城市均价区间
- **正确geocode获取方法**: Bing 搜索 `site:tripadvisor.cn {城市名} 酒店`

**示例数据 (襄阳 TOP 5)**:
| 排名 | 酒店名称 | 评论数 | 均价区间 |
|------|----------|--------|---------|
| 1 | 襄阳富力皇冠假日酒店（诸葛亮广场万达广场店） | 2,121 | ￥1,080-1,736 |
| 2 | 襄阳共享国际大酒店 | 66 | ￥1,080-1,736 |
| 3 | 维也纳国际酒店(襄阳万达广场火车站店) | 89 | ￥1,080-1,736 |
| 4 | 汉江国际大酒店 | 61 | ￥1,080-1,736 |
| 5 | 襄阳南湖宾馆 | 31 | ￥1,080-1,736 |

#### ❌ 美团 (hotel.meituan.com) — 被反爬拦截
- 所有方案均返回 **403 Forbidden (openresty)**
- 即使使用 playwright-stealth 仍被检测
- **根因**: 美团使用高级浏览器指纹检测，headless Chromium 被识别
- **建议方案**:
  1. 部署 Obscura 反检测浏览器（Rust实现，极难被检测）
  2. 使用移动端 API 接口替代网页爬取
  3. 通过第三方比价平台间接获取

#### ⚠️ 去哪儿 (hotel.qunar.com) — JS未完全加载
- Playwright Chromium 可连通，但仅获取到 footer 文字 (296 chars)
- 酒店内容通过 JS 动态加载，`networkidle` 后仍未渲染
- **可能原因**: 
  1. 需要滚动触发懒加载
  2. 需要特定 referer/cookie
  3. 使用虚拟列表只渲染可视区域
- **建议**: 需要监控网络请求，直接拦截酒店数据 API

#### ⚠️ 飞猪 (fliggy.com) — 需要交互
- Playwright Chromium 可连通首页
- 酒店数据在独立搜索页中，需要输入城市名搜索
- 阿里系可能有登录态要求
- **建议**: 优先抓取飞猪API接口而非网页

---

## 三、已完成的代码交付

### `workspace/ota_monitor.py`
统一采集脚本，架构：

```
OTAMonitor (编排器)
├── TripAdvisorAdapter   ← scrap_tools 静态抓取 ✅
├── MeituanAdapter       ← Playwright+stealth    🔄
├── QunarAdapter         ← Playwright            🔄
├── FliggyAdapter        ← Playwright            🔄
└── ObscuraAdapter       ← 预留接口              ⏳
```

### 核心功能
- **统一数据模型** (`HotelRecord`): 平台/酒店名/价格/评分/评论数/房态/时间戳
- **多平台批量采集**: `monitor.scrape_all(city="襄阳")`
- **JSON 导出**: 带时间戳和 `latest.json` 缓存
- **健康检查**: `python ota_monitor.py --report`
- **CLI 接口**: 支持城市、平台筛选

### 使用方法
```bash
# 全平台采集（襄阳）
python ota_monitor.py

# 指定城市
python ota_monitor.py --city 北京

# 单平台
python ota_monitor.py --platform tripadvisor

# 多平台
python ota_monitor.py --platform tripadvisor,qunar

# 健康检查
python ota_monitor.py --health

# 状态报告
python ota_monitor.py --report
```

### 输出位置
- `workspace/cache/ota_monitor/ota_monitor_YYYYMMDD_HHMMSS.json` (历史)
- `workspace/cache/ota_monitor/latest.json` (最新)

---

## 四、工具链状态

| 工具 | 状态 | 版本/位置 | 备注 |
|------|------|-----------|------|
| scrap_tools (scrapling) | ✅ | workspace/scrap_tools.py | 静态抓取核心工具 |
| Playwright Chromium | ✅ | playwright 1.58.0 | 仅 Chromium 可用 |
| playwright-stealth | ✅ | 2.0.3 | 已安装但美团仍被拦截 |
| Playwright Firefox | ❌ | 未安装 | `playwright install firefox` 可补充 |
| Obscura | ❌ | 未安装 | 需下载 GitHub Release |
| scrape_matrix.py | 🔄 | workspace/toolbox/ | 路径硬编码需修复 (D: → C:) |

---

## 五、已知问题 & 待办

### 紧急 (P0)
- [ ] **美团反爬突破**: 部署Obscura或找到移动端API
- [ ] **去哪儿内容加载**: 排查JS渲染问题，尝试拦截API请求

### 重要 (P1)
- [ ] **飞猪搜索交互**: 完善搜索→输入城市→等待结果→解析的流程
- [ ] **Tripadvisor geocode 自发现**: 自动从搜索结果页提取城市 geocode
- [ ] **scrape_matrix.py 路径修复**: 将 `D:\B166ER-OpenClaw` 改为当前 `C:\Users\Administrator\.openclaw`

### 优化 (P2)
- [ ] **增量更新**: 存储历史数据，只采集变化
- [ ] **价格告警**: 价格波动超过阈值时通知
- [ ] **定时调度**: 配合 cron/heartbeat 定时采集
- [ ] **携程(ctrip)接入**: 作为第5个平台的第二批

---

## 六、数据模型 (统一)

```python
@dataclass
class HotelRecord:
    platform: str              # meituan|qunar|fliggy|tripadvisor|ctrip
    hotel_name: str            # 酒店名称
    price_min: Optional[float] # 最低价 (CNY)
    price_max: Optional[float] # 最高价 (CNY)
    rating: Optional[float]    # 用户评分
    review_count: Optional[int]# 评论数
    room_available: bool       # 是否有房
    scraped_at: str            # ISO 8601 时间戳 (北京时间)
    url: str                   # 来源URL
    raw_data: dict             # 平台特有原始数据

@dataclass
class ScrapeResult:
    platform: str
    status: ScrapeStatus       # success|partial|failed|blocked|not_implemented
    hotels: list[HotelRecord]
    errors: list[str]
    tool_used: str
    elapsed_ms: int
```

---

## 七、架构决策记录 (ADR)

### ADR-001: TripAdvisor 使用直接导入而非 subprocess
- **决策**: `from scrap_tools import fetch_static` 直接调用
- **原因**: subprocess 只能捕获 print 输出，scrap_tools.py 的 CLI 入口不打印返回内容
- **影响**: TripAdvisorAdapter 与 scrap_tools 紧密耦合，需确保 workspace 在 Python path 中

### ADR-002: Obscura 预留接口
- **决策**: 创建 ObscuraAdapter 但标记为 `not_implemented`
- **原因**: Obscura.exe 未安装，网络环境（代理限制）暂无法下载
- **影响**: 美团等强反爬平台暂时无解，需人工部署 Obscura

### ADR-003: 城市 geocode 手动维护
- **决策**: CITY_GEOCODE 字典手动管理
- **原因**: Tripadvisor 的 geocode 无法通过静态页面搜索获取（JS渲染）
- **替代方案**: Bing搜索 `site:tripadvisor.cn {城市} 酒店` 获取

---

*本报告由 B166ER 子代理自动生成，主代理可随时查看详情。*
