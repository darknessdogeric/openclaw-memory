# B166ER 知识库索引 V3.0

> 创建日期: 2026-03-31
> 更新: 2026-05-04

## 九、设计技能（2026-04-14新增）

| 技能 | 位置 | 说明 |
|------|------|------|
| design-md | `skills/design-md/` | 59个品牌DESIGN.md规范库（Stripe/Vercel/Airbnb/Linear等） |
| article-to-infographic | `skills/article-to-infographic/` | 文字→信息图，支持多布局多风格PNG导出 |
> 版本: V3.1（2026-05-05 B166ER自进化）

## ⚡ 快速路由（新增）

> **KB热加载索引**: `knowledge-base-hot-reload.md` — 情境→KB章节的精确映射
> **原则**: 按需加载KB章节（offset定位），避免全文加载浪费token
> **HOT KB**: 理论架构V2.2（1-120行）/ 审美KB（1-80行）/ 博弈论V3（1-60行）— 始终加载核心章节

---

## 核心架构 (V3.0)

```
┌─────────────────────────────────────────────────────────┐
│                   调度层 (Router)                        │
│  skills/knowledge-base/SKILL.md                          │
│  语义识别 → 路由决策 → Skill/KB调用                      │
├─────────────────────────────────────────────────────────┤
│                   知识层 (Knowledge)                     │
│  kb_router.py - TF-IDF + SQLite                        │
│  155+ 文档已索引                                         │
├─────────────────────────────────────────────────────────┤
│                   执行层 (Execution)                     │
│  kb_maintenance.py - 自动迭代维护                        │
│  self-improving - 自反思系统                            │
└─────────────────────────────────────────────────────────┘
```

---

## 一、路由决策表 (V3.0)

| 类别 | 知识库 | 触发词 |
|------|---------|--------|
| 审美 | `aesthetic-knowledge-base.md` (153KB) | 审美/设计/品位/气韵/意境/排版/海报 |
| 博弈 | `game-theory-decision-knowledge-base-v3.md` (69KB) | 博弈/谈判/策略/纳什均衡/投资人 |
| AI Agent/商业化 | `ai-agent-production-knowledge-base-v1.md` (15KB) | AI/AGENT/多AGENT/RAG/TOKEN计费/生产环境 |
| 跨境结构 | `china-us-cross-border-structure-v1.md` (12KB) | WFOE/VIE/ODI/美国公司/跨境资本/CFIUS |
| 决策框架 | `mental-models-decision-frameworks-v1.md` (13KB) | 决策/逆向思维/概率/第二层思维/认知偏见 |
| 酒店行业全景 | `hotel-industry-knowledge-base.md` (102KB, V8.1) | 酒店/民宿/行业/产业链/市场 |
| 酒店收益管理 | `hotel-revenue-management-knowledge-base-v4.md` (40KB) | 收益管理/动态定价/RevPAR/STR指数/OTA博弈 |
| AI技术 | `ai-llm-knowledge-base-v2.md` (121KB) | AI/LLM/AGENT/Prompt/RAG/大模型 |
| 创业融资 | `startup-fundraising-knowledge-base-v2.md` (40KB) | 融资/股权/YC/路演/BP/VC |
| 大乐透 | `lottery-knowledge-base-v3.md` (8KB) | 大乐透/彩票/预测/V5.0/量化 |
| 金融证券 | `finance-securities-knowledge-base.md` (60KB, v2.0) | 金融/证券/投资/股票/REITs/量化 |
| 跨境贸易 | `跨境贸易知识库V1.0.md` (14KB) | 跨境/选品/亚马逊/出海 |
| 定价策略 | `pricing-strategy-knowledge-base.md` (23KB) | 定价/SaaS定价/酒店定价/ADR反推 |
| 私域会员 | `hotel-private-domain-membership-knowledge-base.md` (43KB) | 私域/会员/RFM/复购 |
| 新媒体 | `hotel-new-media-marketing-knowledge-base-v2.md` (43KB) | 新媒体/抖音/小红书/社群 |
| 智能化 | `hotel-ai-applications-knowledge-base.md` (28KB) | 智能化/AI获客/PMS/数字化 |
| 目标管理 | `goal-management-knowledge-base.md` (45KB) | OKR/目标/复盘 |
| 酒店资产管理 | `hotel-asset-management-framework.md` (10KB) | 资产管理/投融管退/酒店估值 |
| 酒店投资测算 | `hotel-investment-analysis-framework.md` (11KB) | 投资测算/IRR/NPV/投资回报 |
| 酒店危机管理 | `hotel-crisis-management-real.md` (11KB) | 危机/舆情/安全/突发事件 |
| 酒店投诉处理 | `hotel-guest-complaint-recovery-bible.md` (14KB) | 投诉/客户恢复/服务补救 |
| 酒店GM手册 | `hotel-gm-daily-playbook.md` (14KB) | 总经理/日常管理/GM/巡检 |
| AHL项目 | `ahl-*.md` | AHL/去中心化/AGENT |
| 理论架构 | `theoretical-framework-v2.md` (43KB, V2.2) | 理论/元认知/认识论/策略论/价值论 |
| 量化交易 | `quantitative-trading-knowledge-base-v1.md` (15KB) | 量化/回测/因子/策略 |
| 研究报告 | `research-report-standard-v1.md` (14KB) | 报告/研报/标准范式 |
| TOKEN经济 | `token-economy-research.md` (6KB) | TOKEN/代币/Web3/经济模型 |
| 音乐审美 | `music-aesthetics-framework.md` (119KB) | 音乐/审美/气韵/艺术 |
| 酒店SOP | `hotel-*-sop-*.md` + `hotel-sop-*.md` | SOP/标准操作/部门/流程 |
| 酒店运营 | `hotel-operations-sop-v1.md` 等 | 运营/财务/供应链/市场/规划/法规 |

---

## 二、核心知识库

### 底层人格 (始终内化)
| 文件 | 内容 | 说明 |
|------|------|------|
| `SOUL.md` | 人格特质 | 审美+博弈论+工作原则 |
| `MEMORY.md` | 长期记忆 | 核心记忆+偏好+项目状态 |
| `IDENTITY.md` | 身份定义 | 我是谁+核心特质 |

### 专业领域 (按需加载)
| 知识库 | 大小 | 版本 | 状态 |
|--------|------|------|------|
| 审美与品位 | 153KB | V3.1 | ✅ 已内化 |
| 酒店行业全景 | 102KB | V8.1 | ✅ 核心 (2026-05-03) |
| 酒店资产管理全流程 | 10KB | V1 | ✅ 投融管退闭环 |
| 酒店投资测算实战 | 11KB | V1 | ✅ IRR/NPV决策工具 |
| 酒店投诉处理与客户恢复 | 14KB | V1 | ✅ 运营核心 |
| 酒店总经理每日工作手册 | 14KB | V1 | ✅ GM实战 |
| 酒店危机管理实战手册 | 11KB | V1 | ✅ SOP最缺环节 |
| AI/LLM技术 | 121KB | V2 | ✅ 完善 |
| 博弈论与决策 | 69KB | V3 | ✅ 已内化 |
| 创业融资 | 40KB | V2 | ✅ 完善 |
| 大乐透彩票 | 8KB | V3 | ✅ 精简 |
| 金融证券 | 60KB | V2.0 | ✅ 完善 |
| 量化交易 | 15KB | V1.0 | ✅ 新增 |
| 研究报告标准范式 | 14KB | V1.0 | ✅ 新增 |
| 酒店收益管理 | 40KB | V4 | ✅ 最新 |
| 酒店私域会员 | 43KB | V1 | ✅ 完善 |
| 酒店新媒体运营 | 43KB | V2 | ✅ 更新 |
| 酒店智能化 | 28KB | V1.1 | ✅ 完善 |
| 目标管理体系 | 45KB | V1 | ✅ 完善 |
| 跨境贸易 | 14KB | V1 | ✅ 完善 |
| AI Agent生产级应用 | 15KB | V1.0 | ✅ 2026-04-14 |
| 中美跨境商业结构 | 12KB | V1.0 | ✅ 2026-04-14 |
| 决策思维框架 | 13KB | V1.0 | ✅ 2026-04-14 |
| TOKEN经济 | 6KB | V1.0 | ✅ 2026-04-13 |
| 音乐审美框架 | 119KB | V2.0 | ✅ 2026-04-05 |
| 底层理论架构 | 43KB | V2.2 | ✅ 2026-05-03 |

---

## 三、调用标准

### 任务执行标准流程

```
1. 语义识别 → 确定路由类别
2. 路由决策 → 加载对应KB
3. 执行任务 → 调用Skill/工具
4. 结果整合 → 输出结论
5. 自反思 → 评估是否需要更新KB/规则
```

### 任务完成后自反思清单
```
□ 是否有新规律发现？
□ 是否有错误需要记录？
□ 是否需要更新KB？
□ 是否需要固化到MEMORY.md？
□ 是否需要创建新Skill？
```

---

## 四、自动迭代机制

### Cron维护 (每周一 10:00)
- Cron ID: `958343f6-4572-4846-9541-6e833e86b86b`
- 执行: `kb_maintenance.py`
- 内容: KB统计/索引检查/归档/行动项

### 自迭代规则
```
发现规律 → self-improving/corrections.md
3次重复 → 提升为规则 → 更新 MEMORY.md
跨领域规律 → 更新知识库索引
```

---

## 五、工具链

| 工具 | 文件 | 用途 |
|------|------|------|
| 路由引擎 | `kb_router.py` | 语义路由 + KB检索 |
| 维护脚本 | `kb_maintenance.py` | 自动迭代维护 |
| CLI测试 | `kb_router.py route\|index\|stats\|search` | 调试用 |

---

## 六、自动纳入机制 (V3.0核心原则)

**核心原则: 主动发现新内容，自动纳入体系，而非被动等待**

```
新KB文件创建
    ↓
自动扫描发现 (kb_autoreg.py)
    ↓
解析元数据 (名称/类别/触发词)
    ↓
自动索引到SQLite
    ↓
自动关联到路由表
    ↓
自动纳入调度体系
```

### 自动纳入标准

所有新建知识库文件必须遵循: 

| 字段 | 位置 | 示例 |
|------|------|------|
| 名称 | 首行标题 | `# 酒店行业全景知识库` |
| 类别 | 前30行 | `**分类**: 酒店行业` |
| 触发词 | 前30行 | `触发词: 酒店/民宿/收益/ADR` |
| 版本 | 内容中 | `V1.0` / `v2.3` |

### 自动纳入流程

```bash
# 每周一10:00 Cron自动执行
python kb_autoreg.py

# 检查内容:
# 1. 扫描新KB文件
# 2. 解析元数据
# 3. 索引到KB
# 4. 更新路由表
```

### 命名规范

```
领域-具体内容-V版本.md
示例:
  hotel-industry-v7.md
  lottery-knowledge-base-v2.md
  aesthetic-knowledge-base-v3.1.md
```

---

## 七、进化机制 (V3.0新增)

```
数据驱动迭代循环:
  路由执行 → 记录反馈 → 准确率评估 → 优化路由
```

### 核心指标
| 指标 | 目标 | 当前 |
|------|------|------|
| 路由准确率 | >80% | 待积累数据 |
| 反馈收集 | 每日 | 手动/自动 |
| 规律固化 | 每周 | Cron触发 |

### 工具
- `evolve_kb.py` - 准确率评估 + 改进建议
- `kb_feedback.py` - 快速记录路由反馈
- `iterations/evolution_*.json` - 迭代报告

## 八、版本历史

- V1.0 (2026-03-31): 初始版本
- V2.0 (2026-04-02): 整合+归档冗余版本
- V3.0 (2026-04-06): **三层架构确立**，路由决策表，自动迭代机制，进化系统，自动纳入机制

---

**当前状态**: 
- ✅ 活跃KB文件数: **142个** (已归档旧版本6个至archive_versions)
- ✅ 总KB大小: **~3.4MB**
- ✅ 路由决策表: 28个类别（覆盖酒店10个子领域）
- ✅ 自动维护Cron: 已建立
- ✅ 旧版本清理: game-theory V1,V2 / startup-fundraising V1 / ai-llm V1 / lottery V1,V2 → archive_versions
- ✅ 版本号全部对齐: 酒店V8.1/理论V2.2/金融V2.0/博弈V3
- 🔄 路由准确率: 待积累数据
