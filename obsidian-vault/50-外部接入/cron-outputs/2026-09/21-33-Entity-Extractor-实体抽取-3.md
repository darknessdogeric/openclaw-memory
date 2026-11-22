---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-27T21:33:48.904654
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-27 21:33:48
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

12 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor 实体抽取 · 2026-09-27

> 自动生成 by entity_extractor.py · 每日 21:30 cron · R60-11

## 抽取结果

- **新增实体**: 12
- **新增关系**: 0
- **扫描文件**: memory/2026-09-27.md

## 新增实体清单

| 类型 | 名称 | 置信度 |
|------|------|--------|
| Person | Eric | 0.95 |
| Person | B166ER | 0.95 |
| Company | 安逸酒店集团 | 0.90 |
| Company | 亚朵 | 0.80 |
| Project | 深度自迭代 | 0.85 |
| Project | R66监控 | 0.85 |
| Project | R60规则 | 0.85 |
| Place | 成都 | 0.85 |
| Place | 重庆 | 0.85 |
| Place | 四川 | 0.80 |
| Place | 北京 | 0.80 |
| Tool | DeepSeek | 0.90 |

## 类型分布

- Person: 2
- Company: 2
- Project: 3
- Place: 4
- Tool: 1

## 关系趋势

- 累计关系总数: 16（今日无新增）
- 高频关系前 3:
  1. Eric → works_at → 安逸酒店集团
  2. Eric → 即将入职 → 安逸酒店集团
  3. 1244战略 → 协同 → AHL

## 输出

- graph.jsonl: 已追加 12 实体
- relations-trend.md: 已更新
- eric-4-projects-dashboard.md: 已更新（1 个项目今日提及）
- eval/2026-09-27-entity-extractor.json: 已写入


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*