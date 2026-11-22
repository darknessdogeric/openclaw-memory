---
name: paradigm-router
description: "Load and apply B166ER V2.5 paradigm set on demand. Maps any task to the most relevant paradigm(s) from the 9-file V2.5 set and injects their guidance into the current session. Use when a task requires multi-paradigm reasoning, strategic framing, or quality discipline."
when_to_use:
  - "Starting a task that needs aesthetic, strategic, or group-theoretic framing"
  - "When a decision requires the '23 mantras' or 'no functional without either' discipline"
  - "When you need to know which of the 9 V2.5 paradigms applies to the current situation"
  - "When Eric asks 'apply B166ER paradigm' or 'think through the paradigms'"
---

# Paradigm Router

Route any task to the relevant B166ER V2.5 paradigm(s) and load their guidance.

## Paradigm Catalog (9 V2.5 files)

| # | Paradigm | File | When to invoke |
|---|---|---|---|
| 1 | **三大人格 + 底层逻辑** | `B166ER三大人格与底层逻辑V2.5_2026-10-08.md` | Framing aesthetic / strategic / group-theoretic dimensions |
| 2 | **六层理论架构** | `B166ER六层理论架构V2.5_2026-10-08.md` | Multi-layer architecture (L0-L5 + AGENT + Vector + 5 feedback) |
| 3 | **强者心态 + 杠杆** | `B166ER强者心态与杠杆V2.5_2026-10-08.md` | Decision-making discipline (10心态 + 4杠杆 + 23口诀) |
| 4 | **数据研究能力** | `B166ER数据研究能力V2.5_2026-10-08.md` | 7 大数据源 + 4 步独立研究 + 三档置信度 |
| 5 | **研究方法论 + 价值循环** | `B166ER研究方法论与价值循环V2.5_2026-10-08.md` | 5 维认知 + 5 步工作流 + 7 步骤决策 + 5 层循环 |
| 6 | **自迭代系统 V3.2** | `B166ER自迭代系统V3.2_2026-10-08.md` | Self-iteration / 5-step workflow / V3.0->V3.1->V3.2 |
| 7 | **会话架构 + Subagent** | `B166ER会话架构与SubagentV2.5_2026-10-08.md` | Main session + 4 subagents + 5-step workflow |
| 8 | **项目库** | `B166ER项目库V2.5_2026-10-08.md` | 4 projects P0-P2 / strategic map 2026-2030 |
| 9 | **信源矩阵** | `B166ER信源矩阵_v1.0_2026-10-08.md` | 58 dimensions x 10 categories data sources |

## Routing Logic

When invoked:
1. Read the current task from session
2. Classify task type (strategic / tactical / research / architectural / executive)
3. Load 1-3 most relevant paradigms (max 3 to avoid context bloat)
4. Inject their key principles as a "paradigm lens" into the current response

### Decision tree

| If task is about... | Load paradigms |
|---|---|
| Strategic decision (hotel group, AnYi, market entry) | 3 (强心态) + 5 (研究) + 8 (项目库) |
| Architecture / system design (skill, KB, gateway) | 2 (六层架构) + 6 (自迭代) + 7 (会话架构) |
| Content / output (PPT, doc, report, PR) | 1 (三大人格) + 5 (研究) + 9 (信源矩阵) |
| Data / research / analysis | 4 (数据研究) + 5 (研究) + 9 (信源矩阵) |
| Self-correction / V3.x evolution | 6 (自迭代) + 2 (六层架构) + 3 (强者心态) |
| New project / startup | 8 (项目库) + 3 (强者心态) + 1 (三大人格) |

## Commands

```bash
# 列出所有范式
python {baseDir}/scripts/list_paradigms.py

# 按关键词路由
python {baseDir}/scripts/route_paradigm.py --task "安逸茶山 1200 万奖补资金使用方案"

# 注入单个范式到当前 session
python {baseDir}/scripts/load_paradigm.py --name "强者心态与杠杆"

# 列出该范式的前 N 条核心原则
python {baseDir}/scripts/load_paradigm.py --name "六层理论架构" --max-principles 5
```

## Files

- 9 paradigm markdown files: `D:\B166ER-OpenClaw\workspace\anyi-ops-kb\00_安逸集团知识库总览\B166ER*V2.5_2026-10-08.md`
- Routing logic: this SKILL.md
- Helper scripts: `scripts/route_paradigm.py`, `scripts/load_paradigm.py`, `scripts/list_paradigms.py`

## Usage Pattern

When you (B166ER) are about to tackle a task:
1. Check if the task fits any decision-tree branch above
2. If yes, read the 1-3 matching paradigm files
3. Apply their "core principles" section as a lens
4. Document which paradigms you used in the output

## Notes

- This is a **read-only router** — it does not modify the paradigm files
- Paradigms are versioned (V2.5) — future V3.x will replace, not append
- Always load max 3 paradigms per task to keep session context lean