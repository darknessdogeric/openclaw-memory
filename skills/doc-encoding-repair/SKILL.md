---
name: doc-encoding-repair
description: 混合编码与文件完整性修复：结构化切分识别 UTF-8/GB18030 混合块，逐字符安全解码，保留字节原件，不可逆者标注留痕。触发：文件读不出来、U+FFFD 乱码、PowerShell 追加破坏 UTF-8、编码损坏批量修复。
---

# doc-encoding-repair

> **来源**：`toolbox/fix_mixed_encoding.py`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

混合编码与文件完整性修复：结构化切分识别 UTF-8/GB18030 混合块，逐字符安全解码，保留字节原件，不可逆者标注留痕。触发：文件读不出来、U+FFFD 乱码、PowerShell 追加破坏 UTF-8、编码损坏批量修复。

## 边界（不要越界）

- 本技能只负责"doc"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
