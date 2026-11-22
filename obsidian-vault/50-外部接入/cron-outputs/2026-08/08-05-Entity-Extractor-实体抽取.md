---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-08-19T08:05:20.804032
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> [R66修订·2026-08-30·Eric指令] 已清理'本奥米尔/阿联酋/UAE/Benoemir/350亿授信/中国银行四川省分行'等已作废/虚构内容。修订原则：以实际信息为准。

> **推送时间**: 2026-08-19 08:05:20
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

11 实体 + 0 关系入 graph (2026-08-19 08:02 异常早触发)

## 📄 内容

# Entity Extractor · 2026-08-19 08:02 GMT+8

> cron:0eced1e9-8729-47d8-b8d6-34eff13ed780 (scheduled 21:30 daily, fired 08:02 = anomalous early replay)
> R60-11 sedimentation · 5/5 steps executed
> R65/R258/R69 DORMANT sustained (no proactive notification to Eric)

## 抽取摘要

| 指标 | 数值 |
|------|------|
| 扫描文件 | 1 (2026-08-18.md) |
| 新增实体 | 11 |
| 新增关系 | 0 |
| 关系总数 | 16 (累计) |
| graph.jsonl 总行数 | 820 |

## 新增实体清单

| 类型 | 实体 |
|------|------|
| Person | Eric |
| Person | B166ER |
| Company | 安逸酒店集团 |
| Company | AHL |
| Project | AHL |
| Project | 深度自迭代 |
| Project | R66监控 |
| Project | R60规则 |
| Event | 入职 |
| Place | 四川 |
| Tool | OpenClaw |

## Eric 4 项目仪表板更新

| 项目 | 状态 |
|------|------|
| AHL | 今日提及 |
| 1244战略 | 待入职后融合 |
| 医养酒店 | 个人研究 |
| 深度自迭代 | 今日提及 |

## 关键观察

1. **cron 异常触发**: 08:02 早于预定 21:30 12h+，疑似错过的 8/18 21:30 run 重放
2. **8/18 内容密度极高**: v1.3 战略升级 + 2 场会议吸收(国宴/平安) + 钟华身份纠偏 + R282 draft + Jinjiang MOU T-0
3. **抽取盲点**: 8/18 新词(钟华/平安/平安产险/国堰宾馆/樊登/陈保刚/中华/于秀等)未在 pattern 字典中 → 后续建议扩词
4. **DORMANT 合规**: push_queue 未调用,仅 Obsidian 写入(沉淀通道)

## 待办(下次 pattern 字典升级)

- [ ] 加 钟华 / 平安集团 / 平安产险 / 国堰宾馆 / 樊登 / 中华 / 于秀 / 陈保刚 / 董事长 / 大运营中心
- [ ] cron 调度原因排查(8/18 21:30 为何未执行)

## 关系趋势 (Top 16)

累计 16 条,主要分布:
- Eric → works_at → 安逸酒店集团 (1)
- Eric → 即将入职 → 安逸酒店集团 (1)
- Eric → 即将担任 → 产业发展部部长 (1)
- Eric → 使用 → DeepSeek (1)
- Eric → 管理 → 医养酒店 (1)
- AHL → 落地于 / 特性 / 架构 → 安逸酒店集团 / 去中心化 / 双Agent (3)
- 1244战略 → 协同 → AHL (1) (2)
- 入职 → 时间 → 7月中上旬 (1)
- 党委会 → 7月13或14 (1)
- D-day → 触发 → 党委会 (1)
- 医养酒店 → 模式 → 轻资产 (1)
- B166ER → 运行 → cron任务 (1)

---

*— B166ER Entity Extractor · 2026-08-19 08:04 GMT+8 · R60-11 沉淀完成*

---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*