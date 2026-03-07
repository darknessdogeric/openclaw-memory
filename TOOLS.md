# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Ontology 技能 (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\ontology\`
**来源**: https://github.com/hiveminderbot/ontology
**功能**: 结构化知识图谱，实体关系管理
**存储**: `memory/ontology/graph.jsonl`

**使用方法**:
```python
from src.services.entity_service import create_entity, query_entities
from src.services.relation_service import create_relation

# 创建实体
person = create_entity('Person', {'name': '张三'}, 'memory/ontology/graph.jsonl')
project = create_entity('Project', {'name': '项目A'}, 'memory/ontology/graph.jsonl')

# 建立关系
create_relation(person['id'], 'owns', project['id'], {}, 'memory/ontology/graph.jsonl')

# 查询
results = query_entities('Person', {'name': '张三'}, 'memory/ontology/graph.jsonl')
```

**已创建实体**:
- Person: 张实 (pers_a71f9e3f)
- Project: AHL-LLM去中心化旅行平台 (proj_b39fb3af)
- Relation: 张实 owns AHL项目

---

### Firecrawl Skill (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\firecrawl-skill\`
**来源**: https://github.com/capt-marbles/firecrawl
**功能**: 网页爬取，支持markdown/screenshot/extract/crawl
**状态**: ✅ 已克隆，待配置API Key

**使用方法**:
```bash
# 设置API Key
export FIRECRAWL_API_KEY=fc-your-key

# 获取页面markdown
python3 fc.py markdown "https://example.com"

# 截图
python3 fc.py screenshot "https://example.com" -o screenshot.png

# 提取结构化数据
python3 fc.py extract "https://example.com" --schema schema.json

# 搜索
python3 fc.py search "query" --limit 5

# 爬取文档站点
python3 fc.py crawl "https://docs.example.com" --limit 30
```

---

### Ultimate Search Skill (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\ultimate-search\`
**来源**: https://github.com/ckckck/UltimateSearchSkill
**功能**: Grok + Tavily双引擎搜索，FireCrawl降级
**状态**: ✅ 已克隆，需Docker部署

**使用方法**:
```bash
# Docker部署
cd ultimate-search
docker compose up -d

# Grok搜索
bash scripts/grok-search.sh --query "FastAPI最新特性"

# Tavily搜索
bash scripts/tavily-search.sh --query "Python web frameworks"

# 双引擎搜索
bash scripts/dual-search.sh --query "Rust vs Go"

# 网页抓取
bash scripts/web-fetch.sh --url "https://example.com"
```

**需要配置**:
- Grok SSO Token (export_sso.txt)
- Tavily API Key
- FireCrawl API Key (可选)

---

### Crawl4AI (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\crawl4ai\`
**来源**: https://github.com/unclecode/crawl4ai
**功能**: AI驱动的网页爬取和数据提取
**状态**: ✅ 已克隆

---

### Playwright MCP (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\playwright-mcp\`
**来源**: https://github.com/microsoft/playwright-mcp
**功能**: Microsoft Playwright浏览器自动化
**状态**: ✅ 已克隆

---

### Apify MCP (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\apify-mcp\`
**来源**: https://github.com/apify/actors-mcp-server
**功能**: Apify actors MCP服务器
**状态**: ✅ 已克隆

---

### Skill Creator (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\skill-creator\`
**来源**: https://github.com/nkchivas/openclaw-skill-skill-creator
**功能**: 自动生成OpenClaw技能结构
**状态**: ✅ 已克隆

---

### Nano PDF 技能 (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\nano-pdf\`
**来源**: https://github.com/nkchivas/openclaw-skill-nano-pdf
**功能**: 使用自然语言指令编辑PDF
**依赖**: `uv install nano-pdf`
**状态**: ✅ 已克隆，待安装依赖

**使用方法**:
```bash
# 安装依赖
uv install nano-pdf

# 编辑PDF第1页
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results'"

# 修复拼写错误
nano-pdf edit document.pdf 3 "Fix typo in subtitle"
```

**注意**: 页码从0或1开始，取决于工具版本；如果结果不对，尝试另一种。

---

### Proactive Agent 技能 (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\proactive-agent\`
**来源**: https://github.com/nkchivas/openclaw-skill-proactive-agent
**版本**: v3.0.0 by Hal Labs
**功能**: 主动式智能体架构 - 从被动等待到主动创造价值

**核心能力**:
- **WAL Protocol** - 关键信息预写日志（修正/决策/偏好立即记录）
- **Working Buffer** - 上下文60%后自动记录所有交换
- **Compaction Recovery** - 上下文截断后从buffer恢复
- **安全加固** - 技能安装审查、外部AI网络防护、上下文防泄露
- **Relentless Resourcefulness** - 10种方法尝试后才放弃
- **自我改进** - ADL(防漂移)/VFM(价值优先)安全进化协议
- **主动惊喜** - "我能为用户创造什么他们没要求但会喜欢的东西？"

**使用方法**:
```bash
# 复制模板到工作区
cp assets/*.md ./

# 运行安全审计
./scripts/security-audit.sh
```

**关键文件**:
- `SESSION-STATE.md` - 活跃任务状态（RAM）
- `memory/working-buffer.md` - 危险区域日志
- `AGENTS.md` - 运行规则和工作流
- `SOUL.md` - 身份和原则
- `USER.md` - 用户上下文和目标

---

### 运行环境偏好

**终端选择**: Git Bash (非 PowerShell)
- 原因: 更好的 Linux 命令兼容性、一致的体验
- 避免: 直接在 PowerShell 中运行 OpenClaw 命令

---

### Tavily Search API
- API Key: `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`
- 免费额度: 1000次/月
- 备用方案: 额度用完时用 Kimi 大模型联网搜索
- 安装命令: `clawhub install tavily-search`

---

### Agent Reach (互联网能力)
- **版本**: 1.2.0
- **安装位置**: C:\Python314\Lib\site-packages
- **克隆位置**: C:\Users\Administrator\Downloads\agent-reach
- **功能**: 
  - 网页阅读: `curl https://r.jina.ai/http://URL`
  - YouTube/B站字幕: `yt-dlp --dump-json "URL"`
  - RSS解析: Python feedparser
  - Twitter/小红书: 需配置Cookie (待配置)
- **使用指南**: `docs/Agent_Reach_使用指南.md`

---

### Agent Reach - 社交媒体配置状态
- **Twitter/X**: 可配置 (需安装 xreach-cli)
- **小红书**: 需Docker (未安装)
- **抖音**: 可配置 (需安装 douyin-mcp-server)
- **配置指南**: `docs/Agent_Reach_社交媒体配置指南.md`
- **状态报告**: `docs/Agent_Reach_配置状态报告.md`

---

### 已安装 OpenClaw Skills (9个)
位置: `C:\Users\Administrator\.openclaw\skills\`

**核心技能**:
- ✅ email - 邮件管理
- ✅ calendar - 日程管理
- ✅ github - GitHub集成
- ✅ web-search - AI搜索
- ✅ jina-reader - 网页阅读
- ✅ twitter - Twitter/X监控
- ✅ second-brain - 知识管理
- ✅ **self-improving - 自我改进智能体** 🧠
- ✅ **find-skills - 技能发现助手** 🔍 (新增)

**self-improving 技能说明**:
- **版本**: 1.2.9
- **功能**: 自我反思 + 自我批评 + 自我学习 + 自我组织记忆
- **能力**: 
  - 评估自己的工作质量
  - 发现错误并永久改进
  - 从用户纠正中学习
  - 自动分层存储记忆（HOT/WARM/COLD）
- **使用时机**: 
  - 用户纠正错误时
  - 完成重要工作后自我评估
  - 发现输出可以改进时
- **记忆位置**: `~/self-improving/` (自动创建)
- **文档**: `skills/self-improving/SKILL.md`

**示例场景**:
- 您说:"不对，应该这样做..." → 自动记录到 corrections.md
- 我说:"我注意到刚才的回复可以改进..." → 自我反思并记录
- 相同模式出现3次 → 自动升级到 HOT 记忆

**配置方法**: 编辑各技能目录下的 SKILL.md 和 config.yaml

---

### Markdown转PDF技能 (MD2PDF Converter)
- **位置**: `C:\Users\Administrator\.openclaw\skills\md2pdf-converter\`
- **脚本**: `张实项目总控\06-AHL-去中心化旅行平台\md_to_pdf.py`
- **一键运行**: `转换MD为PDF.bat`
- **依赖**: Python + wkhtmltopdf
- **安装**: https://wkhtmltopdf.org/downloads.html
- **用途**: 将项目文档Markdown转换为专业PDF

**使用方法**:
```bash
# 方式1: 双击运行
转换MD为PDF.bat

# 方式2: 命令行
python md_to_pdf.py
```

---

### Markdown转PPT技能 (MD2PPT Converter)
- **位置**: `C:\Users\Administrator\.openclaw\skills\md2ppt\`
- **脚本**: `md2ppt.py`
- **依赖**: `pip install python-pptx Pillow`
- **功能**: 将Markdown文档转换为路演PPT
- **用途**: 政府申请路演、投资人路演、团队分享

**使用方法**:
```bash
# 批量转换所有文档
python C:\Users\Administrator\.openclaw\skills\md2ppt\md2ppt.py

# 输出位置
C:\Users\Administrator\Desktop\项目说明书\
```

**生成文件**:
- AHL路演-政府申请.pptx
- AHL路演-投资人BP.pptx
- AHL路演-顶层设计.pptx

---

### 提示词工程资源库

#### Awesome ChatGPT Prompts 中文版
- **GitHub**: https://github.com/PlexPt/awesome-chatgpt-prompts-zh
- **描述**: ChatGPT中文调教指南，各种场景使用指南
- **用途**: AIGC文案生成、内容创作、营销文案
- **已整理**: AHL专用版本保存在 `D:\AHL-Database\07-AIGC提示词库\`

**包含场景**:
- 小红书文案生成（酒店种草/民宿体验/促销）
- 抖音短视频脚本（探店/故事）
- 朋友圈文案（入住分享/打卡）
- 邮件营销（会员优惠/B端开发）
- 公众号文章（品牌故事/旅游攻略）
- OTA详情页优化（携程/美团）

**使用方式**:
- 选择合适的提示词模板
- 填入变量信息（酒店名称/特色等）
- 提交给AI生成（Kimi/ChatGPT）
- 人工审核后发布

**更新建议**: 定期关注GitHub仓库，获取新提示词

---

### 网络爬虫与自动化技能（待安装）

**搜索状态**: 已找到相关技能，等待安装（Clawhub速率限制）

#### 1. Web Crawler（网络爬虫）
- **技能名称**: `crawl4ai` (Crawl4AI Web Scraper)
- **功能**: AI驱动的网页爬取和数据提取
- **安装命令**: `npx clawhub install crawl4ai`
- **状态**: ⏳ 待安装（速率限制，稍后重试）

#### 2. Playwright Automation（浏览器自动化）
- **技能名称**: `playwright` 或 `playwright-browser-automation`
- **功能**: 浏览器自动化、MCP集成、网页抓取
- **安装命令**: `npx clawhub install playwright`
- **状态**: ⏳ 待安装

#### 3. Firecrawl Skill
- **技能名称**: `firecrawl-skills` (Firecrawl Skills)
- **功能**: Firecrawl搜索和网页爬取
- **安装命令**: `npx clawhub install firecrawl-skills`
- **状态**: ⏳ 待安装

#### 4. Apify Agent Skills
- **技能名称**: `apify` (Apify)
- **功能**: Apify平台集成，云端爬虫和自动化
- **安装命令**: `npx clawhub install apify`
- **状态**: ⏳ 待安装

#### 5. Decodo Skill
- **技能名称**: `decodo-scraper` (Decodo Scraper)
- **功能**: Decodo网页抓取服务
- **安装命令**: `npx clawhub install decodo-scraper`
- **状态**: ⏳ 待安装

#### 6. Agent-Reach（已存在）
- **类型**: Python包（非OpenClaw Skill）
- **版本**: 1.2.0
- **位置**: C:\Python314\Lib\site-packages
- **克隆位置**: C:\Users\Administrator\Downloads\agent-reach
- **状态**: ✅ 已安装
- **功能**: 网页阅读、YouTube/B站字幕、RSS解析、社交媒体
- **使用指南**: `docs/Agent_Reach_使用指南.md`

---

**安装状态**: 2026-03-05 23:15
- ❌ firecrawl-skills: 多次尝试，速率限制
- ❌ crawl4ai: 速率限制
- ❌ playwright: 速率限制
- ❌ apify: 速率限制
- ⏳ decodo-scraper: 待尝试
- ✅ Agent-Reach: 已安装（Python包）

**问题**: Clawhub速率限制严格，短时间内多次请求被限制

**解决方案**:
方案1: 等待较长时间后重试（建议1-2小时后）
方案2: 明早运行批量安装脚本
```bash
C:\Users\Administrator\.openclaw\scripts\install-crawler-skills.bat
```
方案3: 分时段逐个安装（间隔30分钟以上）

**明日优先安装技能（9个）- P0任务**:
1. 🔥 skill-creator - 技能创建工具（速率限制恢复后安装）
2. 🔥 superpowers - 48k+星标技能集（需搜索确认）
3. 🔥 planning-with-files - 文件规划技能（需搜索确认）
4. 🔥 ui-ux-promax - UI/UX设计技能（需搜索确认）
5. 🔥 firecrawl-skills - 网页爬取（速率限制恢复后安装）
6. 🔥 crawl4ai - AI网页爬取（速率限制恢复后安装）
7. 🔥 playwright - 浏览器自动化（速率限制恢复后安装）
8. 🔥 apify - Apify平台（速率限制恢复后安装）
9. 🔥 decodo-scraper - Decodo抓取（速率限制恢复后安装）

**安装顺序**: 先搜索确认技能存在 → 逐一安装（间隔5分钟以上避免速率限制）
**安装脚本**: `C:\Users\Administrator\.openclaw\scripts\install-crawler-skills.bat`
**优先级**: P0 - 明早首要任务

---

### 用户信息
- **姓名**: 张实
- **电话**: 17760348653
- **微信**: 17760348653 (同号)
- **邮箱**: ericzhangshi@163.com
- **角色**: 所有项目总控

---

Add whatever helps you do your job. This is your cheat sheet.
