---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-08-05T21:36:50.406226
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> [R66修订·2026-08-30·Eric指令] 已清理'本奥米尔/阿联酋/UAE/Benoemir/350亿授信/中国银行四川省分行'等已作废/虚构内容。修订原则：以实际信息为准。

> **推送时间**: 2026-08-05 21:36:50
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

20 实体 + 0 关系入 graph (2026-08-05 21:36)

## 📄 内容

# Entity Extractor · 2026-08-05 21:36

> **Cron**: Entity Extractor (每日21:30) · 触发延迟 6 分钟
> **扫描文件**: memory/2026-08-05.md (今日全量)
> **模型**: MiniMax-M3

---

## 抽取统计

| 维度 | 数值 |
|------|------|
| 新增实体 | 20 |
| 新增关系 | 0 |
| 累计实体 | (graph.jsonl) |
| 累计关系 | 15 |
| 抽取耗时 | <1s |

---

## 新实体（20 个）

### Person (2)
- `Person:Eric` — Eric / 张实
- `Person:B166ER` — AI 助理

### Company (7)
- `Company:安逸酒店集团` — AnYi Hotel Group
- `Company:AHL` — AI Hotel Layer 协议栈
- `Company:携程` — OTA 平台
- `Company:美团` — 本地生活/OTA
- `Company:高盛` — 投行
- `Company:OpenAI` — LLM 提供方

### Project (6)
- `Project:AHL` — 内部孵化
- `Project:1244战略` — 安逸集团战略命名
- `Project:医养酒店` — 轻资产研究
- `Project:深度自迭代` — R60-11 协议
- `Project:R66监控` — 质量门控
- `Project:R60规则` — 规则集

### Event (1)
- `Event:入职` — Eric 入职 AnYi

### Place (3)
- `Place:成都`
- `Place:重庆`
- `Place:四川`

### Tool (2)
- `Tool:Agent TARS`
- `Tool:scrape_matrix`

---

## 高频关系趋势（Top 15）

| 排名 | 关系 | 累计频次 |
|------|------|----------|
| 1 | Eric → works_at → 安逸酒店集团 | 1 |
| 2 | Eric → 即将入职 → 安逸酒店集团 | 1 |
| 3 | 1244战略 → 协同 → AHL | 1 |
| 4 | D-day → 触发事件 → 党委会 | 1 |
| 5 | 入职 → 时间 → 7月中上旬 | 1 |
| 6 | 党委会 → 预定日期 → 7月13或14 | 1 |
| 7 | 安逸酒店集团 → 拥有 → 167酒店 | 1 |
| 8 | AHL → 落地于 → 安逸酒店集团 | 1 | | 1 |
| 10 | 医养酒店 → 模式 → 轻资产 | 1 |
| 11 | AHL → 特性 → 去中心化 | 1 |
| 12 | B166ER → 运行 → cron任务 | 1 |
| 13 | AHL → 架构 → 双Agent | 1 |
| 14 | Eric → 即将担任 → 产业发展部部长 | 1 |
| 15 | Eric → 使用 → DeepSeek | 1 |

---

## Eric 4 项目仪表板更新

| 项目 | 状态 | 置信度 | 最近更新 |
|------|------|--------|----------|
| AHL | 今日提及 | 0.9 | 2026-08-05 |
| 1244战略 | 今日提及 | 0.85 | 2026-08-05 |
| 医养酒店 | 今日提及 | 0.8 | 2026-08-05 |
| 深度自迭代 | 今日提及 | 0.95 | 2026-08-05 |

---

## 沉淀动作执行

- [x] 实体入 `memory/ontology/graph.jsonl` ✅
- [x] 关系趋势入 `memory/ontology/relations-trend.md` ✅
- [x] 仪表板入 `memory/eric-4-projects-dashboard.md` ✅
- [x] eval/2026-08-05.json 追加 ✅
- [ ] 推送 Obsidian (执行中)

---

*2026-08-05 21:36 · B166ER Entity Extractor*

---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*