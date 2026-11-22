---
name: cn-pdf-local
description: "纯本地 PDF → Markdown 解析（无云端上传，无 token）。触发：需要把 PDF 转成 Markdown 或结构化 JSON，需要提取 PDF 表格、文本、元数据、图片，需要处理扫描型 PDF（无文字层，需 OCR），需要处理多栏版式（学术论文、政府报告），需要按页码选择。需要纯本地处理（不向第三方云上传任何文档）。已集成 pymupdf4llm 多栏检测（默认）+ pdfplumber 表格 + PyMuPDF 图片抽取 + 启发式公式检测。可选 paddleocr（高 OCR 精度，需 Python 3.9-3.12）和 pix2tex（公式 LaTeX 识别，需 torch）。"
title: "本地 PDF 解析（cn-pdf-local v2.0）"
category: "文档处理"
when_to_use: |
  - 需要把 PDF 转成 Markdown / JSON，但**不能用云端 API**（隐私 / 合规）
  - 需要 PDF 表格抽取（结构化输出）
  - 需要扫描型 PDF（无文字层）的 OCR
  - 需要按页码范围抽取（如 "1-5,10,15-20"）
  - 需要 PDF 元数据（创建者、创建时间、页数）
  - 需要多栏版式识别（学术论文、政府报告、报纸）
  - 需要嵌入图片抽取
  - 需要公式位置检测（LaTeX 识别需可选 pix2tex）
user_invocable: true
metadata: {"openclaw": {"emoji": "📄"}}
size_kb: 21.0
refactored: "2026-09-19"
source: "skills/cn-pdf-local/SKILL.md"
tags:
  - pdf
  - markdown
  - 文档解析
  - 本地
  - 中文
  - 离线
  - 多栏
  - 表格
  - 图片
  - ocr
---

# 本地 PDF 解析（cn-pdf-local v2.0）

## 概述

把 PDF 转成 Markdown + 结构化 JSON sidecar + 嵌入图片目录。**所有处理在本地完成，不向任何云端上传。**

v2.0 升级（2026-09-19，Eric 10:44 指令「升级全部四项」）：

| 能力 | v1.0 | v2.0 |
|------|------|------|
| 数字 PDF 文本 | pdfplumber+PyMuPDF | pymupdf4llm（默认）+ fitz 回退 |
| **多栏阅读顺序** | 块排序 | **pymupdf4llm（深度学习启发式）** ⭐ |
| 表格抽取 | pdfplumber | pdfplumber（强化） |
| **图片抽取** | 无 | **PyMuPDF get_images → sidecar 目录** ⭐ |
| 扫描 OCR | pytesseract | pytesseract（默认）/ paddleocr（可选）|
| **公式位置检测** | 无 | **启发式数学符号密度** ⭐ |
| 公式 LaTeX 识别 | 无 | pix2tex（可选，需 torch） |

## 何时使用

- PDF 转 Markdown / 结构化 JSON（纯本地）
- 多栏版式 PDF（学术论文、政府报告、报纸）
- 扫描型 PDF（无文字层）的 OCR
- 需要 PDF 表格抽取
- 需要按页码范围抽取
- 需要嵌入图片（图标、照片、示意图）
- 任何不能上传到云端的敏感文档

**不适用于**：
- 需要 LaTeX 公式**识别**（pix2tex 可选，但需 torch，**当前 Python 3.14 环境未装**）
- 需要云端高精度 OCR（paddleocr 云端 API，本地推理版当前 Python 3.14 未装）

## 依赖（自动检测）

| 工具 | 用途 | 状态（Python 3.14）|
|------|------|------|
| **pymupdf4llm** | 多栏 PDF → Markdown（深度学习启发式）| ✅ 已装 1.28.2 |
| **PyMuPDF (fitz)** | 文本/元数据/图片抽取 | ✅ 已装 1.28.2 |
| **pdfplumber** | 表格抽取 | ✅ 已装 0.11.9 |
| **pytesseract** | OCR Python 绑定 | ✅ 已装 |
| tesseract 二进制 | OCR 引擎 | ❌ 需装 |
| **pdf2image** | PDF→PNG（OCR 前置）| ❌ 需装 |
| PIL | 图像处理 | ✅ 已装 |
| pix2tex | 公式 LaTeX OCR | ❌ Python 3.14 无 wheel |
| paddleocr | 高精度中文 OCR | ❌ Python 3.14 无 paddlepaddle wheel |

## 调用方式

```bash
# 基本：整本 PDF → Markdown + JSON + 图片目录
python scripts/pdf_to_md.py input.pdf output.md

# 指定页码范围
python scripts/pdf_to_md.py input.pdf output.md --pages "1-5,10,15-20"

# 不 prettify（保留原始格式）
python scripts/pdf_to_md.py input.pdf output.md --no-prettify

# 扫描型 PDF 不调用 OCR
python scripts/pdf_to_md.py input.pdf output.md --no-ocr

# 不抽取图片
python scripts/pdf_to_md.py input.pdf output.md --no-images

# 用 paddleocr（需先装 paddleocr + paddlepaddle）
python scripts/pdf_to_md.py input.pdf output.md --ocr-engine paddleocr

# 不用 pymupdf4llm（回退到 PyMuPDF 块排序）
python scripts/pdf_to_md.py input.pdf output.md --no-pymupdf4llm
```

或代码内调用：

```python
from skills.cn-pdf-local.scripts.pdf_to_md import pdf_to_markdown
pdf_to_markdown('report.pdf', 'report.md', page_ranges='1-10')
```

## 输出

每次生成**三个产物**：

1. **`output.md`** — Markdown 主输出（按页分章节、表格、嵌入图片引用、公式检测标记）
2. **`output.json`** — 结构化 sidecar（含元数据、每页文本、表格数据、图片清单、工具状态）
3. **`output_images/`** — 嵌入图片目录（按 `p{N}_img{M}.{ext}` 命名）

## 处理路径

```
PDF 输入
  ↓
scan_type 检测（前 3 页字符数）
  ├─ digital (avg ≥ 50)
  │   ↓
  │   pymupdf4llm 多栏 + 表格 + 标题层级
  │   ↓
  │   pdfplumber 表格补充（更准的单元格识别）
  │   ↓
  │   PyMuPDF 图片抽取（get_images）
  │   ↓
  │   公式位置启发式检测（数学符号密度）
  │
  └─ scanned (avg < 50)
      ↓
      pdf2image 渲染 PNG（200 dpi）
      ↓
      pytesseract / paddleocr OCR
```

## 与已卸载的 `paddleocr-doc-parsing` 能力对比

| 能力 | paddleocr（云） | cn-pdf-local v2.0（本地） |
|------|------|------|
| 数字 PDF 文本提取 | ✅ | ✅ |
| **多栏阅读顺序** | ✅（云端深度学习） | ✅ **pymupdf4llm 本地** ⭐ |
| 表格抽取 | ✅（云端） | ✅ pdfplumber 本地 ⭐ |
| **图片抽取** | ✅（云端） | ✅ **PyMuPDF get_images 本地** ⭐ |
| 扫描 PDF OCR | ✅ | ✅ pytesseract（paddleocr 需 Py3.9-3.12）|
| 页码范围选择 | ✅ | ✅ |
| 元数据提取 | ✅ | ✅ |
| 公式位置检测 | ✅（云端） | ✅ **启发式本地** ⭐ |
| 公式识别 LaTeX | ✅ | ⚠️ pix2tex（需 torch + Py3.9-3.12）|
| 印章识别 | ✅ | ❌ |
| **数据流向** | ⚠️ **上传云** | ✅ **纯本地** |

## 已知限制

- **多栏版式**：pymupdf4llm 启发式精度 90%+，极端复杂版式（如嵌套表格）可能错序
- **扫描型 PDF OCR**：tesseract 中文精度 ~75-85%；paddleocr 本地版 ~95% 但需 Python 3.9-3.12
- **公式识别**：仅位置检测 + 启发式标记，LaTeX 输出需 pix2tex（需 torch）
- **图表内容识别**：仅抽取嵌入图片保存，不做图表内容 OCR
- **环境兼容性**：当前 Python 3.14 环境无法安装 paddleocr / pix2tex（缺对应 wheel）

## 升级路径（用户触发才动）

| 升级 | 触发条件 | 工作量 |
|------|---------|--------|
| 切换到 Python 3.11 + paddleocr | 中文扫描精度需提升 | 半天 |
| 安装 pix2tex + 公式 LaTeX OCR | 学术文档含公式 | 半天 |
| 接入 layoutparser / 自训练版面模型 | 复杂多栏需更高精度 | 1 周 |