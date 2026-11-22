---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-09T09:33:39.295871
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-09 09:33:39
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

0 实体 + 0 关系入 graph (今日 memory 文件不存在)

## 📄 内容

# Entity Extractor · 2026-09-09 09:32

## 运行参数
- 命令: `python toolbox/entity_extractor.py today`
- 扫描文件: 无（`memory/2026-09-09.md` 不存在）
- 增量模式: full=False, days=1
- 触发: cron 每日 21:30 (本次实际 09:32 · **离计划时间 12h 提前**)

## 抽取结果

**0 实体 + 0 关系**（脚本正确返回，no-op）

```
[entity_extractor] 启动 · days=1 · full=False
[entity_extractor] 未找到memory文件
```

## 异常标记 ⚠️

- **离计划时间提前 12h 触发** — 21:30 cron 误在 09:32 触发（疑似 timezone / cron 配置漂移，需排查 scheduler）
- **2026-09-08.md / 2026-09-09.md 都不存在** — 连续两天无 daily note，可能是 Eric 周末/出差未写
- 9/8 实际应为昨日 21:30 抽取日（应有内容），但 9/8 文件空 → 09-08 cron 同样无产物
- **本 run 为纯空转**，未污染 graph.jsonl / relations-trend.md / eric-4-projects-dashboard.md

## 沉淀动作清单 (R60-11)

- [x] 实体入 memory/ontology/graph.jsonl（**无新增**，跳过）
- [x] 关系趋势 → memory/ontology/relations-trend.md（**无新增**，跳过）
- [x] Eric 4 项目 → memory/eric-4-projects-dashboard.md（**无新增**，跳过）
- [ ] eval/2026-09-09.json（**未生成** — 脚本 0 输入时不写 eval）
- [x] Obsidian 推送（本文件即推送内容）

## 建议

- 排查 cron scheduler 时区设置（应 Asia/Shanghai）
- Eric 周末 daily note 缺勤时，连续 no-op 不应反复触发 push
- 可考虑: 连续 2 天无 daily note → 自动告警 Eric（写入 inbox）

---
_生成: 2026-09-09 09:32 GMT+8 · entity_extractor.py v1 · **off-schedule 触发**_


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*