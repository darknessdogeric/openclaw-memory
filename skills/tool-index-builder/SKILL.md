---
name: tool-index-builder
description: 工具索引生成器：扫描 toolbox 全部非临时脚本，按内容级证据（docstring 质量／引用领域词／一次性动词前缀／日期后缀）分类为 capability／oneoff_family／orphan，并标注每个工具的归属技能 owner_skill 与同族 family，使"工具归属哪个技能"成为可校验事实。触发：工具层审计、toolbox 治理、工具注册、哪些工具没被用、工具该归到哪个技能、重复造轮子的工具层证据。
---

# tool-index-builder

> **来源**：2026-11-18 技能库审计后续（工具层治理第一段）
> **脚本**：`scripts/build_tool_index.py` → 输出 `output/audit_skills/TOOL_INDEX.json`

## 何时用

- 审计 toolbox 有多少工具、哪些是真能力工具、哪些是一次性脚本
- 判定某个工具该归到哪个技能（owner_skill）
- 给出"重复造轮子"的工具层证据（同族 N 件）

## 纪律

- **不靠名字猜**：分类依据来自文件内容（docstring／引用领域词／动词前缀／日期后缀），名称只作家族聚合用
- **索引是程序生成**：不手改 `TOOL_INDEX.json`，改逻辑改脚本后重跑
- **孤儿工具（orphan）不自动删**：先人工裁决，避免批量误伤
