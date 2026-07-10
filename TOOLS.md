# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — environment-specific config and tool status.

---

## 环境偏好

**终端**: Git Bash（非PowerShell）

---

## OpenViking - AI上下文数据库 ⚠️
**位置**: `C:\Users\ericz\.openviking\` | **服务器**: http://127.0.0.1:1933
**版本**: v0.2.9 (CLI: 0.2.6) | **Embedding**: Jina v4（限速，免费100次/分钟）
**功能**: 文件系统管理/分层上下文加载/语义搜索
**用法**: `ov status` / `ov find "query"` / `ov ls viking://resources/`
**问题**: Jina免费配额有限，高并发时被限速
**手动重启**: `Remove-Item -Force 'C:\Users\ericz\.openviking\data2\.openviking.pid'` → 运行`start_ov.bat`

### 本地语义搜索（免费无限制）✅ 新
**位置**: `workspace/local_semantic_search.py`
**Embedding**: model2vec `minishlab/potion-base-8M`（8MB，256维，CPU运行，完全免费）
**向量库**: Chromadb（本地持久化，`workspace/.chroma_db/`）
**用法**:
```
python local_semantic_search.py index   # 重建索引
python local_semantic_search.py count    # 统计文档数
python local_semantic_search.py search "查询内容"  # 语义搜索
python local_semantic_search.py full     # 完整重建
```
**已索引**: 141个memory文件（2026-04-08）
**优势**: 完全离线、无API限制、无配额问题

---

## PPT工具

### ppt-deck-builder-pro ✅
**位置**: `skills/ppt-deck-builder-pro/` | **版本**: 0.3.0
**模板**: 12种（含 startup_roadshow/corporate_pro/minimal_white/luxury_premium 等）
**用法**: 告诉B166ER场景 → 自动推荐模板 → 生成PPT
**快速生成**: `bash scripts/run_image_batch.sh plan.json output_dir`
**打包**: `bash scripts/package_image_deck.sh output_dir deck.pptx plan.json`

### md2all - Markdown转多格式 ✅
**位置**: `tools/md2all/` | **依赖**: python-docx, markdown, fpdf2, beautifulsoup4
**用法**: `python md2all.py 文档.md [pdf|docx|html]`

### md2ppt ✅
**位置**: `skills/md2ppt/md2ppt.py` | **依赖**: python-pptx, Pillow
**用法**: `python C:\Users\Administrator\.openclaw\skills\md2ppt\md2ppt.py`
**输出**: `C:\Users\Administrator\Desktop\项目说明书\`

---

## 网络工具

### scrap_tools.py - 爬虫工具箱 ✅
**位置**: `workspace/scrap_tools.py`
**用法**:
```
python scrap_tools.py fetch <url> [output]     # 静态页面
python scrap_tools.py dynamic <url> [output]  # JS页面
python scrap_tools.py search <query> [engine] # 搜索
python scrap_tools.py smart <query>            # 多引擎智能搜索
python scrap_tools.py parse <html> [engine]   # 解析结果
```
**已验证**: 静态页面(百度百科/新闻)、Playwright可用、scrapling可用
**注意**: 国内搜索有反爬（Baidu安全验证/Bing人机验证）→ 用直接URL抓取替代

### tavily_search.py - Tavily API搜索 ✅
**位置**: `workspace/tavily_search_v2.py`
**API Key**: `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` (2026-05-23更新)
**认证**: Authorization Bearer Header
**状态**: ✅ 已验证可用 (旧dev key已失效)

**⚠️ PNG截图铁律**: 使用 Edge/Chrome headless 截图时，必须加 `--force-device-scale-factor=2` 参数获得 Retina 清晰度（Eric 2026-05-21 明确要求）

**用法**:
```bash
python tavily_search_v2.py --query "关键词" --max-results 8 --include-answer --format md
```
**成功率**: 接近100%（绕过国内搜索引擎反爬限制）
**配额**: 1000次/月（免费版）
**对比**:
| 工具 | 成功率 | 速度 | 备注 |
|------|--------|------|------|
| Tavily API | ✅ 95%+ | 快 | 需API Key |
| scrapling | ✅ 静态页 | 快 | 百科/新闻 |
| 搜狗+selenium | ✅ 70% | 慢 | JS渲染页 |
| 百度/必应 | ❌ 反爬 | - | 触发验证 |

### Agent-Reach ✅ 已安装（2026-05-23）
**版本**: 1.4.0 | **命令**: `agent-reach doctor`
**状态**: 5/16渠道即开即用，11个可选渠道需配置
**安装方式**: `pip install git+https://github.com/Panniantong/Agent-Reach.git`
**SKILL路由**: `~/.agents/skills/agent-reach/`（17平台路由表已就位）

**已激活渠道（0配置）**: V2EX / RSS / Jina网页 / B站(yt-dlp+bili-cli) / 雪球
**待配置渠道（告诉Agent

### Firecrawl Skill ✅
**位置**: `skills/firecrawl-skill/` | **状态**: 已克隆，待配API Key
**用法**: `export FIRECRAWL_API_KEY=fc-your-key` → `python3 fc.py markdown "url"`

### Ultimate Search ✅
**位置**: `skills/ultimate-search/` | **状态**: 已克隆，需Docker
**功能**: Grok + Tavily双引擎搜索

### Crawl4AI ✅
**位置**: `skills/crawl4ai/` | **功能**: AI网页爬取

### Playwright MCP ✅
**位置**: `skills/playwright-mcp/` | **功能**: 浏览器自动化

### Apify MCP ✅
**位置**: `skills/apify-mcp/` | **功能**: Apify actors MCP

### Skyvern Vision LLM 浏览器Agent ✅ NEW
**位置**: `workspace/toolbox/skyvern_client.py` | **venv**: `workspace/workspace/skyvern_env/`
**Python**: 3.12（uv创建，与主环境3.14隔离）
**功能**: Vision LLM 驱动的浏览器自动化，替代脆弱的 XPath 选择器
**核心价值**: "换页面不坏"——用自然语言理解页面，而非硬编码选择器

**状态检查**:
```python
from toolbox.skyvern_client import diagnose, get_status
# 返回 {venv_ready, llm_configured, playwright_browsers, ...}
```

**集成到 scrape_matrix**: 所有工具都失败时，Skyvern 作为智能兜底自动触发
**快捷调用**:
```python
from toolbox.scrape_matrix import scrape_smart
# scrape_smart(url, prompt="提取酒店名称/价格/评分", schema={...})
```

**关键优势**:
- Vision LLM 理解页面语义，无需为每个网站写 XPath
- Planner-Actor-Validator 三智能体闭环（85.85% WebVoyager 准确率）
- 支持自然语言操作：page.act("点击登录按钮") / page.extract("提取订单数据")
- 与现有 Playwright/Obscura/scrap_tools 无缝集成

**依赖**: OPENAI_API_KEY 或 ANTHROPIC_API_KEY（环境变量）

### 爬虫技能矩阵 ✅ **NEW**
**位置**: `workspace/toolbox/scrape_matrix.py` | **版本**: V1.0
**四工具编排**: scrap_tools + Obscura + Playwright + Tavily
**用法**:
```python
import sys; sys.path.insert(0, 'workspace/toolbox')
from scrape_matrix import scrape, scrape_search, matrix_report

# 普通爬取（自动路由）
r = scrape("https://www.ctrip.com")           # → Obscura
r = scrape("https://www.xiaohongshu.com")    # → Obscura
r = scrape("https://en.wikipedia.org/wiki/...")  # → scrap_tools

# 强制类型
r = scrape("url", task_type="dynamic")       # 强制JS渲染
r = scrape("url", task_type="research")       # 强制Tavily搜索

# 搜索快捷
r = scrape_search("中国酒店行业2026趋势")

# 矩阵状态
print(matrix_report())
```
**优先级路由**:
| 优先级 | 工具 | 擅长场景 | 状态 |
|--------|------|---------|------|
| 1 | scrap_tools | 静态页面（百科/新闻/政府） | ✅ |
| 2 | **Obscura** | OTA强反爬/小红书/JS渲染 | ✅ |
| 3 | Playwright | 复杂交互/登录态 | ✅ |
| 4 | Tavily | 研究型搜索 | ✅ |
**Obscura安装**: `workspace/toolbox/obscura/obscura.exe`（49MB，内置反检测）
**已验证**: 携程✅ 小红书✅ Tavily搜索✅

---

## 增长工具

### Growth Mindset ✅
**位置**: `skills/growth-mindset/` | **版本**: 1.0.0
**用法**:
```bash
python reflection-tool.py reflect --task "任务" --completion 90 --quality 4
python reflection-tool.py summary
python reflection-tool.py suggest
```

### Ontology ✅
**位置**: `skills/ontology/` | **存储**: `memory/ontology/graph.jsonl`
**用法**: `create_entity()` / `create_relation()` / `query_entities()`

---

## 内容工具

### 提示词库
**AHL专用**: `D:\AHL-Database\07-AIGC提示词库\`
**源**: github.com/PlexPt/awesome-chatgpt-prompts-zh
**覆盖**: 小红书/抖音/朋友圈/邮件/公众号/OTA详情页

### 信息图/海报能力
| 能力 | 状态 | 说明 |
|------|------|------|
| design-md skill | ✅ 已安装 | 59个品牌DESIGN.md规范+设计语言库 |
| article-to-infographic skill | ✅ 已安装 | 文字→信息图，支持多风格 |
| 竖版9:16手机海报 | ✅ 掌握 | 2160×3840 Retina，4次迭代 |
| 参考图风格复现 | ✅ 掌握 | 玻璃拟态/扁平/深色科技全风格 |
| AHL海报 | ✅ 完成 | 4版本（AHL树形架构图） |
| **infographic_gen.py** | 🆕 | Python信息图生成器 + Jinja2模板 + Edge截图 |
| **markmap_cli** | 🆕 | Markdown→交互式思维导图，npm全局安装 |

### 思维导图（Markmap）
**安装**: `npm install -g markmap-cli`（已完成）
**用法**:
```
markmap 文档.md -o 输出.html   # 生成交互式HTML
markmap 文档.md -o 输出.svg    # 生成SVG
markmap -w 文档.md              # 监听模式（编辑实时更新）
```
**优点**: Markdown写好→自动生成思维导图，零设计成本。

### 信息图生成器（infographic_gen.py）
**位置**: `toolbox/infographic_gen.py` | **依赖**: jinja2, pillow, pycairo
**用法**:
```bash
python toolbox/infographic_gen.py   # 生成demo配置
python toolbox/infographic_gen.py infographic_config.json  # 根据JSON生成
```
**工作流**: JSON配置 → 自动生成HTML → 自动调用Edge截图 → PNG输出

### Next AI Draw.io 🟡 后备
**位置**: `workspace/next_ai_draw_tools.py` | **依赖**: CloakBrowser（已装）
**功能**: 自然语言生成draw.io图表，截图保存
**在线Demo**: `https://next-ai-drawio.jiang.jp/`（不稳定）
**状态**: 工具验证✅ 服务不稳定（MiniMax限流）
**用法**:
```bash
python next_ai_draw_tools.py "创建一个酒店收益管理流程图" "hotel_revenue"
python next_ai_draw_tools.py "创建一个AHL Agent架构图" "ahl_agent"
```
**输出**: `workspace/ai_draw_output/{文件名}.png`
**限制**:
- Demo服务不稳定（免费额度限流，AI常回复"Gone"）
- 建议自部署MCP Server以获得稳定服务
**用途**:
- AHL架构图/流程图
- 酒店收益管理矩阵
- 商业画布/竞争分析图
- 汇报材料插图

---

## invisible_playwright 评估记录（2026-06-12）

**状态**：✅ **已纳入 scrape_matrix 第 5 优先级，作为跨境 OTA 专用路由**

### A/B 对比结果（关键决策点）

| 工具 | 引擎 | Booking 抓取 | 现象 |
|------|------|------------|------|
| **Obscura** | Chromium + JS stealth | ❌ 失败 | 被重定向到 `pipl_consent.en-us.html`（未拿到数据）|
| **InvisiblePlaywright** | Firefox 150 + C++ 源 patch | ✅ 成功 | 抓到 "Imperial Hotel Tokyo, Tokyo (updated prices 2026)" |

**结论**：invisible_playwright 在跨境场景是**必要补充**，不是冗余。验证了 README 核心卖点（reCAPTCHA 0.90 vs Chromium 0.3-0.5）。

### 验证（30 分钟 demo）
| 测试 | 结果 | 解读 |
|------|------|------|
| bot.sannysoft.com（57 项基础检测）| 55/57 通过（96.5%）| 优秀 |
| Booking.com 酒店详情页 | 不被拦截，页面正常加载 | ✅ 核心价值验证 |
| 价格抓取（自动） | 未拿到（需选择器维护） | 工程问题，非工具问题 |
| Cloudflare/DataDome/reCAPTCHA | 0/4 触发 | ✅ 过检测确认 |

### scrape_matrix 路由规则

| URL 类型 | 默认工具 | 备选 |
|---------|---------|------|
| 静态页面 | scrap_tools | — |
| **跨境 OTA** (Booking/Agoda/Airbnb/Expedia) | **InvisiblePlaywright** | — |
| 国内 OTA (携程/美团/小红书) | Obscura | — |
| 复杂动态交互 | Playwright | InvisiblePlaywright |
| 搜索查询 | Tavily | — |
| 智能提取（视觉理解） | Vision LLM | Skyvern |

### 路由验证（已测试）

```python
from scrape_matrix import scrape
# Booking URL → 自动走 InvisiblePlaywright
r = scrape("https://www.booking.com/hotel/jp/imperial-tokyo.html",
           task_type="cross-border", wait_ms=8000, extract="title")
print(r.tool_used)  # → "InvisiblePlaywright"
print(r.content)    # → "Imperial Hotel Tokyo, Tokyo (updated prices 2026)"

# 携程 URL → 自动走 Obscura
r = scrape("https://www.ctrip.com/", extract="title")
print(r.tool_used)  # → "Obscura"
```

### 当前 scrape_matrix 6 个适配器

```
[1] scrap_tools       (静态页面)
[2] Obscura           (国内强反爬)
[3] Playwright        (复杂动态)
[4] InvisiblePlaywright (跨境 OTA)  ← NEW
[5] Tavily            (搜索)
[6] Vision LLM        (智能提取)
```

### 对 AHL 价值
- 🟢 **跨境 OTA**（Booking/Agoda/TripAdvisor）—— Firefox 差异化甜区，已验证
- 🟡 强反爬备选引擎（Obscura 仍主用国内）
- 🟢 批量抓取 anti-correlation（SOCKS5 + 唯一指纹）

### 关键风险
- bus factor = 1（feder-cr 个人维护，但**每周发版**，昨日 6/11 还在发版）
- 项目小众（GitHub stars 不详）
- Firefox 150 binary (~100MB) 需手动管理

### 下一步（不立即执行）
- 写 Booking/Agoda 价格 GraphQL 解析（1-2 天工程）
- 部署 IP 代理池（跨境抓取规模化）
- 等 AHL 跨境板块启动时再深入

### career-ops 借鉴（2026-06-12）

**位置**：`career-ops/`（完整克隆）+ `toolbox/career_ops_wrapper.py`（B166ER 适配包装器）

**状态**：✅ 已克隆 + 包装完成

**为什么装**（Eric 原话）："求职也要装。因为我即是创业者也是求职者，不耽误。互补。"

**career-ops 原版限制**：专为 ClaudeCode 设计（.claude/、.qwen/ 目录），不能直接用于 OpenClaw / B166ER

**B166ER 适配方案**：保留原克隆 + 写 wrapper 提取核心方法论
- ✅ **14 个模式**（scan / job / jobs / apply / cover / pdf / latex / interview / interview-prep / followup / patterns / batch / auto-pipeline / pipeline）
- ✅ **6 个 Archetype**（FDE / SA / PM / LLMOps / Agentic / Transformation）
- ✅ **A-G 评分体系**（10 维评分，13 项加权：role_fit / seniority / domain / skills / experience / culture / growth / network / comp / location / stability / legitimacy）
- ✅ **Liveness Gate**（用 B166ER 的 InvisiblePlaywright 替代 ClaudeCode 的 Playwright）
- ✅ **9 阶段 Pipeline**（discovered → evaluated → shortlisted → applying → interviewing → offered → accepted → rejected → withdrawn）

**使用举例**：
```python
from career_ops_wrapper import JobScore, liveness_check, CAREER_MODES

# 评分一个 offer
score = JobScore(role_fit=8.5, comp_competitiveness=7.5, ...)
print(f"Grade: {score.grade}, Total: {score.total}")

# 检查链接是否存活
check = liveness_check("https://linkedin.com/jobs/...")
print(f"Live: {check.is_live}, Has JD: {check.has_jd}")
```

**互补价值**（Eric 视角）：
- 🟢 创业者视角：作为产业观察窗口
- 🟢 求职者视角：作为外部 offer 信号源（即使在安逸集团也能看市场温度）
- 🟢 AHL 视角：候选人评估方法论可借鉴

---

### superpowers + MemPalace 方法论借鉴（2026-06-12）

**来源**：
- **obra/superpowers**（219.6K⭐）— Agent Skills 框架
- **MemPalace/mempalace**（54.3K⭐）— AI 记忆系统（LongMemEval R@5 = 96.6%）

**新规则加入 B166ER 自进化系统**（`~/self-improving/rules.md`）：
- **R07 - writing-plans before coding**：复杂任务先输出 2-5 分钟小任务计划
- **R08 - 验证先于完成**：报告前必须有测试/截图/JSON 验证证据
- **R09 - 系统化调试 4 阶段**：根因→假设→验证→修复
- **R10 - L0/L1 启动协议**：身份信息 + 关键事实 ≤ 200 token
- **R11 - 并行子代理 + 双阶段审查**：合规性 + 质量双层审查

**关键原则**：
- 借鉴而非照搬：superpowers 是 ClaudeCode 专用，B166ER 只吸收方法论
- 不重复造轮子：MemPalace 的 L0/L1 跟 AHL 记忆体系有重叠，借鉴"170 token 约束"原则
- 工具就用好：career-ops 原版在 OpenClaw 不可用，所以做 wrapper

---

### 盲水印工具 ✅ 已安装（2026-06-12）

**位置**：`toolbox/watermark_tool.py`
**来源**：guofei9987/blind_watermark (9.7K⭐)
**功能**：图片盲水印嵌入（肉眼不可见）/ 提取（无需原图）/ 抗旋转裁剪遮挡攻击 / 密码加密

**默认 Tag**：`B166ER-{YYYYMMDD}`（2026-06-12 Eric 明确：所有出品都需水印，不只AHL）

**验证**：✅ 嵌入→提取完整通过
**Python 3.14 兼容**：已手动 patch `blind_watermark.py` line 106（fromhex 奇偶padding）

**使用场景**（全量出品）：
- 信息图 / 海报 / 截图 / 监控图
- PPT 导出 / PDF 封面
- OTA 抓取截图
- “ERIC的B166ER出品”品牌保护

**快捷调用**：
```python
from watermark_tool import protect_output, verify_output
# 一键保护（默认 Tag: B166ER-{today}）
wm_img = protect_output('截图.png')
# 验证（提取水印）
print(verify_output(wm_img))  # → "OK: B166ER-20260612"
```

**原则 (R12)**：所有视觉产出都必须调 `protect_output()`。代码/MD/JSON 不需要（仅限图片/导出文件）。

---

### Booking 价格提取器 ✅ 生产就绪（2026-06-12）

**位置**：`toolbox/booking_price_extractor.py`

**攻破关键**：
- Booking 隐式"无日期不显示价格" — `ur_nodat=1` 标记
- 解决：URL 加 `?checkin=...&checkout=...&group_adults=...&selected_currency=...`
- DOM：价格在 `table.hprt-table` → `tr` → `td.hprt-table-cell-price`

**3/3 酒店验证**（2026-07-15→2026-07-16，2 成人，JPY）：
| 酒店 | 房型数 | 价格区间 | 平均价 |
|------|--------|---------|--------|
| Imperial Hotel Tokyo | 28 | ¥59,677 - ¥495,470 | ¥125,672 |
| Park Hyatt Tokyo | 28 | ¥147,899 - ¥646,056 | ¥277,927 |
| Hotel Granvia Kyoto | 24 | ¥26,606 - ¥84,212 | ¥44,198 |

**每个房型输出字段**：
- 房型名 + 床型 + 人数
- 原价 + 现价 + 折扣 %
- 取消政策（Free cancellation / Non-refundable）
- 早餐包含
- Pay later 标志
- 完整 raw_text（供 fallback）

**用法**：
```python
from booking_price_extractor import BookingPriceExtractor
ex = BookingPriceExtractor(wait_ms=12000)
result = ex.fetch_prices(
    hotel_url="https://www.booking.com/hotel/jp/imperial-tokyo.html",
    checkin="2026-07-15",
    checkout="2026-07-16",
    adults=2,
    currency="JPY",
)
print(result.rooms)  # [RoomRate, ...]
print(result.min_price, result.max_price, result.avg_price)
```

**稳定性**：自带 retry 机制（默认 2 次），临时网络问题自动恢复。

**AHL 数据底座接入路径**：
- 单一酒店：`ex.fetch_prices(...)`
- 批量酒店：循环 `for url in hotel_urls: ex.fetch_prices(...)`
- 数据流：`HotelPriceResult` → JSON → AHL Hub DB

---

### 安装信息
- `pip install git+https://github.com/feder-cr/invisible_playwright.git`
- Python 包：`invisible-playwright 0.2.0`
- Binary 路径：`C:\Users\ericz\AppData\Local\invisible-playwright\invisible-playwright\Cache\firefox-10\firefox.exe`
- 用法：`from invisible_playwright import InvisiblePlaywright` (drop-in Playwright 替换)

### 测试脚本与证据
- `toolbox/test_invisible_pw.py` / `test_invisible_pw_v2.py` / `test_invisible_pw_v3.py` (4 轮验证)
- `toolbox/test_routing.py` / `toolbox/test_routing_debug.py` (scrape_matrix 路由验证)
- `test_ahl_2.png`（Imperial Hotel 正常渲染截图）
- `test_invisible_pw_results.json` / `test_ahl_scenario.json`（结构化结果）
- `toolbox/scrape_matrix.py`（已集成 InvisiblePlaywrightAdapter）

---

## API Keys

| 服务 | Key | 备注 |
|------|-----|------|
| Jina Embedding | `jina_1aa1bc0d...` | OpenViking向量 |
| DeepSeek Chat | `sk-e4f35...822` | LLM (Agent TARS 主模型) |
| Tavily (Prod) | `tvly-prod-...W4` | Agent TARS 搜索 |
| Tavily | `tvly-dev-8KxnA8...` | 搜索API |
| RUNNINGHUB | (待配置) | PPT图片生成 |

---

## 运行环境

- **Node**: v24.14.0
- **Python**: 3.14 (C:\Users\ericz\AppData\Local\Programs\Python\Python314\)
- **Edge**: 148.0.3967.83 (CDP 端口 9222 已配置)
- **UI-TARS Desktop**: v0.2.4 (C:\Users\ericz\AppData\Local\UiTars\app-0.2.4)
- **工作区**: `C:\Users\ericz\.openclaw\workspace`
- **项目**: `C:\Users\ericz\Desktop\张实项目总控\`
- **Gateway**: 127.0.0.1:18789 | Web: http://127.0.0.1:18789/

---

## Agent TARS — 多模态 AI Agent（已部署）

**位置**: `@agent-tars/cli` v0.3.0 (npm 全局安装)
**配置文件**: `workspace/toolbox/agent-tars.config.json`
**启动脚本**: `workspace/toolbox/start_agent_tars.bat`
**浏览器CDP**: Edge 148 (port 9222, profile: `%USERPROFILE%\EdgeAgentProfile`)

### 使用方法

```bash
# Web UI (推荐)
双击 toolbox\start_agent_tars.bat  # 一键启动
# 或手动:
agent-tars serve --open --config toolbox\agent-tars.config.json

# 命令行 (headless)
agent-tars run --headless --input "你的任务" --config toolbox\agent-tars.config.json
```

### 已配置的能力
- **LLM**: DeepSeek Chat (API: sk-e4f35...822, base: api.deepseek.com)
- **搜索**: Tavily (tvly-prod-...W4, 8 results)
- **浏览器**: Edge 混合模式控制 (CDP 127.0.0.1:9222)
- **文件系统**: workspace 目录读写
- **命令执行**: 本机 shell 执行
- **规划器**: 复杂任务自动拆解

### 32 个内置工具
| 类别 | 工具 |
|------|------|
| 搜索 | web_search |
| 浏览器 | navigate/click/scroll/form_fill/screenshot/markdown 等 16 个 |
| 文件系统 | read/write/edit/list/search 等 9 个 |
| 命令 | run_command/run_script |
| 规划 | planner (自动拆解复杂任务) |

### 与 B166ER 能力矩阵的集成
- 补上 "无API系统操控" 缺口：视觉Agent看屏幕→控制桌面
- 与 WPS 自动化互补：WPS操控有COM的系统，Agent TARS操控有屏幕的系统
- 与 scrape_matrix 互补：抓取数据 + 操作页面（填表/提交/导航）
- 与 Tavily 搜索互补：内置搜索 + 浏览器主动验证

### 已知限制
- DeepSeek prompt_engineering 模式工具参数偶有解析偏差（用更精确的prompt可缓解）
- 桌面GUI Agent需要下载UI-TARS Desktop原生应用（GitHub releases，网络受限）
- 首次启动需要3-5秒模型加载
