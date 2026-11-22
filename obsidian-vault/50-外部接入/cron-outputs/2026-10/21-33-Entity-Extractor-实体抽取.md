---
author: b166er
audience: eric
task: Entity Extractor 实体抽取
importance: normal
pushed_at: 2026-10-01T21:33:09.122590
source: cron
status: active
tags: [cron-push]
---

# 🟡 Entity Extractor 实体抽取

> **推送时间**: 2026-10-01 21:33:09
> **来源**: Cron 任务自动推送
> **重要度**: normal

## 📋 摘要

3 实体 + 0 关系入 graph

## 📄 内容

# Entity Extractor 结果 · 2026-10-01

> 来源：cron 任务「Entity Extractor (每日21:30)」· 时间：2026-10-01 21:30 (Asia/Shanghai)

## 抽取概览

| 指标 | 值 |
|------|-----|
| 扫描文件 | `memory/2026-10-01.md` |
| 新增实体 | 3 |
| 新增关系 | 0 |
| Graph 累计实体 | 17 |
| Graph 累计关系 | 16 |

## 新增实体

| 类型 | ID | 名称 | 置信度 |
|------|------|------|--------|
| Person | `pers_0387` | Eric | 0.95 |
| Person | `pers_0374` | B166ER | 0.95 |
| Tool | `tool_0793` | OpenClaw | 0.95 |

## 内容来源摘要（memory/2026-10-01.md）

今日 memory 记录的是 B166ER 关于 `exec` / `process` 工具白名单问题的诊断：
- Eric 选了 A 方案（加 `exec` 到 main agent 工具白名单）
- `sessions_spawn` 当前可用，`exec` / `process` / `bash` 不在当前会话工具白名单
- 根因：全局 `openclaw.json` 第 386 行 `"exec": {"strictInlineEval": false, "mode": "full"}` 已生效，但 per-session 工具清单未注入
- 给出了 Eric 修改 `openclaw.json` 的最小 diff + 重启 `OpenClaw Gateway` 服务的步骤
- Eric 验证流程 30 秒：schtasks /End → /Run → 新开 webchat 检查工具列表 → 跑 smoke test

## 沉淀动作清单

- [x] 实体入 `memory/ontology/graph.jsonl`
- [x] 关系趋势更新 `memory/ontology/relations-trend.md`
- [x] Eric 4 项目仪表板 `memory/eric-4-projects-dashboard.md`
- [x] eval 评估 `memory/eval/2026-10-01.json`
- [x] 推送到 Obsidian（`cron_to_obsidian.py` → `50-外部接入/cron-outputs/2026-10/`）

## 备注

今日抽取的关系数为 0（仅 3 个实体命中），原因是当天的 memory 内容主要是技术诊断（工具白名单修改指南），未涉及实体之间的关系模式（Eric 用例、招聘、D-day 等）。这是正常情况——抽取器正常工作，只是当日文本不含关系触发模式。

---

*由 `entity_extractor.py today` 自动生成 · 2026-10-01 21:30*

---

## 🔗 相关

- [[../../../../20-我们共同维护的/00-Dashboard]]
- [[../../../../20-我们共同维护的/00-今日重点]]

*由 `cron_to_obsidian.py` 自动推送*