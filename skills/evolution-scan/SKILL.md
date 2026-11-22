---
name: evolution-scan
description: 自进化扫描与缺席告警：周期性跑断言并写扫描记录（eval/），并由独立探测器按「缺席>8 天 / 连续 2 次未全绿」触发告警。触发：让自进化从靠记性变成制度保证、周期回归、缺席检测、eval 断链修复。
---

# evolution-scan

> **来源**：`toolbox/evolution_scan.py / toolbox/evolution_watch.py / toolbox/evolution_watch_trigger2.js / toolbox/evolution_scan_payload.js`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

自进化扫描与缺席告警：周期性跑断言并写扫描记录（eval/），并由独立探测器按「缺席>8 天 / 连续 2 次未全绿」触发告警。触发：让自进化从靠记性变成制度保证、周期回归、缺席检测、eval 断链修复。

## 边界（不要越界）

- 本技能只负责"evolution"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
