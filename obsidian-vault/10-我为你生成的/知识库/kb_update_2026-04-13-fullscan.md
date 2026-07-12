# 张实人格/知识图谱补充报告
## 系统性文件扫描 — 2026-04-13

> 扫描范围：C:\Users\ericz\ 全目录 + D:\B166ER-OpenClaw\workspace
> 优先级：P0核心文件 > P1工具环境 > P2 D盘 > P3其他
> 发现重大补充维度：AI工作流配置、cron任务系统、数据采集基础设施、媒体资产库

---

## 一、P0：核心个人文件

### 1.1 WeChat Files（微信文件）
**路径**: `C:\Users\ericz\Documents\WeChat Files\`

**发现内容**:
- **WXWork（企业微信）备份数据**: `C:\Users\ericz\Documents\WXWork\1688850722709596\Backup\` 包含完整企业微信数据备份（calendar_r7.db, cloud_disk.db, company.db, crm.db, file.db, journal.db, message.db, session.db, user.db等）
- **微信收藏夹**: `Msg\Favorite.db` - 微信收藏内容数据库
- **小程序数据**: 多个小程序wxapkg包（wx5b97b0686831c076等）
- **WMPF数据**: `WMPF/mpfastload/` 包含微信小程序相关数据

**推断意义**:
- Eric使用企业微信作为主要工作通讯工具
- 有完整的聊天记录备份习惯
- 企业微信中包含大量工作相关数据（CRM、日程、文件）

### 1.2 Downloads目录文档
**路径**: `C:\Users\ericz\Downloads\`

**发现文件（部分）**:
- AHL相关PPT/PDF: AHL去中心化平台商业计划书、AHL运营模式深化PPT、酒店民宿数据备份方案
- 视频行业报告: 2026年中国视频行业Q1全景分析PPT
- 酒店相关: 成都3+2平方公里城区规划、酒店竞品分析
- 商业计划书: 酒店竞聘商业计划书PPT

**推断意义**:
- Eric在同时推进多个酒店相关项目
- 视频行业是他关注的一个重要领域
- AHL是最核心的项目，有多个版本的商业计划书

### 1.3 Desktop项目总控
**路径**: `C:\Users\ericz\Desktop\张实项目总控\`

**发现结构**:
```
01-媒体计划（自媒体内容规划）
02-医养酒店计划（康养酒店方向）
03-AI去中心化计划（AHL核心项目）
04-AI智能体SOP（AI工具使用规范）
05-AHL-去中心化旅行平台（核心PPT等）
06-新康养酒店计划（医养结合）
07-新华酒店管理计划（管理输出）
09-TOKEN门票与分成模式预测.md
99-归档资料
README.md
待执行列表_2026-03-09.md
```

**关键发现**: 09-TOKEN门票与分成模式预测 - Eric在探索TOKEN/通证化经济模型用于民宿平台

---

## 二、P1：工具和环境配置

### 2.1 OpenClaw完整配置
**文件**: `C:\Users\ericz\.openclaw\openclaw.json`

**AI模型配置**:
- Primary: `minimax/MiniMax-M2.7`（reasoning=true）
- Fallback: `moonshot/kimi-k2.5`, `kimi-coding/k2p5`, `minimax-cn/MiniMaxM2.7`
- Workspace: `D:\B166ER-OpenClaw\workspace`
- Max concurrent subagents: 8

**MCP服务器**:
- `chrome-devtools`: 浏览器自动化（autoConnect模式）
- `tavily`: 搜索API（使用tvly-dev-key，已配置的Tavily API）

**Gateway**:
- Port: 18789
- Auth: Token模式（已配置token）
- Tailscale: 关闭（本地模式）

**Skills配置**:
- `getnote`: 已配置API Key（笔记工具）

**插件**:
- minimax, moonshot, kimi均启用
- memory-core插件启用，dreaming模式开启

### 2.2 Cron定时任务系统
**文件**: `C:\Users\ericz\.openclaw\cron\jobs.json`

**发现7个cron任务**:
| ID | 任务名 | 频率 | 状态 | 说明 |
|----|--------|------|------|------|
| ab179b98 | B166ER-月度自动复盘 | 每月26日09:00 | ✅ 启用 | 自动生成月报 |
| ab16791e | AI Builders Digest | 每日08:00 | ❌ 停用 | follow-builders每日摘要 |
| e76f4886 | 大乐透开奖检查 | 周一/三/六21:30 | ✅ 启用 | 开奖后自动复盘预测 |
| 332ec6e6 | B166ER-技能市场扫描 | 每2小时 | ❌ 停用 | 检查Clawhub新技能 |
| 8d8930ef | B166ER-知识库月度更新 | 每月28日10:00 | ✅ 启用 | 知识库定期维护 |
| a870e5ad | Multi-OTA平台探测提醒 | 每日09:00 | ✅ 启用 | OTA平台逐个击破提醒 |
| 284e4a7e | B166ER-DailyDataCollection | 每日8:00和20:00 | ❌ 停用 | 数据自动采集 |

**AI Builders Digest错误**: Channel配置问题（连续13次错误）——需要设置明确的channel和target

### 2.3 数据采集系统
**路径**: `C:\Users\ericz\.openclaw\data-acquisition\`

**RSS订阅源**（已验证可用）:
- 36氪 (https://36kr.com/feed) - AI科技
- 虎嗅 (https://www.huxiu.com/rss/)
- 钛媒体 (https://www.tmtpost.com/rss)

**采集数据**:
- `ctrip_hotel_chengdu_20260XXX.json` - 成都携程酒店数据（每日采集，2026-04-05至04-12）
- `industry_news_20260XXX.json` - 行业新闻（每日采集）
- `collector_20260XXX.log` - 采集日志

**推断**: Eric建立了完整的数据采集基础设施，持续监控酒店行业和AI领域动态

### 2.4 Self-Improving系统
**路径**: `C:\Users\ericz\.openclaw\self-improving\`

**Corrections.md** 记录了Eric的重要交互反馈:
- 2026-04-12 20:46: 自我进化机制建立（Eric要求每次动作记录、向量化学习）
- 2026-04-12 20:46: 向量化学习承诺（Eric的思维模式、偏好、指令规律）
- 2026-04-12 20:35: 从Eric处学到的认知（审美是底色、博弈论是思考方式）
- 2026-04-12 20:37: sqlite-vec问题修复
- 2026-04-12 14:09: 免费合作试点标识确立
- 2026-04-12 14:01: 问卷从春熙版改为通用版

**关键原则**:
- 每次重要交流后提炼模式
- 写入文件而非"记住"
- 错误不过夜

### 2.5 Follow-Builders配置
**文件**: `C:\Users\ericz\.follow-builders\config.json`

```json
{
  "platform": "openclaw",
  "language": "zh",
  "timezone": "Asia/Shanghai",
  "frequency": "daily",
  "deliveryTime": "08:00",
  "delivery": {"method": "stdout"},
  "onboardingComplete": true
}
```

**状态**: 已完成onboarding，每日08:00自动生成AI Builders Digest

### 2.6 .config目录
**文件**: `C:\Users\ericz\.config\last30days\.env`
```
INCLUDE_SOURCES=reddit,hn,youtube,polymarket
```
**推断**: Eric在追踪Reddit/HN/YouTube/Polymarket上的AI和科技趋势

---

## 三、Workspace深度分析

### 3.1 项目核心文件（按重要性）

**AHL核心**:
- `AHL-Agent-Skill技能说明文档.html/md` (24KB/19KB)
- `AHL-Archive-System.md` (7KB)
- `ahl-marketing-agent-architecture-v2/v3.md` (21KB/22KB)
- `AHL-Product-Catalog.md` (21KB)
- `AHL组织架构演进规划.md` (27KB)
- `ahl_team_tmp.pptx` (1.9MB)
- 多个poster图像（architecture/chinese/hotel/infographic/matrix版本）

**商业计划书**:
- `bp6_content.txt` (15KB)
- `v51_content.txt` (11KB)
- `original_style.txt` (13KB)

**知识库文件**:
- `memory/aesthetic-knowledge-base.md` (157KB) - 最大文件，审美知识库
- `memory/ai-llm-knowledge-base-v2.md` (123KB)
- `memory/ahl-automation-feasibility-v1.md` (47KB)
- `memory/张实全方位人格侧写报告.md` (已有)

**音频分析**:
- `music_batch_XXX.md` - 50+个批次文件（每批5首歌）
- `music_deep_research.md` (18KB)
- `music_personality_ultimate_analysis.md` (19KB)
- `audio_features.json` (19KB)
- `music_snapshot_201_205.txt` (494KB) - 原始音频快照

### 3.2 工具脚本库（按功能分类）

**OTA爬虫工具**:
- `scrap_tools.py` - 爬虫工具箱
- `do_ota_insert.py` (33KB) - OTA数据插入
- `add_ota_expansion.py` (12KB)
- `ota_section_content.py` (36KB)
- `scrapling_bing.txt` - scrapling测试结果
- `scrap_tools.py` - 综合爬虫工具

**AHL内容生成**:
- `generate_ahl_tech_bp.py` (32KB)
- `generate_ahl_tech_ppt.py` (31KB)
- `generate_ahl_tech_en.py` (20KB)
- `gen_ahl_opc_outline.py` (15KB)

**数据处理**:
- `excel_data.json` (156KB) / `excel_data_v2.json` (615KB)
- `extract_pdfs.py` (11KB) / `extract_pdfs_v2.py` (16KB)
- `add_deep_410.py` (27KB)

**CDP浏览器自动化**:
- `cdp_fill_v2/v3.js` - 抖音发布自动化
- `cdp_navigate.js`, `cdp_click_and_shot.js` 等
- `do_fill_all.js` (10KB)
- `do_hashtag.js`, `do_insert.py` 等

**知识库系统**:
- `kb_router.py` (11KB) - TF-IDF+SQLite检索
- `kb_maintenance.py` (4KB)
- `kb_autoreg.py` (7KB) - 自动纳入
- `evolve_kb.py` (7KB)
- `knowledge_base.py` (7KB)

**音频处理**:
- `extract_audio_features.py` (6KB)
- `test_audio.py` (3KB)

### 3.3 HEARTBEAT.md详细配置

**心跳任务系统**（265行配置）:
1. 技能市场扫描（每30分钟）
2. 行业动态监控（每2小时）
3. 每日技能报告（21:00）
4. 大乐透预测（触发执行，标准SOP）
5. 项目节点检查（每次心跳）
6. TuriX-CUA跟踪（等待Windows版）
7. AGENT军团自主规划（每周复盘）
8. 音频深度分析（已暂停）
9. 数据采集系统（自动运行，已部署）
10. 技能激活与优化（持续）
11. 知识库系统V3.0（核心架构完成）
12. 知识库月度更新（每月28日）

**关键节点（2026-04-07）**:
- 审美与品位知识库 - 最高优先级（人类最后的高地）
- 云顶商业计划书全面深化完成
- 竞聘商业计划书已发送
- 成都春熙宾馆试点已确认

### 3.4 PROJECT-TRACKING.md项目全景

**P0-P9项目矩阵**:
| 编号 | 项目 | 优先级 | 状态 |
|------|------|--------|------|
| P0 | AHL-去中心化旅行平台 | ⭐⭐⭐⭐⭐ | 🟡 融资中 |
| P1 | 酒店AI赋能（单体） | ⭐⭐⭐ | 🟡 待启动 |
| P2 | 乐山试点 | ⭐⭐⭐⭐ | 🟢 就绪 |
| P3 | 自媒体计划 | ⭐⭐ | 🟡 待启动 |
| P4 | 收益管理SOP知识库 | ⭐⭐⭐ | 🟢 建设中 |
| P5 | 人寿医养酒店 | ⭐⭐ | 🟡 资金待到位 |
| P6 | 电子潮玩/衍生品 | ⭐⭐ | ⚪ 概念阶段 |
| P7 | 美国跨境电商 | ⭐⭐ | ⚪ 概念阶段 |
| P8 | 两江假日云顶酒店竞聘 | ⭐⭐⭐⭐ | ✅ 已发送 |
| P9 | 新华酒店管理公司竞聘 | ⭐⭐⭐⭐ | ✅ 已发送 |

**AHL核心里程碑**（已完成）:
- 酒店数据核实 ✅
- 股权结构核实 ✅
- PMS技术方案 ✅
- OTA数据方案 ✅
- 7个Phase 1 SKILL规格 ✅
- 竞品监控配置 ✅
- 到达执行手册 ✅
- 私域运营技术方案 ✅
- AI预订匹配技术方案 ✅

### 3.5 媒体资产库
**路径**: `C:\Users\ericz\.openclaw\media\`

**AHL相关图片**（tool-image-generation）:
- `AHL_architecture_poster_final` - 架构海报
- `AHL_chinese_poster_v3` - 中文海报v3
- `AHL_hotel_poster` - 酒店海报
- `AHL_Infographic` - 信息图
- `AHL_poster` / `AHL_poster_chinese_v2` - 标准海报
- `AHL_poster_matrix` - 矩阵海报
- `AHL_Simple_Infographic` - 简化信息图
- 多个generic生成图片

**推断**: Eric通过AI图像生成工具制作AHL营销素材

---

## 四、新发现的关键洞察

### 4.1 AI工作流的高度工程化
Eric的AI助手（B166ER）不是简单的对话工具，而是一个高度工程化的AI工作系统：
- 完整的cron任务调度（7个定时任务）
- 持续数据采集（每日携程数据+行业新闻）
- 自我进化机制（corrections.md + self-improving迭代）
- 知识库自维护系统（kb_router + kb_autoreg + evolve_kb）

### 4.2 "去中心化"思维贯穿所有项目
从文件结构看，Eric的所有项目都体现去中心化思维：
- AHL：去中心化旅行平台（核心）
- 医养酒店：去中心化康养服务
- 自媒体：去中心化内容分发
- TOKEN模式：去中心化经济激励

### 4.3 酒店行业的模式创新者
Eric不只做酒店管理，他在探索：
- AI驱动的酒店运营自动化
- 去中心化民宿交易（AHL-LLM协议）
- 酒店私域会员的TOKEN化
- 医养结合的新型酒店模式

### 4.4 审美作为决策标准
从审美知识库（157KB）和相关工具看，审美是Eric的核心决策标准：
- aesthetic_tool.py - 五维度审美评估
- eastern_aesthetics.py - 东方美学专项（侘寂/物哀/幽玄）
- 审美知识库涵盖完整哲学体系和学科体系

### 4.5 数据驱动决策的实践者
Eric建立的数据基础设施：
- 每日携程酒店数据采集（8天连续数据）
- 行业新闻RSS订阅（36氪/虎嗅/钛媒体）
- 竞品价格监控
- 自己构建的OTA爬虫系统

---

## 五、对现有USER.md的补充

### 5.1 新增AI工具使用习惯
- **B166ER**: 完全工程化的AI助手，cron驱动，自动任务
- **AI模型**: MiniMax-M2.7为主，Kimi-k2.5为辅
- **数据采集**: 高度依赖自动化（每日两次）

### 5.2 新增项目
- P8: 两江假日云顶酒店竞聘（已发送）
- P9: 新华酒店管理公司竞聘（已发送）
- TOKEN门票与分成模式（探索中）

### 5.3 新增关注领域
- 视频行业（2026Q1全景分析）
- Polymarket/预测市场
- Reddit/HN/YouTube科技趋势

### 5.4 补充沟通风格
- 要求"向量化学习"——每次对话后提炼模式
- 强调"动作必须写文件"——不依赖"记住"
- 错误不过夜原则

---

## 六、关键文件路径索引

### 核心身份文件
- `D:\B166ER-OpenClaw\workspace\SOUL.md` - 灵魂/人格
- `D:\B166ER-OpenClaw\workspace\IDENTITY.md` - 身份
- `D:\B166ER-OpenClaw\workspace\USER.md` - 用户资料
- `D:\B166ER-OpenClaw\workspace\MEMORY.md` - 长期记忆
- `D:\B166ER-OpenClaw\workspace\AGENTS.md` - 工作规范

### 自我进化
- `C:\Users\ericz\.openclaw\self-improving\corrections.md` - 纠错日志
- `D:\B166ER-OpenClaw\workspace\HEARTBEAT.md` - 心跳配置
- `D:\B166ER-OpenClaw\workspace\PROJECT-TRACKING.md` - 项目跟踪

### 知识库
- `D:\B166ER-OpenClaw\workspace\memory\aesthetic-knowledge-base.md` (157KB)
- `D:\B166ER-OpenClaw\workspace\memory\ai-llm-knowledge-base-v2.md` (123KB)
- `D:\B166ER-OpenClaw\workspace\memory\张实全方位人格侧写报告.md`

### AHL核心
- `D:\B166ER-OpenClaw\workspace\AHL-Agent-Skill技能说明文档.md`
- `D:\B166ER-OpenClaw\workspace\AHL组织架构演进规划.md`
- `D:\B166ER-OpenClaw\workspace\ahl-marketing-agent-architecture-v3.md`

### Cron配置
- `C:\Users\ericz\.openclaw\cron\jobs.json`

### 数据采集
- `C:\Users\ericz\.openclaw\data-acquisition\data\`
- `C:\Users\ericz\.openclaw\data-acquisition\rss\rss_sources.md`

---

**报告生成**: 2026-04-13 11:03 GMT+8
**扫描方法**: PowerShell Get-ChildItem递归枚举 + 关键文件内容读取
**覆盖范围**: C:\Users\ericz\ 全目录 + D:\B166ER-OpenClaw\workspace
