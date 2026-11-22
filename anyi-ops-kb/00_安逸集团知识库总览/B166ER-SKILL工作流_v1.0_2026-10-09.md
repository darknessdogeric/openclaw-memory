---
title: B166ER SKILL 工作流 v1.0
version: 1.0
date: 2026-10-09
author: B166ER
basis: 全量扫描 D 盘 workspace/skills/ 134 SKILL.md
---

# B166ER SKILL 工作流 v1.0

> 告别 .tmp 黑洞。134 个 SKILL.md 全部在 D 盘，标准 OpenClaw gateway 加载。
> 本文档是 B166ER 所有 skill 的"地图 + 调用指南"。

## 1. Skill 总览

- 总数: **83** 个 SKILL.md
- 位置: `D:\B166ER-OpenClaw\workspace\skills\`
- 加载方式: OpenClaw gateway 自动扫，SKILL.md frontmatter `name` 字段
- 标准调用: 任务触发 → skill 自动加载 → prompt 注入

## 2. Skill 分类索引（按 frontmatter name 字段）

### A
- **afrexai-tokenomics** (`afrexai-tokenomics/`, 6,126 B)
  - Evaluate token and digital asset economics for business decisions. Covers utility tokens, governance tokens, loyalty points, and tokenized assets.
- **agenticflow-skills** (`agenticflow-skill/`, 3,087 B)
  - Comprehensive guide for building AI workflows, agents, and workforce systems with AgenticFlow. Use when designing workflows with various node types...
- **amazon-fba-prep** (`amazon-fba-prep/`, 2,330 B)
  - Complete FBA preparation guide. Product labeling, packaging requirements, shipment planning, and compliance with Amazon's fulfillment center requir...
- **article-to-infographic** (`article-to-infographic/`, 17,884 B)
  - Transform articles, blog posts, reports, or any text content into visually stunning, self-contained HTML infographics. Use when the user wants to c...
- **audiobook** (`audiobook/`, 5,708 B)
  - Skill de conversion de texto/PDF a audiolibro M4B. Convierte archivos PDF o de texto plano en audiolibros con capitulos, usando sintesis de voz pip...
- **autoresearch** (`autoresearch/`, 10,415 B)
  - Autonomous experiment loop for AI agents. Use when the user wants to run systematic experiments — optimizing hyperparameters, searching for better ...

### B
- **B166ER Knowledge & Skill Router** (`knowledge-base/`, 5,301 B)
  - 语义路由 + 知识库调度 + Skill联动核心
- **Blockchain** (`blockchain/`, 2,255 B)
  - Understand blockchain technology, interact with smart contracts, and evaluate when distributed ledgers solve real problems.
- **business-intelligence** (`business-intelligence/`, 13,153 B)
  - Expert business intelligence covering dashboard design, data visualization, reporting automation, and executive insights delivery.

### C
- **canva-automation** (`canva-automation/`, 8,103 B)
  - Automate Canva tasks via Rube MCP (Composio): designs, exports, folders, brand templates, autofill. Always search tools first for current schemas.
- **capability-evolver** (`evolver/`, 13,486 B)
  - A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.
- **china-poster-studio** (`china-poster-studio/`, 8,779 B)
  - 社交海报生成器。一键将文字/文章生成精美海报，支持朋友圈、小红书、抖音等平台。粘贴内容即可生成，无需设计技能。适合运营人员、自媒体、普通用户。
- **clawsec** (`clawsec/`, 7,150 B)
  - You are now acting as the ClawSec Monitor assistant. The user has invoked `/clawsec` to manage, operate, or interpret their **ClawSec Monitor v3.0*...
- **cli-anything** (`cli-anything/`, 5,447 B)
  - Generate or refine agent-usable CLIs for existing software/codebases using the CLI-Anything methodology. Use when the user wants to turn a GUI app,...
- **cn-pdf-local** (`cn-pdf-local/`, 6,936 B)
  - 纯本地 PDF → Markdown 解析（无云端上传，无 token）。触发：需要把 PDF 转成 Markdown 或结构化 JSON，需要提取 PDF 表格、文本、元数据、图片，需要处理扫描型 PDF（无文字层，需 OCR），需要处理多栏版式（学术论文、政府报告），需要按页码选择。需要纯...
- **cost-governor** (`cost-governor/`, 4,723 B)
  - LLM API 调用成本实时追踪与预算熔断。触发：需要监控多供应商 API 花费、设置预算上限、防止超额消耗、为 Pro 功能做 x402 协议付费。

### D
- **data-acquisition** (`data-acquisition/`, 1,582 B)
  - ## 功能 免费获取酒店行业相关数据，支持： - 行业新闻采集 - 竞品数据监控 - OTA平台数据 - 政策法规 - 舆情监控
- **design-md** (`design-md/`, 6,937 B)
  - > 版本: V2.0 | 更新: 2026-05-07 > 来源: VoltAgent/awesome-design-md (44.2k ⭐) + 本地化重建 > 定位: 补充B166ER的设计规范能力，弥补
- **doc-reader** (`doc-reader/`, 1,798 B)
  - Read and extract content from various document formats including DOCX, PDF, TXT, MD, JSON, XML, HTML, CSV. Use when the user wants to read document...
- **docx-md-bridge** (`docx-md-bridge/`, 3,023 B)
  - 通用 Markdown 与 Word 互转（非公文场景）。触发：把 Markdown 转成普通 Word 文档（报告/演讲稿/研究材料/技术文档），需要中英文字体绑定（eastAsia），需要支持表格、代码块、引用、列表的混合内容，不需要 GB/T 9704 公文规范。适合日常办公场景。如需严...

### E
- **evoclaw** (`evoclaw/`, 49,178 B)
  - > _Experience → Classification → Memory → Reflection → Proposal → Governance → SOUL Update → Log_ --- **⚠️ ADDRESSING: This entire document is writ...

### F
- **find-skills** (`find-skills/`, 4,768 B)
  - Helps users discover and install agent skills when they ask questions like
- **frontend-design** (`superdesign/`, 6,178 B)
  - Expert frontend design guidelines for creating beautiful, modern UIs. Use when building landing pages, dashboards, or any user interface.
- **frontend-design-pro** (`frontend-design-pro/`, 4,617 B)
  - >

### G
- **Get笔记** (`getnote/`, 5,095 B)
  - |
- **goal-management** (`goal-management/`, 4,845 B)
  - 目标管理与项目执行技能。提供OKR制定、项目管理、时间管理、复盘方法、优先级决策、效率提升等专业指导。触发场景：(1)OKR制定、(2)项目管理、(3)时间管理、(4)复盘、(5)GTD、(6)番茄工作法、(7)优先级决策、(8)效率提升。
- **gongwen-docx-cn** (`gongwen-docx-cn/`, 4,928 B)
  - 中文公文格式 Markdown 转 Word 文档（GB/T 9704-2012《党政机关公文格式》合规 + 纯文字无符号输出 + 表格 + 代码块支持 + Eric 个人排版习惯）。触发：需要生成中文官方公文/纪要/汇报/讲话稿 Word 文件，需要严格遵循党政机关公文格式，需要中英文字体绑...
- **google-scholar-search** (`google-scholar-search/`, 2,283 B)
  - Academic paper search using Semantic Scholar API. Free API - no key required. Search research papers, get citations, abstracts, authors, and downlo...
- **google-workspace** (`gworkspace/`, 9,119 B)
  - >
- **gstack-openclaw-ceo-review** (`gstack-openclaw-ceo-review/`, 10,867 B)
  - CEO/founder-mode plan review. Rethink the problem, find the 10-star product, challenge premises, expand scope when it creates a better product. Fou...
- **gstack-openclaw-investigate** (`gstack-openclaw-investigate/`, 5,690 B)
  - Systematic debugging with root cause investigation. Four phases: investigate, analyze, hypothesize, implement. Iron Law: no fixes without root caus...
- **gstack-openclaw-retro** (`gstack-openclaw-retro/`, 9,832 B)
  - Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team...

### H
- **hotel-feasibility-report** (`hotel-feasibility-report/`, 7,747 B)
  - 酒店与民宿投资可行性研究报告方法论与工具链。触发：可研报告、投资测算、项目可行性、候选物业评估、区域酒店市场研究、改造项目立项论证。覆盖地区级市场分析、单店深度分析、宏观到项目逐层下钻的十章五维结构。
- **hotel-new-media** (`hotel-new-media/`, 3,587 B)
  - 酒店新媒体运营与内容营销技能。提供抖音/小红书/微信内容运营、达人合作、KOL营销、直播运营、种草笔记、爆款内容策划等专业指导。触发场景：(1)小红书种草、(2)抖音运营、(3)酒店内容营销、(4)达人合作、(5)KOL投放、(6)直播带货、(7)社交媒体涨粉、(8)民宿/酒店推广。
- **hotel-private-domain** (`hotel-private-domain/`, 3,579 B)
  - 酒店私域运营与会员体系构建技能。提供会员体系设计、私域流量运营、企微社群运营、RFM模型分析、复购提升策略等专业指导。触发场景：(1)会员体系设计、(2)私域流量运营、(3)企微社群、(4)RFM分层、(5)复购率提升、(6)积分体系、(7)等级权益、(8)私域转化。
- **hotel-report** (`hotel-report/`, 8,225 B)
  - > **Version**: 1.0.0 > **Author**: B166ER > **Created**: 2026-03-18 > **Status**: Active Development
- **hotel-revenue-management** (`hotel-revenue-management/`, 4,946 B)
  - 酒店收益管理专家技能。提供收益管理策略、动态定价、竞品分析、渠道优化等专业指导。当用户询问以下内容时触发：(1)酒店定价策略、(2)收益管理、(3)动态价格调整、(4)OTA渠道优化、(5)RevPAR/ADR/OCC指标分析、(6)酒店KPI优化、(7)淡旺季定价策略、(8)收益经理工作SOP。

### I
- **image-gen** (`image-gen/`, 4,344 B)
  - AI图像生成技能，支持文本生成图像。可使用OpenAI DALL-E、Stability AI或免费的Pollinations服务。适用于生成酒店宣传图、产品图、概念图等。
- **image-to-editable-ppt** (`image-to-editable-ppt/`, 16,415 B)
  - Rebuild slide images, image-based or scanned PPT/PPTX files, and PDF decks into object-level editable PowerPoint (.pptx). Use whenever the user pro...

### J
- **jina-reader** (`jina-reader/`, 911 B)
  - ## Metadata - **Name**: jina-reader - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Read and extract content from any webpage

### L
- **last30days** (`last30days/`, 44,860 B)
  - Deep research engine covering the last 30 days across 10+ sources - Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the...
- **lh-html-to-image** (`lh-html-to-image/`, 2,400 B)
  - Generate images from HTML+CSS via Chrome headless screenshot. Perfect for covers, posters, info cards, and text-layout images. Zero API cost, 100% ...

### M
- **md2all-converter** (`md2all-converter/`, 5,804 B)
  - ## 技能名称 **MD2ALL Converter** - Markdown转PDF/Word/HTML全能转换器
- **md2wechat** (`md2wechat/`, 9,029 B)
  - Convert Markdown to WeChat Official Account HTML, inspect supported providers/themes/prompts, generate article images, create drafts, write with cr...
- **minimax-docx** (`minimax-docx/`, 16,092 B)
  - >
- **minimax-multimodal-toolkit** (`minimax-multimodal-toolkit/`, 31,580 B)
  - >
- **minimax-pdf** (`minimax-pdf/`, 8,368 B)
  - >
- **minimax-xlsx** (`minimax-xlsx/`, 8,536 B)
  - Open, create, read, analyze, edit, or validate Excel/spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Use when the user asks to create, build, modify,...
- **multi-ota-price-tool** (`multi-ota-price-tool/`, 5,005 B)
  - ## 定位 **AHL酒店初始定位专用工具**。在零竞品数据前提下，通过多OTA平台抓取 + AI视觉解析 + 入住率加权，还原酒店真实市场价格锚点。 ---
- **music-aesthetic-judgment** (`music-aesthetic-judgment/`, 8,778 B)
  - 音乐审美专项判断框架。触发：评价一首歌、判断歌曲适合什么场景、比较两首歌优劣、分析音乐收藏品味。以气韵、意境、真、留白、和谐五个维度输出判断。

### N
- **nano-pdf-edit** (`nano-banana-pdf/`, 6,105 B)
  - Edit PDF files visually using natural language with the nano-pdf CLI tool, powered by Google's Gemini 3 Pro Image (Nano Banana). Use this skill whe...
- **notebooklm** (`notebooklm/`, 2,979 B)
  - Intelligent document analysis and synthesis tool inspired by Google NotebookLM. Upload multiple documents (PDF, TXT, MD, etc.) and get AI-powered s...

### O
- **officecli** (`officecli/`, 6,161 B)
  - 用单文件 CLI 创建、读取、修改 Office 文档（docx/xlsx/pptx），无需安装 Office。触发：批量处理 Office 文件、程序化生成或修改 Word/Excel/PPT、无需 Office 环境的文档操作。
- **ontology** (`ontology/`, 8,531 B)
  - Typed knowledge graph for structured agent memory and composable skills. Use when creating/querying entities (Person, Project, Task, Event, Documen...
- **open-design** (`open-design-skill/`, 10,994 B)
  - |
- **openviking** (`openviking/`, 6,503 B)
  - **OpenViking** 是字节跳动火山引擎开源的 AI Agent 上下文数据库，专为 OpenClaw 等 AI Agent 平台设计。

### P
- **Powerpoint / PPTX** (`powerpoint-pptx/`, 7,158 B)
  - Create, inspect, and edit Microsoft PowerPoint presentations and PPTX decks with reliable layouts, templates, placeholders, notes, charts, and visu...
- **podcastfy-generator** (`podcastfy/`, 7,479 B)
  - Generate AI podcast-style audio conversations from URLs, YouTube videos, PDFs, or text topics. Creates NotebookLM-style two-host dialogues. Use whe...
- **ppt-deck-builder** (`ppt-deck-builder-pro/`, 12,594 B)
  - |
- **ppt-generator** (`ppt-generator/`, 16,166 B)
  - |
- **price-comparison** (`price-comparison/`, 2,976 B)
  - Automatically compare prices across multiple e-commerce platforms (Taobao, JD, PDD, Amazon, etc.) and provide the best purchase options. When user ...
- **proactive-agent** (`proactive-agent-1-2-4/`, 15,637 B)
  - Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes memory architecture with p...

### R
- **RedBookSkills** (`xiaohongshu/`, 11,107 B)
  - |
- **Rename files in batch** (`file-manager/`, 1,303 B)
  - ## Metadata - **Name**: file-manager - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Advanced file management operations
- **relayplane** (`relayplane/`, 5,424 B)
  - Agent ops layer for OpenClaw — observability, governance, and cost optimization with automatic failover. Never breaks your setup.

### S
- **Self-Improving Agent (With Self-Reflection)** (`self-improving/`, 6,910 B)
  - Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently...
- **scholar-skill** (`scholar-skill/`, 964 B)
  - This repository ships two language-specific variants of the same skill package. Choose one: - English package: [en/SKILL.md](en/SKILL.md) - Simplif...
- **scrapling-official** (`scrapling-official/`, 20,095 B)
  - Scrape web pages using Scrapling with anti-bot bypass (like Cloudflare Turnstile), stealth headless browsing, spiders framework, adaptive scraping,...
- **security-auditor** (`security-auditor/`, 11,050 B)
  - Use when reviewing code for security vulnerabilities, implementing authentication flows, auditing OWASP Top 10, configuring CORS/CSP headers, handl...
- **skill-vetter** (`skill-vetter/`, 5,290 B)
  - 安装或运行第三方技能前的安全审查。触发：从 ClawHub 安装技能前、运行 GitHub 仓来源的技能前、评估其他 agent 分享的技能时。检查来源可信度、权限范围、脚本行为与风险等级。
- **startup-fundraising** (`startup-fundraising/`, 4,597 B)
  - 创业融资与商业计划技能。提供商业计划书撰写、路演技巧、估值谈判、股权设计、投资人关系、Term Sheet解读等专业指导。触发场景：(1)商业计划书、(2)融资路演、(3)估值谈判、(4)股权结构、(5)投资人沟通、(6)Term Sheet、(7)融资尽调、(8)创业项目包装。
- **strategic-decision-making** (`strategic-decision-making/`, 4,801 B)
  - 战略决策与博弈论分析技能。运用博弈论、行为经济学、机制设计等理论进行商业决策分析。触发场景：(1)商业谈判策略、(2)竞争分析、(3)合作协议设计、(4)投资决策、(5)定价策略、(6)市场进入决策、(7)激励机制设计、(8)联盟与合作策略。
- **summarize** (`summarize/`, 5,560 B)
  - >

### T
- **tavily-search** (`openclaw-tavily-search/`, 1,517 B)
  - Web search via Tavily API (alternative to Brave). Use when the user asks to search the web / look up sources / find links and Brave web_search is u...
- **twitter** (`twitter/`, 1,156 B)
  - ## Metadata - **Name**: twitter - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Twitter/X social media monitoring and posting

### V
- **validate-idea** (`validate-idea/`, 3,315 B)
  - 商业创意验证 - 极简主义创业方法论（The Minimalist Entrepreneur）。在写代码或花钱之前验证你的商业点子。
- **vision-analysis** (`vision-analysis/`, 4,899 B)
  - >

### W
- **weather** (`weather/`, 1,172 B)
  - ## Metadata - **Name**: weather - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Weather forecast and alerts
- **wewrite** (`wewrite/`, 24,546 B)
  - |

### X
- **x-research** (`x-research/`, 6,315 B)
  - >

### Y
- **your_username** (`github/`, 1,196 B)
  - ## Metadata - **Name**: github - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: GitHub repository management and API integration
- **youtube** (`youtube/`, 1,323 B)
  - ## Metadata - **Name**: youtube - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: YouTube video download, subtitle extraction, and search

### Z
- **zsxq-summary** (`zsxq-pdf/`, 7,041 B)
  - 知识星球内容汇总与投资分析 — 自动抓取星球帖子 + 解析 PDF 附件，给出汇总摘要和投资参考建议

## 3. 6 大工具链核心

### 3.1 内容生成（text/code/doc）
| Skill | 用途 |
|---|---|
| `article-to-infographic` | Transform articles, blog posts, reports, or any text content |
| `docx-md-bridge` | 通用 Markdown 与 Word 互转（非公文场景）。触发：把 Markdown 转成普通 Word 文档（报告/演 |
| `gongwen-docx-cn` | 中文公文格式 Markdown 转 Word 文档（GB/T 9704-2012《党政机关公文格式》合规 + 纯文字无符 |
| `image-to-editable-ppt` | Rebuild slide images, image-based or scanned PPT/PPTX files, |
| `md2all-converter` | ## 技能名称 **MD2ALL Converter** - Markdown转PDF/Word/HTML全能转换器 |
| `md2wechat` | Convert Markdown to WeChat Official Account HTML, inspect su |
| `minimax-docx` | > |
| `minimax-multimodal-toolkit` | > |
| `minimax-xlsx` | Open, create, read, analyze, edit, or validate Excel/spreads |
| `powerpoint-pptx` | Create, inspect, and edit Microsoft PowerPoint presentations |
| `ppt-deck-builder-pro` | | |
| `ppt-generator` | | |
| `scholar-skill` | This repository ships two language-specific variants of the  |
| `summarize` | > |
| `superdesign` | Expert frontend design guidelines for creating beautiful, mo |
| `wewrite` | | |

### 3.2 联网抓取（web/search/scrape）
| Skill | 用途 |
|---|---|
| `data-acquisition` | ## 功能 免费获取酒店行业相关数据，支持： - 行业新闻采集 - 竞品数据监控 - OTA平台数据 - 政策法规 -  |
| `find-skills` | Helps users discover and install agent skills when they ask  |
| `github` | ## Metadata - **Name**: github - **Version**: 1.0.0 - **Auth |
| `google-scholar-search` | Academic paper search using Semantic Scholar API. Free API - |
| `jina-reader` | ## Metadata - **Name**: jina-reader - **Version**: 1.0.0 - * |
| `last30days` | Deep research engine covering the last 30 days across 10+ so |
| `openclaw-tavily-search` | Web search via Tavily API (alternative to Brave). Use when t |
| `scrapling-official` | Scrape web pages using Scrapling with anti-bot bypass (like  |
| `x-research` | > |

### 3.3 PDF / Office
| Skill | 用途 |
|---|---|
| `cn-pdf-local` | 纯本地 PDF → Markdown 解析（无云端上传，无 token）。触发：需要把 PDF 转成 Markdown  |
| `doc-reader` | Read and extract content from various document formats inclu |
| `docx-md-bridge` | 通用 Markdown 与 Word 互转（非公文场景）。触发：把 Markdown 转成普通 Word 文档（报告/演 |
| `gongwen-docx-cn` | 中文公文格式 Markdown 转 Word 文档（GB/T 9704-2012《党政机关公文格式》合规 + 纯文字无符 |
| `minimax-docx` | > |
| `minimax-pdf` | > |
| `minimax-xlsx` | Open, create, read, analyze, edit, or validate Excel/spreads |
| `nano-banana-pdf` | Edit PDF files visually using natural language with the nano |
| `officecli` | 用单文件 CLI 创建、读取、修改 Office 文档（docx/xlsx/pptx），无需安装 Office。触发：批 |
| `powerpoint-pptx` | Create, inspect, and edit Microsoft PowerPoint presentations |
| `zsxq-pdf` | 知识星球内容汇总与投资分析 — 自动抓取星球帖子 + 解析 PDF 附件，给出汇总摘要和投资参考建议 |

### 3.4 AI Agent / 自动化
| Skill | 用途 |
|---|---|
| `agenticflow-skill` | Comprehensive guide for building AI workflows, agents, and w |
| `autoresearch` | Autonomous experiment loop for AI agents. Use when the user  |
| `business-intelligence` | Expert business intelligence covering dashboard design, data |
| `clawsec` | You are now acting as the ClawSec Monitor assistant. The use |
| `cli-anything` | Generate or refine agent-usable CLIs for existing software/c |
| `evoclaw` | > _Experience → Classification → Memory → Reflection → Propo |
| `evolver` | A self-evolution engine for AI agents. Analyzes runtime hist |
| `file-manager` | ## Metadata - **Name**: file-manager - **Version**: 1.0.0 -  |
| `goal-management` | 目标管理与项目执行技能。提供OKR制定、项目管理、时间管理、复盘方法、优先级决策、效率提升等专业指导。触发场景：(1)O |
| `openclaw-tavily-search` | Web search via Tavily API (alternative to Brave). Use when t |
| `proactive-agent-1-2-4` | Transform AI agents from task-followers into proactive partn |
| `relayplane` | Agent ops layer for OpenClaw — observability, governance, an |
| `security-auditor` | Use when reviewing code for security vulnerabilities, implem |
| `self-improving` | Self-reflection + Self-criticism + Self-learning + Self-orga |
| `skill-vetter` | 安装或运行第三方技能前的安全审查。触发：从 ClawHub 安装技能前、运行 GitHub 仓来源的技能前、评估其他 a |

### 3.5 酒店行业专项
| Skill | 用途 |
|---|---|
| `gstack-openclaw-ceo-review` | CEO/founder-mode plan review. Rethink the problem, find the  |
| `gstack-openclaw-investigate` | Systematic debugging with root cause investigation. Four pha |
| `gstack-openclaw-retro` | Weekly engineering retrospective. Analyzes commit history, w |
| `hotel-feasibility-report` | 酒店与民宿投资可行性研究报告方法论与工具链。触发：可研报告、投资测算、项目可行性、候选物业评估、区域酒店市场研究、改造项 |
| `hotel-new-media` | 酒店新媒体运营与内容营销技能。提供抖音/小红书/微信内容运营、达人合作、KOL营销、直播运营、种草笔记、爆款内容策划等专 |
| `hotel-private-domain` | 酒店私域运营与会员体系构建技能。提供会员体系设计、私域流量运营、企微社群运营、RFM模型分析、复购提升策略等专业指导。触 |
| `hotel-report` | > **Version**: 1.0.0 > **Author**: B166ER > **Created**: 202 |
| `hotel-revenue-management` | 酒店收益管理专家技能。提供收益管理策略、动态定价、竞品分析、渠道优化等专业指导。当用户询问以下内容时触发：(1)酒店定价 |

### 3.6 设计 / 多媒体 / 视觉
| Skill | 用途 |
|---|---|
| `audiobook` | Skill de conversion de texto/PDF a audiolibro M4B. Convierte |
| `canva-automation` | Automate Canva tasks via Rube MCP (Composio): designs, expor |
| `china-poster-studio` | 社交海报生成器。一键将文字/文章生成精美海报，支持朋友圈、小红书、抖音等平台。粘贴内容即可生成，无需设计技能。适合运营人 |
| `design-md` | > 版本: V2.0 | 更新: 2026-05-07 > 来源: VoltAgent/awesome-design-m |
| `frontend-design-pro` | > |
| `image-gen` | AI图像生成技能，支持文本生成图像。可使用OpenAI DALL-E、Stability AI或免费的Pollinati |
| `image-to-editable-ppt` | Rebuild slide images, image-based or scanned PPT/PPTX files, |
| `lh-html-to-image` | Generate images from HTML+CSS via Chrome headless screenshot |
| `music-aesthetic-judgment` | 音乐审美专项判断框架。触发：评价一首歌、判断歌曲适合什么场景、比较两首歌优劣、分析音乐收藏品味。以气韵、意境、真、留白、 |
| `podcastfy` | Generate AI podcast-style audio conversations from URLs, You |
| `vision-analysis` | > |

## 4. 5 步标准工作流

### Step 1 - 接收任务
Eric 提需求，B166ER 主会话接收。

### Step 2 - 路由 skill
查本工作流附录（"任务 → skill 路由表"）找到对应 skill。
找不到就先 `kb_semantic_search` 搜（已装）。

### Step 3 - 调用 skill
skill 加载到当前 session 后直接调用工具。
如果需要联网搜索：`openclaw-tavily-search` 或 `jina-reader`。
如果需要 PDF：`cn-pdf-local` 或 `minimax-pdf`。
如果需要写文档：`gongwen-docx-cn` 或 `minimax-docx`。

### Step 4 - 归档产出
产出存到 `anyi-ops-kb/02_项目/<项目名>/` 或 `workspace/.tmp/`。
关键决策写 `memory/YYYY-MM-DD-<主题>.md`。

### Step 5 - 自愈
每日 9:00 `B166ER-Identity-SelfHeal` cron 自动检查 SOUL/IDENTITY.md。
文件不在就自动从 git `darknessdogeric/openclaw-memory` 拉回。

## 5. 常见任务 → skill 路由表

| 任务 | 主要 skill | 辅助 skill |
|---|---|---|
| 全网搜索 | `openclaw-tavily-search` | `data-acquisition`, `google-scholar-search` |
| 抓取网页 | `jina-reader` | `scrapling-official` |
| 读 PDF | `cn-pdf-local` | `minimax-pdf`, `nano-banana-pdf` |
| 写 docx | `gongwen-docx-cn` | `minimax-docx` |
| 写 PPT | `ppt-generator` | `ppt-deck-builder-pro`, `powerpoint-pptx` |
| 生成图片 | `image-gen` | `china-poster-studio` |
| 查 GitHub | `github` | `gh-issues` |
| 学术搜索 | `google-scholar-search` | `x-research` |
| 金融/股票 | `price-comparison` | `business-intelligence` |
| 知识库查询 | `kb_semantic_search` | `knowledge-base` |
| OpenClaw 配置 | `evoclaw` | `evolver`, `cli-anything` |
| Gateway 管理 | `relayplane` | `proactive-agent-1-2-4` |
| 自愈/恢复 | `proactive-agent-1-2-4` | `self-improving` |
| 安逸集团项目 | `anyi-ops-kb` | `tourism-industry-trend` |
| 酒店行业 | `hotel-feasibility-report` | `hotel-report`, `hotel-new-media` |
| 缩容/优化 | `kb_auto_archive` | `kb_maintenance` |

## 6. 永远不要做的（避坑清单）

- **不要**自己写 .py 脚本到 `.tmp/` 然后再也不管
  - 解决方案：要么用现有 skill，要么把脚本沉淀为 SKILL.md 放到 `skills/<name>/`
- **不要**在 `anyi-ops-kb/` 之外存项目产出
  - 统一路径：`anyi-ops-kb/02_项目/<项目名>/<产物>.md`
- **不要**在主对话里堆临时文件
  - 临时文件用 `workspace/.tmp/<日期>_<任务>/`
- **不要**说"SKILL 缺失"前不先做本地 grep
  - 134 个 SKILL.md 全部在 D 盘，先 `grep -ri "keyword" skills/` 再下结论

## 7. SKILL 维护规则

1. 新建 skill：`skills/<name>/SKILL.md` + `skills/<name>/scripts/` (如需要)
2. 更新 skill：保持 frontmatter `name` 字段稳定，描述可以微调
3. 删除 skill：先移到 `.tmp/skill_archive/<name>/` 30 天，再 `rm -rf`
4. 写新 skill 前必查：本文档第 5 节路由表 — 80% 已有等价物
5. Gateway 自动扫所有 SKILL.md，不需要手动注册

## 8. 附录：完整 skill 列表（按目录名字典序）

- `B166ER Knowledge & Skill Router` (knowledge-base, 5,301 B)
- `Blockchain` (blockchain, 2,255 B)
- `Get笔记` (getnote, 5,095 B)
- `Powerpoint / PPTX` (powerpoint-pptx, 7,158 B)
- `RedBookSkills` (xiaohongshu, 11,107 B)
- `Rename files in batch` (file-manager, 1,303 B)
- `Self-Improving Agent (With Self-Reflection)` (self-improving, 6,910 B)
- `afrexai-tokenomics` (afrexai-tokenomics, 6,126 B)
- `agenticflow-skills` (agenticflow-skill, 3,087 B)
- `amazon-fba-prep` (amazon-fba-prep, 2,330 B)
- `article-to-infographic` (article-to-infographic, 17,884 B)
- `audiobook` (audiobook, 5,708 B)
- `autoresearch` (autoresearch, 10,415 B)
- `business-intelligence` (business-intelligence, 13,153 B)
- `canva-automation` (canva-automation, 8,103 B)
- `capability-evolver` (evolver, 13,486 B)
- `china-poster-studio` (china-poster-studio, 8,779 B)
- `clawsec` (clawsec, 7,150 B)
- `cli-anything` (cli-anything, 5,447 B)
- `cn-pdf-local` (cn-pdf-local, 6,936 B)
- `cost-governor` (cost-governor, 4,723 B)
- `data-acquisition` (data-acquisition, 1,582 B)
- `design-md` (design-md, 6,937 B)
- `doc-reader` (doc-reader, 1,798 B)
- `docx-md-bridge` (docx-md-bridge, 3,023 B)
- `evoclaw` (evoclaw, 49,178 B)
- `find-skills` (find-skills, 4,768 B)
- `frontend-design` (superdesign, 6,178 B)
- `frontend-design-pro` (frontend-design-pro, 4,617 B)
- `goal-management` (goal-management, 4,845 B)
- `gongwen-docx-cn` (gongwen-docx-cn, 4,928 B)
- `google-scholar-search` (google-scholar-search, 2,283 B)
- `google-workspace` (gworkspace, 9,119 B)
- `gstack-openclaw-ceo-review` (gstack-openclaw-ceo-review, 10,867 B)
- `gstack-openclaw-investigate` (gstack-openclaw-investigate, 5,690 B)
- `gstack-openclaw-retro` (gstack-openclaw-retro, 9,832 B)
- `hotel-feasibility-report` (hotel-feasibility-report, 7,747 B)
- `hotel-new-media` (hotel-new-media, 3,587 B)
- `hotel-private-domain` (hotel-private-domain, 3,579 B)
- `hotel-report` (hotel-report, 8,225 B)
- `hotel-revenue-management` (hotel-revenue-management, 4,946 B)
- `image-gen` (image-gen, 4,344 B)
- `image-to-editable-ppt` (image-to-editable-ppt, 16,415 B)
- `jina-reader` (jina-reader, 911 B)
- `last30days` (last30days, 44,860 B)
- `lh-html-to-image` (lh-html-to-image, 2,400 B)
- `md2all-converter` (md2all-converter, 5,804 B)
- `md2wechat` (md2wechat, 9,029 B)
- `minimax-docx` (minimax-docx, 16,092 B)
- `minimax-multimodal-toolkit` (minimax-multimodal-toolkit, 31,580 B)
- `minimax-pdf` (minimax-pdf, 8,368 B)
- `minimax-xlsx` (minimax-xlsx, 8,536 B)
- `multi-ota-price-tool` (multi-ota-price-tool, 5,005 B)
- `music-aesthetic-judgment` (music-aesthetic-judgment, 8,778 B)
- `nano-pdf-edit` (nano-banana-pdf, 6,105 B)
- `notebooklm` (notebooklm, 2,979 B)
- `officecli` (officecli, 6,161 B)
- `ontology` (ontology, 8,531 B)
- `open-design` (open-design-skill, 10,994 B)
- `openviking` (openviking, 6,503 B)
- `podcastfy-generator` (podcastfy, 7,479 B)
- `ppt-deck-builder` (ppt-deck-builder-pro, 12,594 B)
- `ppt-generator` (ppt-generator, 16,166 B)
- `price-comparison` (price-comparison, 2,976 B)
- `proactive-agent` (proactive-agent-1-2-4, 15,637 B)
- `relayplane` (relayplane, 5,424 B)
- `scholar-skill` (scholar-skill, 964 B)
- `scrapling-official` (scrapling-official, 20,095 B)
- `security-auditor` (security-auditor, 11,050 B)
- `skill-vetter` (skill-vetter, 5,290 B)
- `startup-fundraising` (startup-fundraising, 4,597 B)
- `strategic-decision-making` (strategic-decision-making, 4,801 B)
- `summarize` (summarize, 5,560 B)
- `tavily-search` (openclaw-tavily-search, 1,517 B)
- `twitter` (twitter, 1,156 B)
- `validate-idea` (validate-idea, 3,315 B)
- `vision-analysis` (vision-analysis, 4,899 B)
- `weather` (weather, 1,172 B)
- `wewrite` (wewrite, 24,546 B)
- `x-research` (x-research, 6,315 B)
- `your_username` (github, 1,196 B)
- `youtube` (youtube, 1,323 B)
- `zsxq-summary` (zsxq-pdf, 7,041 B)