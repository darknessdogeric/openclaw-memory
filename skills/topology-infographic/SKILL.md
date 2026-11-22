---
name: topology-infographic
description: 信息拓扑图生成器：单一 SVG 源出 3:4 与 9:16 两版，自动三层质检（盒模型/SVG 元素级重叠·越界·压曲线·死白/视觉核验）。触发：把系统结构画成拓扑图、机制可视化、9:16 手机长图、认知拓扑、信息架构图。
---

# topology-infographic

> **来源**：`toolbox/make_topology.py`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

信息拓扑图生成器：单一 SVG 源出 3:4 与 9:16 两版，自动三层质检（盒模型/SVG 元素级重叠·越界·压曲线·死白/视觉核验）。触发：把系统结构画成拓扑图、机制可视化、9:16 手机长图、认知拓扑、信息架构图。

## 边界（不要越界）

- 本技能只负责"topology"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
