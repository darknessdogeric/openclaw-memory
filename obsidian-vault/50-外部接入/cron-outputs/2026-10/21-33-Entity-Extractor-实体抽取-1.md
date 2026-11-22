---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-10-02T21:33:54.985094
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-10-02 21:33:54
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

6 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor · 2026-10-02 21:30

> 自动生成 from entity_extractor.py · 2026-10-02 21:32
> Cron: Entity Extractor (每日21:30) · cron_id 0eced1e9-8729-47d8-b8d6-34eff13ed780

## 本次抽取概览

| 指标 | 数值 |
|---|---|
| 扫描模式 | today |
| 扫描文件 | `memory/2026-10-02.md` |
| 新增实体 | **6** |
| 新增关系 | **0** |
| 累计实体（graph.jsonl）| 86+ |
| 累计关系 | 16 |

## 新增实体（6 个）

| # | 类型 | 名称 | 置信度 | ID |
|---|---|---|---|---|
| 1 | Person | Eric | 0.95 | pers_0387 |
| 2 | Person | B166ER | 0.95 | pers_0374 |
| 3 | Company | 安逸酒店集团 | 0.95 | comp_0610 |
| 4 | Place | 四川 | 0.80 | plac_0264 |
| 5 | Place | 北京 | 0.80 | plac_0411 |
| 6 | Tool | Playwright | 0.80 | tool_0067 |

## 类型分布

| 类型 | 新增 |
|---|---|
| Person | 2 |
| Company | 1 |
| Place | 2 |
| Tool | 1 |
| Project | 0 |
| Event | 0 |

## 当日 memory 关键主题（来自 2026-10-02.md）

- **07:40-07:56**：Eric 诊断文件制作工具耗时长 → 系统解决工具可用性 → **安装 .NET SDK 8.0.425**
- **12:04-12:13**：修复 OCR 中文包 + 视觉模型（不增加费用）
- **12:35**：深度梳理安逸工作内容 + 笔记/录音 vs KB 交叉比对
  - 桌面转录件 33 份 / KB 597 份
  - **GAP 缺口 15 份**（待吸收）
  - 产出 `anyi-ops-kb/00_安逸集团知识库总览/安逸工作内容全景结构化索引_v1.0_2026-10-02.md`

## R60-11 沉淀动作清单

| # | 动作 | 产物 | 状态 |
|---|---|---|---|
| 1 | 实体入 graph.jsonl | `memory/ontology/graph.jsonl` | ✅ |
| 2 | 高频关系趋势 | `memory/ontology/relations-trend.md` | ✅ |
| 3 | Eric 4 项目仪表板 | `memory/eric-4-projects-dashboard.md` | ✅ |
| 4 | eval 写入 | `eval/2026-10-02-entity-extractor.json` | ✅ |
| 5 | Obsidian 推送 | `obsidian-vault/50-外部接入/cron-outputs/2026-10/` | ✅ |

## Notes

- 0 新增关系：今日 memory 内容以工作诊断/工具修复为主，未触发关系模式
- Eric 提及「安逸集团」「B166ER」高频 → 这两个实体为持续高频实体
- 「四川」「北京」地名出现在 12:35 的 KB 索引（安逸集团地理分布）
- 「Playwright」出现在 07:40-07:51 工具修复诊断章节
- push_queue 工具不存在 → 降级到 cron_to_obsidian.py 通道 ✅


---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*