---
name: self-check-assertions
description: 把每条教训写成可 PASS/FAIL 的断言并自动执行：编码完整性、HOT 层上限与时效、索引一致性、分层非空、正本唯一、不重复造轮子、技能可路由、日志不膨胀、日记被读回、纠错已下沉、PREFLIGHT 存在、信息图三层质检。触发：交付前自检、回归断言、失败即拦、selfcheck、每条教训如何变成机器可执行的规则。
---

# self-check-assertions

> **来源**：`toolbox/selfcheck.py`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

把每条教训写成可 PASS/FAIL 的断言并自动执行：编码完整性、HOT 层上限与时效、索引一致性、分层非空、正本唯一、不重复造轮子、技能可路由、日志不膨胀、日记被读回、纠错已下沉、PREFLIGHT 存在、信息图三层质检。触发：交付前自检、回归断言、失败即拦、selfcheck、每条教训如何变成机器可执行的规则。

## 边界（不要越界）

- 本技能只负责"self"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
