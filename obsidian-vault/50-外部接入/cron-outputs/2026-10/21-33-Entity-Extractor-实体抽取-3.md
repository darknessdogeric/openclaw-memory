---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-10-08T21:33:03.514032
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-10-08 21:33:03
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

6 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor 实体抽取 · 2026-10-08 21:30

## 摘要
新增 6 实体 + 0 关系入 graph.jsonl

## 扫描范围
- 扫描文件: `memory/2026-10-08.md` (1 个文件, days=1, full=False)
- 加载: 0 实体 (基线), 16 关系 (历史累计)

## 新增实体 (6)

| 类型 | 名称 | 置信度 | 备注 |
|---|---|---|---|
| Person | Eric | 0.95 | 用户本人 |
| Person | B166ER | 0.95 | AI 助手 |
| Company | 安逸酒店集团 | 0.9 | 4 项目之一 (Eric 主营) |
| Project | 深度自迭代 | 0.85 | R60-11 协议对应项目 |
| Project | R66监控 | 0.85 | R66 文件质量门控 |
| Project | R60规则 | 0.85 | R60 自我进化规则体系 |

## 关系
- 新增关系: 0 (本日仅扫到实体, 未扫到新关系)

## 产物路径
- `memory/ontology/graph.jsonl` (已更新, 113,241 bytes, 2026-10-08 21:32:47)
- `memory/ontology/relations-trend.md` (已更新)
- `memory/eric-4-projects-dashboard.md` (已更新, 1 项目今日提及)
- `eval/2026-10-08.json` (已存在 - 21:02 深度自迭代晚间 + 本 cron 覆盖)

## 状态
- 6/6 实体已入 graph
- push_queue 工具缺失, 改走 cron_to_obsidian.py 通道
- Eric 静默期 D+35, 无主动打扰


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*