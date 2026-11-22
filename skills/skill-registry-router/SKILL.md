---
name: skill-registry-router
description: 技能与工具路由：按任务类型检索既有技能/工具，命中即用不得自建；含自建前查重（--check）与固定工作流表。触发：动手前查有没有现成工具、选哪个技能、任务到技能的映射、避免重复造轮子。
---

# skill-registry-router

> **来源**：`toolbox/skill_router.py`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

技能与工具路由：按任务类型检索既有技能/工具，命中即用不得自建；含自建前查重（--check）与固定工作流表。触发：动手前查有没有现成工具、选哪个技能、任务到技能的映射、避免重复造轮子。

## 边界（不要越界）

- 本技能只负责"skill"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
