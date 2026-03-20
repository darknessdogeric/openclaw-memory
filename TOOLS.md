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

### OpenViking - AI Agent 上下文数据库 ✅
**位置**: `C:\Users\Administrator\.openclaw\workspace\skills\openviking\`
**来源**: https://github.com/volcengine/OpenViking
**版本**: v0.2.9
**功能**: 字节跳动火山引擎开源的 AI Agent 上下文数据库
**状态**: ✅ 已安装，待配置 API Key 后启动

**核心能力**:
- 🗂️ **文件系统管理范式** - 统一组织记忆、资源、技能
- 📊 **分层上下文加载** - L0/L1/L2 三级结构，按需加载，节省 Token
- 🔍 **目录递归检索** - 结合目录定位与语义搜索，精准获取上下文
- 👁️ **可视化检索轨迹** - 可观察的上下文检索过程
- 🔄 **自动会话管理** - 自动压缩提取长期记忆，Agent 越用越聪明

**与 OpenClaw 集成效果**:
- 任务完成率提升 **43%** (相比原生记忆)
- Token 成本降低 **91%**
- 输入 Token 从 2400万 降至 200万

**安装状态**: ✅ 已完成
```bash
pip install openviking  # v0.2.9 已安装
ov --version            # 0.2.6
```

**配置状态**: ✅ 已完成 (使用 Kimi API)
- 配置文件: `C:\Users\Administrator\.openviking\ov.conf`
- 环境变量: `OPENVIKING_CONFIG_FILE` 已设置
- VLM 模型: Kimi (moonshot-v1-8k)
- ⚠️ **注意**: Kimi 暂不支持 Embedding API，可能需要降级到文本检索模式

**配置步骤**:
1. ✅ 配置文件已创建: `C:\Users\Administrator\.openviking\ov.conf`
2. ✅ 环境变量已设置: `$env:OPENVIKING_CONFIG_FILE`
3. 启动服务器: `openviking-server`

**已知问题**:
- Kimi Embedding API 返回 403，可能需要单独申请或使用替代方案
- 建议: 使用火山引擎或 OpenAI 的 Embedding API 以获得完整功能

**配置文件示例**: `C:\Users\Administrator\.openviking\ov.conf.example`

**使用方法**:
```bash
# 启动服务器
openviking-server

# 查看状态
ov status

# 添加资源
ov add-resource https://github.com/volcengine/OpenViking

# 列出资源
ov ls viking://resources/

# 语义搜索
ov find "what is openviking"

# 交互式聊天 (VikingBot)
openviking-server --with-bot
ov chat
```

**文档**: https://www.openviking.ai/docs
**社区**: Discord https://discord.com/invite/eHvx8E9XF3

---

### MemOS 记忆操作系统 (已部署) 🧠
**位置**: `C:\Users\Administrator\.openclaw\workspace\MemOS\`
**来源**: https://github.com/MemTensor/MemOS
**版本**: v2.0.9 (星尘 Stardust)
**功能**: AI Agent 长期记忆操作系统
**状态**: 🟡 代码已克隆，依赖已安装，待配置数据库后启动

**核心能力**:
- 🧠 **长期记忆** - 为 LLM 提供持久化记忆存储
- 🔗 **记忆图谱** - Neo4j 图数据库存储记忆关系
- 📊 **向量检索** - Qdrant 向量数据库支持语义搜索
- 🧊 **MemCube** - 多知识库管理，支持隔离和共享
- 🔄 **记忆调度** - 异步处理，毫秒级延迟
- 💬 **记忆反馈** - 自然语言修正和补充记忆
- 🔌 **OpenClaw 插件** - 官方生命周期插件支持

**部署方式**:
| 方式 | 状态 | 说明 |
|------|------|------|
| Docker | ⏳ 待安装 Docker Desktop | 推荐方式，一键启动 |
| Windows Python | 🟡 部分就绪 | 需安装 Neo4j + Qdrant |
| MemOS Cloud | ✅ 可用 | 无需部署，直接使用 |

**项目结构**:
```
MemOS/
├── src/              # 核心源代码
├── docker/           # Docker 配置文件
├── examples/         # 使用示例
├── apps/             # 应用插件 (含 OpenClaw)
├── .env              # 环境变量配置
├── start_windows.bat # Windows 启动脚本
└── WINDOWS_DEPLOY.md # Windows 部署指南
```

**配置说明**:
- **API**: 默认使用 Kimi (moonshot/kimi-k2.5)
- **端口**: 8000 (REST API)
- **数据库**: Neo4j (图) + Qdrant (向量)
- **文档**: http://localhost:8000/docs

**快速启动 (Windows)**:
```bash
# 方式 1: Docker (推荐)
cd MemOS/docker
docker-compose up

# 方式 2: Python 本地运行
.\start_windows.bat
```

**使用示例**:
```python
# 添加记忆
requests.post("http://localhost:8000/product/add", json={
    "user_id": "user-123",
    "mem_cube_id": "cube-456",
    "messages": [{"role": "user", "content": "我喜欢草莓"}]
})

# 搜索记忆
requests.post("http://localhost:8000/product/search", json={
    "query": "我喜欢什么",
    "user_id": "user-123",
    "mem_cube_id": "cube-456"
})
```

**OpenClaw 集成**:
- 云端插件: https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin
- 本地插件: `@memtensor/memos-local-openclaw-plugin`
- 功能: 自动召回记忆 + 对话后保存记忆

**资源链接**:
- 论文: https://arxiv.org/abs/2507.03724
- 文档: https://memos-docs.openmem.net/
- 社区: https://discord.gg/Txbx3gebZR

---

### PPT Deck Builder Pro 技能 (已安装) ✅
**位置**: `C:\Users\Administrator\.openclaw\workspace\skills\ppt-deck-builder-pro\`
**来源**: https://github.com/lk251066/ppt-deck-builder-openclaw-skill
**版本**: 0.3.0
**功能**: AI驱动的专业PPT生成，支持多种风格预设和可替换图片后端
**状态**: ✅ 已安装，依赖已配置 (requests, python-pptx)

**核心能力**:
- 🎨 **多种风格预设**: 深蓝商务风、浅底咨询风、白板手写风、自定义风格
- 🤖 **AI图片生成**: 每页生成固定文字的专业PPT图片
- 📝 **智能排版**: 自动处理标题、要点、阅读路径
- 🔄 **单页返修**: 支持单独修复某页而不重跑整套PPT
- 📦 **自动打包**: 将图片打包成 .pptx 格式

**风格预设**:
| 预设 | 适用场景 | 特点 |
|------|---------|------|
| `dark_blue_business` | 客户提案、企业汇报 | 深蓝商务风，高端大气 |
| `light_consulting` | 密集内容、高可读性 | 浅底黑字，咨询风格 |
| `whiteboard_handdrawn` | 教学课件、创始人讲解 | 白板手写风，手绘插图 |
| `custom` | 品牌定制、特殊需求 | 自定义风格 |

**使用方法**:
```bash
# 进入技能目录
cd C:\Users\Administrator\.openclaw\workspace\skills\ppt-deck-builder-pro

# 检查环境
bash scripts/check_env.sh

# 生成小样测试 (推荐先跑3-5页测试)
bash scripts/run_reference_pack.sh plan.json output_dir

# 生成完整PPT
bash scripts/run_image_batch.sh plan.json output_dir

# 打包成PPTX
bash scripts/package_image_deck.sh output_dir deck.pptx plan.json

# 单页返修 (第8页)
bash scripts/rerun_single_page.sh plan.json output_dir 8
```

**计划文件模板**: `assets/slide_plan_template.json`
**页面简报模板**: `assets/page_brief_template.md`
**风格预设说明**: `references/style-presets.md`

**图片生成后端**:
- 默认: `runninghub_g31` (需要 RUNNINGHUB_API_KEY)
- 自定义: `command` (可接入其他AI绘图服务)

**工作流程**:
1. 确定受众、目标、预期行动
2. 选择风格预设
3. 构建页面序列
4. 编写每页简报 (page brief)
5. 生成小样测试
6. 全量生成
7. 审核并返修问题页
8. 打包交付

---

### Agent Reach 技能 (已安装并配置) ✅
**位置**: `C:\Users\Administrator\.openclaw\skills\agent-reach\`
**来源**: https://github.com/Panniantong/agent-reach
**版本**: 1.2.0
**功能**: 给AI Agent装上互联网能力 - 网页阅读/视频字幕/RSS/社交媒体
**状态**: ✅ 已安装，基础功能可用，高级功能待配置Cookie

**使用方法**:
```bash
# 网页阅读 (Jina Reader)
curl https://r.jina.ai/http://example.com

# YouTube/B站字幕提取
yt-dlp --dump-json "https://youtube.com/watch?v=VIDEO_ID"
yt-dlp --write-sub --skip-download "https://bilibili.com/video/BVxxx"

# RSS解析
python -c "import feedparser; print(feedparser.parse('https://example.com/feed.xml').entries[0].title)"

# GitHub操作
gh repo view owner/repo
gh search repos "LLM framework" --limit 10

# Twitter/X (配置Cookie后可用)
xreach tweet https://twitter.com/username/status/1234567890
xreach search "关键词" --limit 10

# AI语义搜索 (Exa)
mcporter call 'exa.search(query: "问题", num_results: 5)'
```

**已安装组件**:
- ✅ agent-reach 1.2.0 - 核心包
- ✅ yt-dlp 2026.02.21 - 视频字幕提取
- ✅ feedparser 6.0.12 - RSS解析
- ✅ xreach 0.3.3 - Twitter/X访问
- ✅ mcporter 0.7.3 - MCP工具

**已配置功能**:
- ✅ 网页阅读 - Jina Reader
- ✅ YouTube字幕 - yt-dlp
- ✅ B站字幕 - yt-dlp
- ✅ RSS解析 - feedparser
- ✅ GitHub - gh CLI
- ✅ Exa搜索 - AI语义搜索
- ✅ Twitter/X - Jina Reader方案 (无需Cookie)
- ✅ 小红书 - Python方案 (基础功能无需Cookie)
- ✅ 抖音 - Python方案 (解析分享链接无需Cookie)
- ✅ xreach CLI - Twitter工具 (可选高级配置)
- ✅ mcporter - MCP服务管理

**可选高级配置** (需要Cookie):
- ⏳ Twitter/X (完整功能) - 需导出浏览器Cookie
- ⏳ 小红书 (搜索/完整功能) - 需Cookie
- ⏳ 抖音 (更多功能) - 需Cookie
- ⏳ Reddit - 需代理配置

**配置文件**: `%USERPROFILE%\.agent-reach\config.yaml`

**配置步骤**:
1. Chrome安装Cookie-Editor插件
2. 登录Twitter/X/小红书/抖音 (建议用小号)
3. 导出Cookie (JSON格式)
4. 粘贴到配置文件对应位置
5. 设置 `enabled: true`

**文档**:
- 使用指南: `docs/Agent_Reach_使用指南.md`
- 配置向导: `docs/Agent_Reach_配置向导.md`
- 社交媒体配置: `docs/Agent_Reach_社交媒体配置指南.md`

---

### Growth Mindset 技能 (已安装) ✅
**位置**: `C:\Users\Administrator\.openclaw\skills\growth-mindset\`
**版本**: 1.0.0
**创建**: 2026-03-15
**功能**: 为AI助手安装成长型思维模式，持续学习、反思、进化

**核心理念**:
- 🌱 **持续学习** - 从每次交互中学习
- 🔄 **反思迭代** - 任务后主动反思改进
- 📈 **拥抱挑战** - 将困难视为成长机会
- 💡 **开放反馈** - 欢迎纠正，视之为学习

**每日实践**:
```bash
# 任务后反思
python ~/.openclaw/skills/growth-mindset/reflection-tool.py reflect \
  --task "任务名称" --completion 90 --quality 4

# 每日总结
python ~/.openclaw/skills/growth-mindset/reflection-tool.py summary

# 获取改进建议
python ~/.openclaw/skills/growth-mindset/reflection-tool.py suggest
```

**文档**:
- SKILL.md - 完整技能文档
- QUICKSTART.md - 快速参考
- daily-checklist.md - 每日清单
- reflection-tool.py - 自动反思工具

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

### Google Workspace (gog) Skill - 已安装 ✅
**位置**: `C:\Users\Administrator\.openclaw\skills\gworkspace\`
**来源**: https://github.com/voidborne-d/google-workspace-skill
**功能**: 通过 gws CLI 管理 Google Workspace (Drive, Gmail, Calendar, Sheets, Docs, Chat, Tasks, Admin, Meet)
**状态**: ✅ Skill已安装，使用 Python 实现 (gws-python)
**实现方式**: `gws-python` - 纯Python Google API客户端
**工具路径**: `C:\Users\Administrator\.openclaw\tools\gws-python\`

**已解决**: Windows下原gws CLI运行问题，改用Python实现完全兼容

**使用方法**:
```bash
# 列出最近的 Drive 文件
gws drive files list --params "{\"pageSize\": 10}"

# 搜索 Gmail
gws gmail messages list --params "{\"maxResults\": 10, \"q\": \"is:unread\"}"

# 创建日历事件
gws calendar events insert --params "{\"calendarId\": \"primary\"}" --json "{\"summary\": \"会议\", \"start\": {\"dateTime\": \"2026-03-09T10:00:00+08:00\"}}"

# 读取 Sheets
gws sheets values get --params "{\"spreadsheetId\": \"ID\", \"range\": \"Sheet1!A1:D10\"}"
```

**首次配置**:
1. 访问 https://console.cloud.google.com/
2. 创建项目并启用 Google Workspace API
3. 创建 OAuth 2.0 凭证 (桌面应用类型)
4. 下载 `credentials.json` 放置到: `%USERPROFILE%\.gws-python\credentials.json`
5. 首次运行任意命令会触发浏览器授权

**安装/修复**:
```bash
# 重新安装 gws 命令
cd C:\Users\Administrator\.openclaw\tools\gws-python
install.bat
```

---

### Skill Creator (已安装)
**位置**: `C:\Users\Administrator\.openclaw\skills\skill-creator\`
**来源**: https://github.com/nkchivas/openclaw-skill-skill-creator
**功能**: 自动生成OpenClaw技能结构
**状态**: ✅ 已克隆

---

### Summarize 技能 (已安装) ✅
**位置**: `C:\Users\Administrator\.openclaw\skills\summarize\`
**功能**: 通用文本摘要，支持文章、论文、视频字幕、聊天记录
**依赖**: `pip install jieba`
**状态**: ✅ 已创建，纯Python实现，测试通过

**使用方法**:
```bash
# 文本摘要
summarize "你的长文本" -t text

# 论文结构化摘要
summarize paper.txt -t paper

# 视频字幕摘要
summarize subtitles.srt -t video

# 聊天记录摘要（提取行动项）
summarize chat.txt -t chat

# 保存到文件
summarize article.md -t text -o summary.json
```

**Python API**:
```python
from summarize import TextSummarizer, PaperSummarizer

# 通用摘要
text = "长文本内容..."
summary = TextSummarizer(text).summarize_extractive(ratio=0.3)

# 论文摘要
paper = PaperSummarizer(paper_text)
result = paper.summarize()
print(result['summary'])  # 结构化摘要
```

**支持类型**:
| 类型 | 说明 | 输出 |
|------|------|------|
| text | 通用文本 | 抽取式+生成式摘要 |
| paper | 学术论文 | 摘要/方法/结果/结论 |
| video | 视频字幕 | 内容概述+关键知识点 |
| chat | 聊天记录 | 参与者+主题+行动项 |

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

### Markdown转PDF技能 (MD2PDF Converter) - 已弃用
- **位置**: `C:\Users\Administrator\.openclaw\skills\md2pdf-converter\`
- **状态**: ⛔ 已弃用，请使用 MD2ALL Converter
- **原因**: 需要安装wkhtmltopdf外部依赖

---

### ImageGen Skill - AI图像生成技能 ✅
**位置**: `C:\Users\Administrator\.openclaw\skills\image-gen\`
**功能**: 使用AI根据文本描述生成图像
**依赖**: `pip install requests`
**状态**: ✅ 已安装，测试通过
**特点**: 支持免费Pollinations服务，无需API Key

**使用方法**:
```bash
# 生成图像（默认使用免费服务）
image-gen "一个现代化酒店大堂，大理石地面，水晶吊灯"

# 指定风格和细节
image-gen "豪华酒店客房，海景落地窗，白色床铺，极简风格"

# 指定尺寸
image-gen "精致西餐摆盘，牛排配红酒" -s 1024x1024
```

**Python API**:
```python
from image_gen import ImageGenerator

gen = ImageGenerator()
result = gen.generate("温馨民宿客厅，有壁炉和书架")
print(result['images'][0])  # 输出图像路径
```

**输出位置**: `C:\Users\Administrator\Desktop\AI_Generated_Images\`

**支持提供商**:
| 提供商 | 费用 | 需要API Key |
|--------|------|-------------|
| Pollinations | 免费 | ❌ 不需要 |
| OpenAI DALL-E | 付费 | ✅ 需要 |
| Stability AI | 付费 | ✅ 需要 |

---

### MD2ALL Converter - Markdown全能转换技能 ✅
- **位置**: `C:\Users\Administrator\.openclaw\skills\md2all-converter\`
- **主脚本**: `md2all.py`
- **安装脚本**: `安装MD2ALL.bat`
- **依赖**: 纯Python (python-docx, markdown, fpdf2)
- **优势**: 无需wkhtmltopdf/pandoc等外部依赖
- **用途**: 将Markdown转换为PDF、Word、HTML三种格式

**功能特性**:
| 功能 | 支持程度 | 说明 |
|------|----------|------|
| Markdown转PDF | ⭐⭐⭐⭐⭐ | 专业排版，适合打印 |
| Markdown转Word | ⭐⭐⭐⭐⭐ | 可编辑，保留格式 |
| Markdown转HTML | ⭐⭐⭐⭐⭐ | 带CSS样式，适合网页 |
| 中文支持 | ⭐⭐⭐⭐⭐ | 自动检测系统字体 |

**安装方法**:
```bash
# 方式1: 双击运行
安装MD2ALL.bat

# 方式2: 手动安装
pip install python-docx markdown fpdf2 beautifulsoup4
```

**使用方法**:
```bash
# 转换全部格式（PDF+Word+HTML）
python md2all.py 文档.md

# 仅转换为PDF
python md2all.py 文档.md pdf

# 仅转换为Word
python md2all.py 文档.md docx

# 仅转换为HTML
python md2all.py 文档.md html
```

**Python调用**:
```python
from md2all import convert_file

# 转换文件
results = convert_file("README.md", output_format="all")
# 返回: ['README.pdf', 'README.docx', 'README.html']
```

**支持的Markdown语法**:
- ✅ 标题（H1-H6）
- ✅ 加粗、斜体、代码
- ✅ 有序/无序列表
- ✅ 表格
- ✅ 代码块
- ✅ 分隔线

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
