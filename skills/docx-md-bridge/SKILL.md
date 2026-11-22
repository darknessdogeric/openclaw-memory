---
name: docx-md-bridge
description: "通用 Markdown 与 Word 互转（非公文场景）。触发：把 Markdown 转成普通 Word 文档（报告/演讲稿/研究材料/技术文档），需要中英文字体绑定（eastAsia），需要支持表格、代码块、引用、列表的混合内容，不需要 GB/T 9704 公文规范。适合日常办公场景。如需严格的党政机关公文格式请改用 gongwen-docx-cn 技能。"
title: "Markdown ↔ Word 通用互转"
category: "文档生成"
when_to_use: |
  - 需要把 Markdown 转成普通 Word 文档（不是公文）
  - 需要保留 Markdown 表格、代码块、引用等结构
  - 需要中英文字体绑定（中文不变成方块）
  - 不需要符合 GB/T 9704 公文格式（那种请用 gongwen-docx-cn）
user_invocable: true
metadata: {"openclaw": {"emoji": "📄"}}
size_kb: 4.2
refactored: "2026-09-19"
source: "skills/docx-md-bridge/SKILL.md"
tags:
  - markdown
  - docx
  - word
  - 文档生成
  - bridge
---

# Markdown ↔ Word 通用互转

## 概述

把 Markdown 文档转成结构清晰的 Word 文档（`.docx`）。**非公文场景**，适合：

- 研究报告、调研材料
- 会议演讲稿、内部汇报
- 技术文档、API 文档
- 任何需要把 Markdown 沉淀为 Word 但不要求党政公文格式的场景

**对比 `gongwen-docx-cn`**：本技能用通用字体（等线），不做 GB/T 9704 公文规范。如果需要公文格式请改用 `gongwen-docx-cn`。

## 字体规范（通用办公）

| 元素 | 字体 | 字号 |
|------|------|------|
| 标题（一级 H1） | 等线 | 16pt 加粗 |
| 二级标题 | 等线 | 14pt 加粗 |
| 三级标题 | 等线 | 12pt 加粗 |
| 四级标题 | 等线 | 11pt 加粗 |
| 正文 | 等线 | 11pt |
| 表格内 | 等线 | 10pt，表头加粗 |
| 代码块 | 等线 | 9pt |

## 排版规范

| 项目 | 数值 | 说明 |
|------|------|------|
| 首行缩进 | 2 字符 | 段落首行 |
| 标题居中 | 仅一级 | 文档主标题居中 |
| 表格 | 黑色 0.5pt 边框 | Table Grid |
| 代码块 | 缩进 2 字符 | 不喧宾夺主 |
| 引用 | 左缩进 2 字符 | Markdown `>` 行 |

## 调用方式

```bash
python scripts/md_to_docx.py <src.md> <dst.docx>
```

或代码内调用：

```python
from skills.docx-md-bridge.scripts.md_to_docx import md_to_docx
md_to_docx('report.md', 'report.docx')
```

## 与其他文档生成技能的对比

| 场景 | 技能 |
|------|------|
| 中文公文（GB/T 9704-2012）| `gongwen-docx-cn` |
| 普通报告 / 演讲稿 / 研究 | **`docx-md-bridge`** ← 你在这里 |
| PPT 生成 | `powerpoint-pptx` / `super-ppt` |

## 支持的 Markdown 语法

- `# / ## / ### / ####` 标题
- 段落（自动首行缩进 2 字符）
- `- xxx` / `* xxx` 列表（自动转为 • 符号 + 缩进）
- `> xxx` 引用（缩进显示）
- 表格（`| --- |` 格式，自动转 Word 表格）
- 代码块（```` ``` ```` 围栏，自动转缩进段落）
- 行内 `code` 标记
- 加粗 `**xxx**`、斜体 `*xxx*`
- 分隔线 `---`
