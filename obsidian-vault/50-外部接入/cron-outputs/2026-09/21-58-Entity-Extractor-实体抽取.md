---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-04T21:58:40.348473
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-04 21:58:40
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

5 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor 抽取结果 · 2026-09-04

**时间**: 2026-09-04 21:57 (Asia/Shanghai)
**Cron**: Entity Extractor 每日 21:30 (延迟 27 分钟)
**源文件**: memory/2026-09-04.md

## 新增实体 (5)

| ID | 类型 | 名称 | 置信度 |
|---|---|---|---|
| pers_0387 | Person | Eric | 0.95 |
| comp_0610 | Company | 安逸酒店集团 | 0.9 |
| comp_0213 | Company | AHL | 0.95 |
| proj_0213 | Project | AHL | 0.9 |
| plac_0221 | Place | 成都 | 0.85 |

## 新增关系 (0)

无新关系 — 今日 daily note 仅提及实体,未形成新的实体间关系链。

## 累计统计

- 总实体数: **1055**
- 总关系数: **16**
- 今日提及项目: **2** (安逸集团产业发展部 + AHL 试点)

## 沉淀动作 (R60-11)

- [x] 实体入 memory/ontology/graph.jsonl
- [x] 高频关系趋势 → memory/ontology/relations-trend.md
- [x] Eric 4 项目变化 → memory/eric-4-projects-dashboard.md
- [x] eval/2026-09-04-entity.json 写入
- [x] 推送到 Obsidian (本推送)


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*