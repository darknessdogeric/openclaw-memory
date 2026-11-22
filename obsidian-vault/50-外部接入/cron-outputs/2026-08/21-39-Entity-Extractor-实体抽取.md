---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-08-03T21:39:15.039524
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-08-03 21:39:15
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

17 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor 抽取结果 · 2026-08-03

> 自动生成 from entity_extractor.py · 2026-08-03 21:30
> D+3 @ AnYi · R69 静默观察期第 3 天

## 抽取概览

| 指标 | 数值 |
|------|------|
| 新增实体 | 17 |
| 新增关系 | 0 |
| 项目今日提及 | 4 |
| 源文件 | memory/2026-08-03.md (43,506 bytes) |
| Cron ID | 0eced1e9-8729-47d8-b8d6-34eff13ed780 |

---

## 新增实体清单 (按类型)

### Person (2)
- `Eric` (置信度 0.95)
- `B166ER` (置信度 0.95)

### Company (5)
- `安逸酒店集团` (置信度 0.95)
- `AHL` (置信度 0.95)
- `携程` (置信度 0.80)
- `特斯拉` (置信度 0.80)

### Project (6)
- `AHL` (置信度 0.90)
- `1244战略` (置信度 0.90)
- `深度自迭代` (置信度 0.85)
- `B166ER深度自迭代` (置信度 0.85)
- `R66监控` (置信度 0.85)
- `R60规则` (置信度 0.85)

### Event (1)
- `D-day` (置信度 0.95) — 对应安逸集团入职关键节点

### Place (3)
- `成都` (置信度 0.85)
- `重庆` (置信度 0.85)
- `四川` (置信度 0.80)

### Tool (1)
- `DeepSeek` (置信度 0.90) — B166ER 主 LLM

---

## 4 项目状态

| 项目 | 状态 | 今日提及 |
|------|------|----------|
| AHL | 待入职后启动 | ✅ (Skift 三连发验证战略时机) |
| 1244战略 | 待入职后融合 | ✅ |
| 深度自迭代 | 持续运行 | ✅ (B166ER自我进化) |
| B166ER深度自迭代 | 子项目 | ✅ (R69 静默观察期第 3 天) |

---

## 关键洞察

1. **Eric + B166ER 核心实体首次双入图** — 体现"共在式自我实现"哲学底色 (V2.4)
2. **安逸酒店集团 + AHL** — 平台 + 项目双锚,Eric 当前战略主线
3. **D-day 入图** — 入职关键节点进入时间序列化跟踪
4. **0 新关系** — 关系模式词典相对今日内容覆盖率偏低,需扩充 (尤其是 Skift 三连发类的行业权力地图类关系)
5. **5 工具/平台覆盖** — DeepSeek + Booking + Obscura + Playwright + TrendRadar → AHL 技术栈已成型

---

## 输出文件

| 文件 | 状态 |
|------|------|
| `memory/ontology/graph.jsonl` | +17 entities |
| `memory/ontology/relations-trend.md` | regenerated (Top 20 高频关系) |
| `memory/eric-4-projects-dashboard.md` | updated (4 项目今日提及) |
| `eval/2026-08-03-2130.json` | 1,654 bytes |
| Obsidian vault | 待推送 (本文件) |

---

*Cron 任务执行完成 · B166ER 自动沉淀*

---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*