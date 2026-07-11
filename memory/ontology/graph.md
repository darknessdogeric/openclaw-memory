# 知识图谱 (Knowledge Graph)

> 自动生成 from graph.jsonl · 2026-06-24 21:33

**总计**: 33 实体 / 79 关系

## Company (5)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| comp_0002 | 安逸酒店集团 | - | 2026-06-17.md |
| comp_0011 | 智元机器人 | - | 2026-06-18.md |
| comp_0074 | AHL | - | 2026-06-22.md |
| comp_0080 | 四川旅游投 | - | 2026-06-22.md |
| comp_0105 | 高盛 | - | 2026-06-24.md |

## Event (9)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| even_0019 | 2026年端午节 | 端午D1, 端午假期 | 2026-06-19.md |
| even_0030 | 端午假期 | 端午D2 | 2026-06-20.md |
| even_0037 | 端午节 | 端午 | 2026-06-20.md |
| even_0043 | 伊朗关闭霍尔木兹海峡 | 霍尔木兹海峡关闭 | 2026-06-21.md |
| even_0062 | 深市 REITs 五周年 | - | 2026-06-22.md |
| even_0086 | 北京文旅项目征集 | - | 2026-06-22.md |
| even_0093 | 端午复盘 | - | 2026-06-23.md |
| even_0094 | 商业情报简报 | - | 2026-06-23.md |
| even_0107 | 全球AI/芯片股崩盘 | - | 2026-06-24.md |

## Person (1)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| pers_0001 | Eric | - | 2026-06-17.md |

## Place (1)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| plac_0012 | 重庆丽苑维景 | - | 2026-06-18.md |

## Project (7)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| proj_0003 | AHL | AHL v3 | 2026-06-17.md |
| proj_0005 | 医养酒店 | - | 2026-06-17.md |
| proj_0020 | AHL范式战略v1.0 | AHL v1.1 | 2026-06-19.md |
| proj_0027 | 深度自迭代 | M3 | 2026-06-20.md |
| proj_0042 | AHL协议栈v3.0 | AHL | 2026-06-21.md |
| proj_0061 | B166ER | B166ER 深度自迭代 | 2026-06-22.md |
| proj_0092 | R66 监控 | - | 2026-06-23.md |

## Tool (10)

| ID | 名称 | 别名 | 来源 |
|----|------|------|------|
| tool_0004 | OpenClaw | OpenClaw v2026.3.24 | 2026-06-17.md |
| tool_0013 | DeepSeek Pro | - | 2026-06-18.md |
| tool_0021 | B166ER | - | 2026-06-19.md |
| tool_0028 | 全球情报简报 | - | 2026-06-20.md |
| tool_0029 | 商业情报 | - | 2026-06-20.md |
| tool_0036 | M3 | - | 2026-06-20.md |
| tool_0044 | Firecrawl v4.23.0 | Firecrawl | 2026-06-21.md |
| tool_0050 | trendradar MCP | - | 2026-06-21.md |
| tool_0068 | rules.md | - | 2026-06-22.md |
| tool_0106 | TrendRadar | - | 2026-06-24.md |

## 关系 (Relations)

| 主体 | 关系 | 客体 | 置信度 | 来源文件 |
|------|------|------|--------|---------|
| pers_001 | works_at | comp_0002 | 0.95 | 2026-06-17.md |
| pers_001 | manages | proj_0005 | 0.9 | 2026-06-17.md |
| pers_001 | uses | tool_0004 | 0.95 | 2026-06-17.md |
| proj_001 | related_to | tool_0004 | 0.95 | 2026-06-17.md |
| comp_0002 | related_to | proj_0005 | 0.9 | 2026-06-17.md |
| pers_001 | works_at | comp_001 | 0.7 | 2026-06-18.md |
| pers_001 | uses | tool_001 | 0.95 | 2026-06-18.md |
| pers_001 | related_to | place_001 | 0.9 | 2026-06-18.md |
| pers_001 | related_to | comp_002 | 0.9 | 2026-06-18.md |
| place_001 | located_in | plac_0012 | 0.95 | 2026-06-18.md |
| pers_001 | manages | comp_001 | 0.7 | 2026-06-19.md |
| pers_001 | participated_in | event_001 | 0.9 | 2026-06-19.md |
| pers_001 | owns | proj_001 | 0.9 | 2026-06-19.md |
| pers_001 | uses | tool_001 | 0.95 | 2026-06-19.md |
| proj_001 | related_to | comp_001 | 0.5 | 2026-06-19.md |
| pers_001 | manages | proj_001 | 0.9 | 2026-06-20.md |
| pers_001 | uses | tool_001 | 0.9 | 2026-06-20.md |
| pers_001 | uses | tool_002 | 0.9 | 2026-06-20.md |
| pers_001 | participated_in | event_001 | 0.95 | 2026-06-20.md |
| proj_001 | related_to | tool_001 | 0.6 | 2026-06-20.md |
| pers_001 | manages | proj_001 | 0.9 | 2026-06-20.md |
| proj_001 | uses | tool_001 | 0.9 | 2026-06-20.md |
| pers_001 | participated_in | event_001 | 0.95 | 2026-06-20.md |
| tool_002 | related_to | pers_001 | 0.9 | 2026-06-20.md |
| pers_001 | works_at | comp_001 | 0.9 | 2026-06-21.md |
| pers_001 | manages | proj_001 | 0.85 | 2026-06-21.md |
| event_001 | related_to | proj_001 | 0.7 | 2026-06-21.md |
| proj_001 | uses | tool_001 | 0.9 | 2026-06-21.md |
| comp_001 | targets | proj_001 | 0.75 | 2026-06-21.md |
| pers_001 | works_at | comp_001 | 0.9 | 2026-06-21.md |
| proj_001 | related_to | comp_001 | 0.85 | 2026-06-21.md |
| event_001 | related_to | proj_001 | 0.8 | 2026-06-21.md |
| pers_001 | uses | tool_001 | 0.95 | 2026-06-21.md |
| proj_001 | related_to | event_001 | 0.8 | 2026-06-21.md |
| pers_001 | works_at | comp_001 | 0.9 | 2026-06-21.md |
| pers_001 | manages | proj_001 | 0.85 | 2026-06-21.md |
| proj_001 | related_to | event_001 | 0.7 | 2026-06-21.md |
| proj_001 | uses | tool_001 | 0.8 | 2026-06-21.md |
| comp_001 | targets | event_001 | 0.6 | 2026-06-21.md |
| pers_001 | owns | proj_001 | 0.95 | 2026-06-22.md |
| pers_001 | related_to | comp_001 | 0.9 | 2026-06-22.md |
| proj_001 | related_to | proj_002 | 0.85 | 2026-06-22.md |
| comp_001 | targets | event_001 | 0.8 | 2026-06-22.md |
| proj_002 | related_to | event_001 | 0.85 | 2026-06-22.md |
| pers_001 | manages | proj_001 | 0.95 | 2026-06-22.md |
| pers_001 | targets | comp_001 | 0.9 | 2026-06-22.md |
| proj_001 | uses | tool_001 | 0.95 | 2026-06-22.md |
| comp_001 | related_to | event_001 | 0.7 | 2026-06-22.md |
| pers_001 | participated_in | event_001 | 0.6 | 2026-06-22.md |
| pers_001 | manages | proj_001 | 0.9 | 2026-06-22.md |
| pers_001 | related_to | comp_001 | 0.85 | 2026-06-22.md |
| comp_001 | targets | event_001 | 0.7 | 2026-06-22.md |
| comp_002 | related_to | event_001 | 0.8 | 2026-06-22.md |
| comp_002 | related_to | comp_001 | 0.6 | 2026-06-22.md |
| pers_001 | related_to | comp_001 | 0.9 | 2026-06-22.md |
| pers_001 | owns | proj_001 | 0.95 | 2026-06-22.md |
| comp_001 | related_to | comp_002 | 0.85 | 2026-06-22.md |
| comp_001 | targets | event_001 | 0.7 | 2026-06-22.md |
| proj_001 | related_to | comp_001 | 0.8 | 2026-06-22.md |
| pers_001 | works_at | comp_001 | 0.7 | 2026-06-22.md |
| pers_001 | manages | proj_001 | 0.95 | 2026-06-22.md |
| comp_001 | related_to | event_001 | 0.7 | 2026-06-22.md |
| comp_001 | related_to | event_002 | 0.7 | 2026-06-22.md |
| event_001 | related_to | event_002 | 0.6 | 2026-06-22.md |
| pers_001 | owns | tool_001 | 0.95 | 2026-06-23.md |
| tool_001 | related_to | proj_001 | 0.9 | 2026-06-23.md |
| pers_001 | participated_in | event_001 | 0.7 | 2026-06-23.md |
| pers_001 | participated_in | event_002 | 0.7 | 2026-06-23.md |
| tool_001 | uses | proj_001 | 0.9 | 2026-06-23.md |
| pers_001 | uses | tool_001 | 0.95 | 2026-06-23.md |
| pers_001 | manages | proj_001 | 0.85 | 2026-06-23.md |
| pers_001 | participated_in | event_001 | 0.7 | 2026-06-23.md |
| pers_001 | participated_in | event_002 | 0.7 | 2026-06-23.md |
| tool_001 | related_to | proj_001 | 0.85 | 2026-06-23.md |
| pers_001 | manages | proj_001 | 0.9 | 2026-06-24.md |
| pers_001 | uses | tool_001 | 0.95 | 2026-06-24.md |
| comp_001 | related_to | event_001 | 0.85 | 2026-06-24.md |
| event_001 | related_to | proj_001 | 0.9 | 2026-06-24.md |
| pers_001 | targets | comp_001 | 0.7 | 2026-06-24.md |

---
*原始数据*: `ontology/graph.jsonl`