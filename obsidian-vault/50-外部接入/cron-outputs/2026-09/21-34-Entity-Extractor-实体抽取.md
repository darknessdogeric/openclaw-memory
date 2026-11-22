---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-23T21:34:24.205286
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-23 21:34:24
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

0 实体 + 0 关系入 graph（今日 memory 文件未生成）

## 📄 内容

# Entity Extractor · 2026-09-23 21:30

**Cron**: `cron:0eced1e9-8729-47d8-b8d6-34eff13ed780 Entity Extractor (每日21:30)`
**执行时间**: 2026-09-23 21:30 GMT+8
**模式**: today (days=1)
**结果**: 无新实体（今日 memory 文件不存在）

## 抽取状态

```
[entity_extractor] 启动 · days=1 · full=False
[entity_extractor] 未找到memory文件
```

## 原因分析

`memory/2026-09-23.md` 今日尚未生成（Eric 今日尚无主线程长对话写入 daily note）。

按 R60-11 范式：
- 实体入 `memory/ontology/graph.jsonl` → 跳过（无新源）
- 高频关系趋势 → `memory/ontology/relations-trend.md` → 跳过
- Eric 4 项目变化 → `memory/eric-4-projects-dashboard.md` → 跳过（昨日 2026-09-22 21:30 已更新）
- eval/2026-09-23.json → 本次写入
- Obsidian 推送 → 本次推送（status-only）

## 上次成功抽取

- 时间：2026-09-22 21:30
- 文件：memory/2026-09-22.md（13,411 bytes）
- graph.jsonl 末条：`{"type":"Place","date":"2026-09-22","id":"plac_0264","name":"???","confidence":0.8,"aliases":[]}`

## 下次触发

2026-09-24 21:30 GMT+8（同 cron）


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*