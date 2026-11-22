---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-09-07T22:03:59.932913
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-09-07 22:03:59
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

20 实体 + 0 关系入 graph (晚间 run)

## 📄 内容

# Entity Extractor · 2026-09-07 22:02

## 运行参数
- 命令: `python toolbox/entity_extractor.py today`
- 扫描文件: `2026-09-07.md`
- 增量模式: full=False, days=1
- 触发: cron 每日 21:30 (本次实际 22:02)

## 新增实体 (20)

### Person (2)
| ID | Name | 备注 |
|----|------|------|
| Person:Eric | Eric (张实) | 用户本人 |
| Person:B166ER | B166ER | AI 助理 |

### Company (6)
| ID | Name | 备注 |
|----|------|------|
| Company:安逸酒店集团 | 安逸酒店集团有限责任公司 | 国企 |
| Company:四川旅游投 | 四川省旅游投资集团 | 上级母公司 |
| Company:AHL | AHL 去中心化酒店平台 | Eric 孵化项目 |
| Company:亚朵 | 亚朵 | 行业对标 |
| Company:高盛 | 高盛 | 国际投行 |
| Company:OpenAI | OpenAI | AI 行业 |

### Project (3)
| ID | Name | 备注 |
|----|------|------|
| Project:AHL | AHL 去中心化平台 | 核心孵化 |
| Project:医养酒店 | 医养酒店轻资产 | 个人研究 |
| Project:R66监控 | R66 质量门控 | B166ER 内部规则 |
| Project:R60规则 | R60 规则集 | B166ER 内部规则 |

### Event (2)
| ID | Name | 备注 |
|----|------|------|
| Event:党委会 | 集团上党委会 | 入职流程 |
| Event:霍尔木兹海峡事件 | 霍尔木兹海峡事件 | 地缘政治 |

### Place (3)
| ID | Name | 备注 |
|----|------|------|
| Place:成都 | 成都 | 集团总部 |
| Place:四川 | 四川 | 集团驻地 |
| Place:北京 | 北京 | 政治中心 |

### Tool (3)
| ID | Name | 备注 |
|----|------|------|
| Tool:OpenClaw | OpenClaw | 运行底座 |
| Tool:DeepSeek | DeepSeek | Eric 使用 |
| Tool:TrendRadar | TrendRadar | 信息流监控 |

## 关系趋势 (累计 16 条)

详见 `memory/ontology/relations-trend.md`

**Top 关系**:
- Eric works_at 安逸酒店集团
- 1244战略 协同 AHL
- AHL 落地于 安逸酒店集团
- 安逸酒店集团 拥有 167酒店
- Eric 即将担任 产业发展部部长

## Eric 4 项目状态

| 项目 | 状态 | 置信度 |
|------|------|--------|
| AHL | 今日提及 | 0.9 |
| 1244战略 | 待入职后融合 | 0.85 |
| 医养酒店 | 今日提及 | 0.8 |
| 深度自迭代 | 持续运行 | 0.95 |

## 沉淀动作清单 (R60-11)

- [x] 实体入 memory/ontology/graph.jsonl
- [x] 关系趋势 → memory/ontology/relations-trend.md
- [x] Eric 4 项目 → memory/eric-4-projects-dashboard.md
- [ ] eval/2026-09-07.json (追加晚间条目)
- [ ] Obsidian 推送 (本文件即推送内容)

## 异常标记

- 0 关系新增 (今日 daily note 中纯描述多, 实体引用少 → 关系密度低)
- Eric 实际状态: 9/7 应为"已入职"或"正在入职" → 但 daily note 中仍以"即将入职"描述 → 存在时序不一致

---
_生成: 2026-09-07 22:02 GMT+8 · entity_extractor.py v1_


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*