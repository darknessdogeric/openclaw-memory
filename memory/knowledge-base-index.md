# B166ER 知识库索引 V3.0

> 创建日期: 2026-03-31
> 更新: 2026-04-14
> 版本: V3.0

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
| 审美 | `aesthetic-knowledge-base.md` | 审美/设计/品位/气韵/意境/排版/海报 |
| 博弈 | `game-theory-decision-knowledge-base-v3.md` | 博弈/谈判/策略/纳什均衡/投资人 |
| AI Agent/商业化 | `ai-agent-production-knowledge-base-v1.md` | AI/AGENT/多AGENT/RAG/TOKEN计费/生产环境 |
| 跨境结构 | `china-us-cross-border-structure-v1.md` | WFOE/VIE/ODI/美国公司/跨境资本/CFIUS |
| 决策框架 | `mental-models-decision-frameworks-v1.md` | 决策/逆向思维/概率/第二层思维/认知偏见 |
| 酒店 | `hotel-industry-knowledge-base-v7.md` | 酒店/民宿/收益/ADR/OCC/OTA/携程 |
| AI技术 | `ai-llm-knowledge-base-v2.md` | AI/LLM/AGENT/Prompt/RAG/大模型 |
| 创业融资 | `startup-fundraising-knowledge-base-v2.md` | 融资/股权/YC/路演/BP/VC |
| 大乐透 | `lottery-knowledge-base-v3.md` | 大乐透/彩票/预测/V5.0/量化/Gemini |
| 金融 | `finance-securities-knowledge-base.md` | 金融/证券/投资/股票/REITs |
| 跨境 | `跨境贸易知识库V1.0.md` | 跨境/选品/亚马逊/出海 |
| 收益管理 | `hotel-revenue-management-knowledge-base-v4.md` + `appendix-math.md` + `star-report-deep-dive.md` + `china-ota-strategy.md` + `implementation-v5.md` | 收益管理/动态定价/RevPAR/STR指数/OTA博弈/Python实现 |
| 私域会员 | `hotel-private-domain-membership-knowledge-base.md` | 私域/会员/RFM/复购 |
| 新媒体 | `hotel-new-media-marketing-knowledge-base-v2.md` | 新媒体/抖音/小红书/社群 |
| 智能化 | `hotel-ai-applications-knowledge-base.md` | 智能化/AI获客/PMS/数字化 |
| 目标管理 | `goal-management-knowledge-base.md` | OKR/目标/复盘 |
| AHL项目 | `ahl-*.md` (项目目录) | AHL/去中心化/AGENT |

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
| 审美与品位 | 260KB | V3.1 | ✅ 已内化 |
| 酒店行业全景 | 360KB | V7 | ✅ 核心 |
| 酒店行业中国深度（市场博弈+资产估值） | 6KB | V1 | ✅ 新增-博弈视角 |
| 酒店项目投资测算实战框架 | 6KB | V1 | ✅ 新增-决策工具 |
| 单体vs连锁决策框架 | 4KB | V1 | ✅ 新增-AHL核心问题 |
| 酒店资产管理全流程 | 5KB | V1 | ✅ 新增-投到退闭环 |
| 酒店投诉处理与客户恢复实战圣经 | 6KB | V1 | ✅ 新增-运营核心 |
| 酒店总经理每日工作手册 | 6KB | V1 | ✅ 新增-GM实战 |
| 酒店危机管理实战手册 | 5KB | V1 | ✅ 新增-SOP最缺 |
| AI/LLM技术 | 90KB | V2 | ✅ 完善 |
| 博弈论与决策 | 42KB | V3 | ✅ 已内化 |
| 创业融资 | 24KB | V2 | ✅ 完善 |
| 大乐透彩票 | 38KB | V2 | ✅ 完善 |
| 金融证券 | 53KB | V1 | ✅ 完善 |
| 酒店收益管理 | 16KB | V4 | ✅ 最新 |
| 酒店私域会员 | 25KB | V1 | ✅ 完善 |
| 酒店新媒体运营 | 29KB | V2 | ✅ 更新 |
| 酒店智能化 | 17KB | V1.1 | ✅ 完善 |
| 目标管理体系 | 30KB | V1 | ✅ 完善 |
| 跨境贸易 | 27KB | V1 | ✅ 完善 |
| AI Agent生产级应用 | 7KB | V1.0 | ✅ 新增-2026-04-14 |
| 中美跨境商业结构 | 5KB | V1.0 | ✅ 新增-2026-04-14 |
| 决策思维框架 | 5KB | V1.0 | ✅ 新增-2026-04-14 |

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
- ✅ KB文档数: **1359个** (今夜+1184)
- ✅ 扫描文件: 2402个
- ✅ 纳入率: ~57% (主要排除JSON/二进制)
- ✅ 路由决策表: 14个类别
- ✅ 自动维护Cron: 已建立
- ✅ 进化系统: 已建立
- ✅ **自动纳入机制**: 已确立（核心原则）
- 🔄 路由准确率: 待积累数据
