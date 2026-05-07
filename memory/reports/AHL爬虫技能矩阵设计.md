# AHL爬虫技能矩阵设计方案

> 版本：V1.0
> 日期：2026-05-05
> 定位：参考AHL SKILL编排逻辑，为AHL设计爬虫工具的技能矩阵

---

## 一、设计原理：为什么是矩阵而非单一工具

**传统方案**：选一个最强工具，All in
**SKILL矩阵方案**：每个工具是最优技能单元，智能编排

```
传统：scrap_tools.py → 失败 → 换Obscura → 失败 → 放弃

SKILL矩阵：
  URL输入 → 智能路由 → 最优工具执行
                    ↓ 失败
              自动切换下一工具
                    ↓ 失败
              标记"需要人工介入"
```

**核心优势**：
- 速度优先：先用快的（静态页面30ms vs 无头浏览器85ms）
- 成功率优先：动态页面自动切换到渲染引擎
- 成本优先：Tavily API有配额限制，作为最后兜底
- 资源适配：Linux服务器跑scrap_tools，本地/高并发用Obscura

---

## 二、四工具技能画像

| 技能 | 速度 | 反检测 | JS渲染 | 维护成本 | 适用场景 |
|------|------|--------|--------|---------|---------|
| **scrap_tools** | ⚡⚡⚡⚡ (最快) | ⚡⚡ (中等) | ❌ | ⚡⚡⚡⚡ (零) | 静态页面、新闻、百科 |
| **Obscura** | ⚡⚡⚡ (快) | ⚡⚡⚡⚡ (最强) | ✅ | ⚡⚡ (低) | 动态JS页面、反爬强站 |
| **Playwright** | ⚡⚡ (中) | ⚡⚡ (中等) | ✅ | ⚡⚡ (低) | 复杂交互、表单提交 |
| **Tavily API** | ⚡⚡⚡⚡ (最快) | N/A | N/A | ⚡⚡⚡⚡ (零) | 研究型搜索、新闻聚合 |

---

## 三、SKILL路由决策树

```
收到URL爬取请求
       ↓
┌─────────────────────────┐
│ Step 1: URL特征识别      │
│  - 是否为已知强反爬？    │
│  - 是否需要JS渲染？      │
│  - 数据类型？           │
└───────────┬─────────────┘
            ↓
            ├─ 静态页面 ──────────────→ scrap_tools [优先级1]
            │    (新闻/百科/政府/学术)
            │
            ├─ 已知强反爬 ─────────→ Obscura [优先级1]
            │    (携程/美团/小红书/抖音)
            │
            ├─ JS动态内容 ─────────→ Obscura [优先级1]
            │    (需等DOM渲染/用户行为触发)
            │
            ├─ 研究/搜索类 ────────→ Tavily API [优先级1]
            │    (行业研究/竞品分析/新闻)
            │
            └─ 复杂交互 ─────────→ Playwright [优先级1]
                 (登录/表单/滚动加载)
```

---

## 四、工具切换决策规则

### 4.1 自动降级规则

| 主工具失败原因 | 降级到 | 说明 |
|-------------|-------|------|
| HTTP 403/418 封禁 | → Obscura | 切反检测模式重试 |
| HTTP 500/503 服务错误 | → scrap_tools | 等5秒重试1次，仍失败降Obscura |
| 超时（>30s） | → scrap_tools（静态fallback） | 或Obscura无头模式 |
| JS渲染失败 | → Playwright | 换更重的渲染引擎 |
| Tavily配额耗尽 | → scrap_tools | 回退到直接抓取 |

### 4.2 URL特征库（预判用哪个）

```yaml
# 预判表：URL特征 → 最优工具
url_patterns:
  # 静态快取类
  - pattern: "*.gov.cn/*"
    tool: scrap_tools
    reason: 政府网站结构简单
  
  - pattern: "*.baidu.com/*"
    tool: scrap_tools
    reason: 静态内容为主

  - pattern: "*.wikipedia.org/*"
    tool: scrap_tools
    reason: 纯静态百科

  - pattern: "news.sina.com.cn/*"
    tool: scrap_tools
    reason: 新闻门户，静态

  # 强反爬类
  - pattern: "*ctrip.com/*"
    tool: Obscura
    reason: OTA强反爬+JS渲染

  - pattern: "*meituan.com/*"
    tool: Obscura
    reason: 同上

  - pattern: "*xiaohongshu.com/*"
    tool: Obscura
    reason: 小红书强反爬，需Stealth

  - pattern: "*douyin.com/*"
    tool: Obscura
    reason: 抖音/字节系强反爬

  - pattern: "* Fliggy.com/*"
    tool: Obscura
    reason: 飞猪

  # JS动态类
  - pattern: "*.booking.com/*"
    tool: Obscura
    reason: JS渲染+反爬

  - pattern: "*.airbnb.com/*"
    tool: Obscura
    reason: JS渲染

  # 研究类
  - pattern: "[研究/分析/报告]"
    tool: Tavily
    reason: 研究型搜索

  # 复杂交互类
  - pattern: "*/login*"
    tool: Playwright
    reason: 需要登录态
```

---

## 五、SKILL接口设计

### 5.1 统一SKILL接口

```yaml
SKILL_ID: "SCRAPE-01"
SKILL_NAME: "网页爬取技能"
VERSION: "1.0.0"

trigger:
  - intent: "爬取网页"
    keywords: ["抓取页面", "爬虫", "采集数据", "获取页面"]

input_slots:
  - name: "url"
    type: "string"
    required: true
    description: "目标URL"

  - name: "task_type"
    type: "enum"
    required: false
    default: "auto"
    options: ["auto", "static", "dynamic", "research"]
    description: "任务类型，auto自动判断"

  - name: "require_js"
    type: "boolean"
    required: false
    default: false
    description: "是否需要JS渲染"

output_slots:
  - name: "content"
    type: "string"
    description: "爬取到的内容(Markdown)"

  - name: "tool_used"
    type: "string"
    description: "实际使用的工具"

  - name: "attempts"
    type: "integer"
    description: "尝试了几次"

  - name: "status"
    type: "enum"
    options: ["success", "partial", "failed"]
    description: "执行状态"
```

### 5.2 工具适配器接口（标准化）

```python
class BaseScraperAdapter:
    """每个工具都需要实现的标准化接口"""
    
    name: str           # 工具名称
    priority: int        # 优先级（数字越小越优先）
    
    def can_handle(self, url: str, task_type: str) -> bool:
        """判断这个工具是否能处理这个任务"""
        raise NotImplementedError
    
    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        """执行爬取，返回标准结果"""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """检查工具是否可用（依赖是否安装等）"""
        raise NotImplementedError


class ScrapToolsAdapter(BaseScraperAdapter):
    name = "scrap_tools"
    priority = 1
    
    def can_handle(self, url, task_type):
        # 已知静态站优先用scrap_tools
        static_patterns = [
            ".gov.cn", ".baidu.com", ".wikipedia.org",
            "news.", ".sina.com", ".163.com",
            "*.cn/info/", "*.gov/"
        ]
        return any(p in url.lower() for p in static_patterns) and not task_type == "dynamic"


class ObscuraAdapter(BaseScraperAdapter):
    name = "Obscura"
    priority = 2
    
    def can_handle(self, url, task_type):
        # 强反爬/JS渲染/OTA平台
        js_patterns = [
            "ctrip.com", "meituan.com", "xiaohongshu.com",
            "douyin.com", "fliggy.com", "booking.com",
            "airbnb.com", "hotels.com"
        ]
        return any(p in url.lower() for p in js_patterns) or task_type == "dynamic"


class PlaywrightAdapter(BaseScraperAdapter):
    name = "Playwright"
    priority = 3
    
    def can_handle(self, url, task_type):
        # 复杂交互/登录态
        return "/login" in url or "form" in task_type


class TavilyAdapter(BaseScraperAdapter):
    name = "Tavily"
    priority = 4
    
    def can_handle(self, url, task_type):
        # 研究型/新闻类
        return task_type == "research" or "搜索" in task_type
```

---

## 六、SKILL编排核心逻辑

```python
class ScrapeSkillOrchestrator:
    """爬虫技能矩阵编排器"""
    
    def __init__(self):
        self.adapters = [
            ScrapToolsAdapter(),
            ObscuraAdapter(),
            PlaywrightAdapter(),
            TavilyAdapter(),
        ]
        self.adapters.sort(key=lambda x: x.priority)  # 按优先级排序
    
    def scrape(self, url: str, task_type: str = "auto", 
               max_attempts: int = 3) -> ScrapeResult:
        
        attempts = []
        
        for adapter in self.adapters:
            # 检查是否可用
            if not adapter.is_available():
                continue
            
            # 检查是否能处理
            if not adapter.can_handle(url, task_type):
                continue
            
            try:
                result = adapter.scrape(url)
                result.tool_used = adapter.name
                result.attempts = len(attempts) + 1
                return result
                
            except Exception as e:
                attempts.append({
                    "tool": adapter.name,
                    "error": str(e)
                })
                # 自动降级到下一个工具
                continue
        
        # 所有工具都失败
        return ScrapeResult(
            status="failed",
            content="",
            tool_used="none",
            attempts=len(attempts),
            errors=attempts
        )
```

---

## 七、与AHL现有系统的集成

### 7.1 定位

这不是AHL核心SKILL的一部分，而是**AHL的数据采集基础设施层**。

```
AHL数据采集层
┌──────────────────────────────────────┐
│ 爬虫技能矩阵（新增）                    │
│  ┌────────────────────────────────┐  │
│  │  ScrapeSkillOrchestrator        │  │
│  │  scrap_tools + Obscura +       │  │
│  │  Playwright + Tavily           │  │
│  └────────────────────────────────┘  │
└────────────┬───────────────────────────┘
             │
             ↓
┌──────────────────────────────────────┐
│ AHL现有系统                           │
│  SKILL编排层 → 运营数据 → 向量库       │
└──────────────────────────────────────┘
```

### 7.2 使用方式

```python
# AHL内部调用示例
from scrape_skill_matrix import ScrapeSkillOrchestrator

orchestrator = ScrapeSkillOrchestrator()

# 自动路由
result = orchestrator.scrape(
    url="https://www.ctrip.com/hotel/chengdu/12345.html",
    task_type="auto"
)

print(f"工具: {result.tool_used}")      # Obscura
print(f"状态: {result.status}")         # success
print(f"尝试次数: {result.attempts}")   # 1

# 强制指定类型
result2 = orchestrator.scrape(
    url="https://www.xiaohongshu.com/explore/xxx",
    task_type="dynamic"
)
# 自动用Obscura处理小红书
```

---

## 八、实施步骤

| 阶段 | 任务 | 优先级 | 说明 |
|------|------|--------|------|
| **Phase 1** | Obscura安装+适配器开发 | 🟡 中 | 约2小时 |
| **Phase 2** | 路由编排器开发 | 🟡 中 | 约2小时 |
| **Phase 3** | URL特征库建设 | 🟢 低 | 持续补充 |
| **Phase 4** | 与AHL SKILL系统集成 | 🟢 低 | Phase1完成后 |

---

## 九、Obscura安装（Phase 1）

```bash
# 下载最新版本（Linux服务器）
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux.tar.gz
tar xzf obscura-x86_64-linux.tar.gz

# 验证可用
./obscura --version

# 启动CDP服务（用于Puppeteer/Playwright连接）
./obscura serve --port 9222 --stealth

# 快速测试
./obscura fetch https://www.ctrip.com --eval "document.title"
```

**Windows安装**：从Releases页面下载.zip解压即可

---

## 十、与scrap_tools.py的关系

| 场景 | 当前工具 | 矩阵模式 |
|------|---------|---------|
| 静态页面（新闻/百科） | scrap_tools | scrap_tools优先 |
| 强反爬（OTA/小红书） | selenium-stealth | Obscura优先 |
| 复杂交互（登录/表单） | selenium | Playwright |
| 研究型搜索 | Tavily API | Tavily优先 |
| **备用兜底** | 失败后手动 | 自动切换下一个工具 |

**scrap_tools.py不会被删除**，而是作为技能矩阵的一号技能保留。

---

*V1.0 | 2026-05-05 | B166ER 参考AHL SKILL编排逻辑设计*
