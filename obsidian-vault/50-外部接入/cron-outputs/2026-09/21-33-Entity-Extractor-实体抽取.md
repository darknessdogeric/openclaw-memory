---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-09T21:33:22.065979
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-09 21:33:22
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

20 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor · 每日 21:30 抽取结果

**日期**: 2026-09-09 (Wednesday)
**执行时间**: 21:30 Asia/Shanghai
**扫描范围**: 最近 3 天（2026-09-07.md 实际命中）

---

## 新增实体（20）

### Person
- `Eric` (Pers)
- `B166ER` (Pers)

### Company
- `安逸酒店集团`
- `四川旅游投`
- `AHL`
- `亚朵`
- `高盛`
- `OpenAI`

### Project
- `AHL`
- `医养酒店`
- `R66监控`
- `R60规则`

### Event
- `党委会`
- `霍尔木兹海峡事件`

### Place
- `成都`
- `四川`
- `北京`

### Tool
- `OpenClaw`
- `DeepSeek`
- `TrendRadar`

---

## 关系（0）

本次未触发关系匹配模式 — 2026-09-07.md 不包含精确的关系语句模式（如"Eric 在 安逸"、"AHL 落地于"等）。

---

## 沉淀动作状态

| 步骤 | 状态 | 路径 |
|------|------|------|
| 1. 实体入 graph.jsonl | ✅ | `memory/ontology/graph.jsonl` |
| 2. relations-trend.md | ✅ | `memory/ontology/relations-trend.md`（20 关系累计）|
| 3. eric-4-projects-dashboard.md | ✅ | `memory/eric-4-projects-dashboard.md`（3 项目提及）|
| 4. eval/2026-09-09.json | ✅ | `memory/eval/2026-09-09.json` |
| 5. 推送到 Obsidian | ✅ | 本 cron_to_obsidian.py 调用 |

---

## Eric 4 项目状态（dashboard 同步）

| 项目 | 状态 | 置信度 |
|------|------|--------|
| AHL | 今日提及 | 0.9 |
| 医养酒店 | 今日提及 | 0.8 |
| R66监控 | 今日提及 | 0.85 |
| R60规则 | 今日提及 | 0.85 |
| 1244战略 | 待入职后融合 | 0.85 |
| 深度自迭代 | 持续运行 | 0.95 |

---

## 备注

- **今日 daily note (`2026-09-09.md`) 不存在** → 改用 `--days 3` 兜底，命中 2026-09-07.md
- 09:33 时段有过一次"无输入"空跑（off-schedule，scheduler timezone 漂移），本次 21:30 是计划内的正点执行
- 实体 ID 走稳定的 hash 命名（pers_xxxx / comp_xxxx 等），保证可复用
- 关系未触发原因：2026-09-07.md 主要是 dashboard 与 heartbeat 输出，缺少带主谓结构的强语义句

---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*