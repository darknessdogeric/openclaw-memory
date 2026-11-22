---
name: skill-registry-builder
description: 技能注册表生成器：以「祖先判据」重算真实技能数并生成 output/audit_skills/SKILL_REGISTRY.json（与 selfcheck C14 完全同一定义），含 description／可执行件／参考文档／三处位置／活跃状态。触发：技能库盘点、注册表重建、注册表漂移、某技能是否已登记、技能数量对不对、C14 失败、审计后同步索引。
---

# skill-registry-builder

> **来源**：2026-11-18 技能库审计（把注册表生成从一次性脚本沉淀为可复现技能）
> **脚本**：`scripts/build_skill_registry.py` → 输出 `output/audit_skills/SKILL_REGISTRY.json`

## 何时用

- 新建或删除技能后，同步注册表（否则 C14 会 FAIL）
- 盘点真实技能数量（不是文件数）
- 核对某个技能是否已登记、归属哪处位置

## 判据（与 C14 断言同一定义）

一个 `SKILL.md` 算独立技能，当且仅当：
1. 它的所有祖先目录都不含 `SKILL.md`（排除技能内部的 `examples/`、`variants/` 副本）
2. 它的路径里没有 `_` 开头的目录（`_archive` 是归档区，不算在库技能）

**★ 口径必须与 `toolbox/selfcheck.py` 的 C14 一致** —— 断言与被断言对象若定义不同，断言自己就会误报。

## 纪律

- 注册表是**程序生成**的：不手改 JSON，改逻辑改脚本后重跑
- 新增技能后必须重跑，否则索引漂移、路由指向不存在的技能
