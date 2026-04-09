---
name: B166ER Knowledge & Skill Router
slug: kb-router
version: 1.0
created: 2026-04-06
description: 语义路由 + 知识库调度 + Skill联动核心
trigger: 所有任务/问题/分析
---

# B166ER 知识与调度系统 V1.0

## 架构

```
用户输入 → 语义识别 → 路由决策 → Skill/KB调用 → 结果整合 → 自反思
```

## 路由决策表

| 语义类型 | 路由目标 | Skill/KB |
|---------|---------|----------|
| 审美/设计/排版 | 审美知识库 + image-gen | `aesthetic-knowledge-base` |
| 博弈分析/谈判/决策 | 博弈论框架 | `game-theory-decision-knowledge-base` |
| 酒店运营/收益/管理 | 酒店知识库体系 | `hotel-industry-knowledge-base` |
| 融资/股权/YC/Walkrounds | 创业融资知识库 | `startup-fundraising-knowledge-base` |
| 大乐透/彩票/预测 | 大乐透知识库 | `lottery-knowledge-base` |
| 图片生成/海报/信息图 | HTML+Playwright | `lh-html-to-image` |
| 代码/技术架构/AGENT | AI/LLM知识库 | `ai-llm-knowledge-base` |
| 跨境/选品/亚马逊 | 跨境贸易知识库 | `cross-border-trade` |
| 合同/合规/架构 | 知识图谱 | `ontology` |
| 执行/提醒/自动化 | 主动执行 | `proactive-agent` |
| 学习/反思/纠错 | 自反思系统 | `self-improving` |
| 行业研究/报告 | 数据采集系统 | `data-acquisition` |
| **未知/复杂/跨领域** | **多Skill协作** | `agent-council` |

## 知识库索引

### 核心层 (始终可用)
- SOUL.md / MEMORY.md / IDENTITY.md

### 专业层 (按需加载)
| 知识库 | 文件 | 触发词 |
|--------|------|--------|
| 审美与品位 | `aesthetic-knowledge-base.md` | 审美/设计/品位/气韵 |
| 博弈论决策 | `game-theory-decision-knowledge-base-v3.md` | 博弈/谈判/策略/博弈论 |
| 酒店行业 | `hotel-industry-knowledge-base-v7.md` | 酒店/民宿/收益/ADR/OCC |
| AI/LLM技术 | `ai-llm-knowledge-base-v2.md` | AI/LLM/AGENT/Prompt/RAG |
| 创业融资 | `startup-fundraising-knowledge-base-v2.md` | 融资/股权/YC/路演/BP |
| 大乐透 | `lottery-knowledge-base-v2.md` | 大乐透/彩票/预测 |
| 金融证券 | `finance-securities-knowledge-base.md` | 金融/证券/投资 |
| 跨境贸易 | `跨境贸易知识库V1.0.md` | 跨境/选品/亚马逊 |
| 酒店收益 | `hotel-revenue-management-knowledge-base-v4.md` | 收益管理/定价/OCC |
| 酒店私域 | `hotel-private-domain-membership-knowledge-base.md` | 私域/会员/RFM |
| 酒店新媒体 | `hotel-new-media-marketing-knowledge-base-v2.md` | 新媒体/抖音/小红书 |
| 酒店智能化 | `hotel-ai-applications-knowledge-base.md` | 智能化/AI获客/PMS |
| 目标管理 | `goal-management-knowledge-base.md` | OKR/目标/复盘 |
| AHL项目 | `ahl-*.md` (项目目录) | AHL/去中心化/AGENT |

## 自迭代机制

```
每次任务完成 → 自反思(skills/self-improving)
    ↓
发现规律 → 更新 self-improving/corrections.md
    ↓
3次重复 → 提升为规则 → 更新 MEMORY.md
    ↓
跨领域规律 → 更新知识库索引
```

## 调用标准

### 开始任务前
1. 语义识别类型
2. 确定路由目标
3. 加载必要KB

### 任务完成后
1. 调用 self-improving 自反思
2. 评估是否需要更新KB
3. 检查是否有规律需要固化

### 定期维护 (每周)
1. KB质量检查
2. 过期内容归档
3. 新增内容索引
4. Skill效能评估

## 知识库存储

- SQLite: `~/.openclaw/knowledge.db` (TF-IDF语义检索)
- 文件索引: `memory/knowledge-base-index.md`
- 备份: Git自动同步

## 进化机制 (V2.0)

### 数据驱动迭代
```
路由反馈 → routing_feedback表 → 准确率评估 → 改进建议 → 路由优化
```

### 迭代系统
- **准确率追踪**: `evolve_kb.py` - 评估7天路由准确率
- **规律发现**: 自动发现corrections趋势，固化规律
- **改进建议**: 基于数据生成优化建议

### 反馈记录CLI
```bash
python kb_feedback.py "用户问题" "路由到的KB" "实际应该用" 1或0
# 示例
python kb_feedback.py "酒店收益" "hotel-industry" "hotel-revenue" 0
```

### 迭代报告
- 位置: `self-improving/iterations/evolution_*.json`
- 每周维护自动生成
- 包含: 准确率/建议/规律

## 状态

- ✅ V1.0 核心架构建立 (2026-04-06)
- ✅ V2.0 进化机制建立 (2026-04-06)
- ✅ 路由决策表完成 (14个类别)
- ✅ 自迭代机制定义
- ✅ 每周维护Cron已建立
- 🔄 持续迭代优化中
