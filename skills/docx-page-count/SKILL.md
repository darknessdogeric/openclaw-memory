---
name: docx-page-count
description: 实测 docx 文件真实页数（用 LibreOffice 无头转 PDF 再用 PyMuPDF 数页）。触发场景：用户说「几页」「不要超过 N 页」「控制在一到两页」「压到两页」「页数太多了」「排版几页」「word 有几页」「文档多长」；或交付任何 docx 前需要确认页数是否达标。
---

# docx-page-count · 实测 docx 页数

## 为什么需要这个技能

**页数不能靠估算。** 2026-11-20 用「字号 × 行距 × 边距」推算某个对外文件的页数，估出 2.23 页，**实际渲染是 3 页**，误差 0.8 页 —— 足以让「不要超过 2 页」的要求直接不达标。

**不要用 python-docx 数页**：python-docx 没有排版引擎，`len(docx.paragraphs)` 与页数无对应关系。
**不要用 Word COM**：本机未装 Office，`Word.Application` 抛 `CLSID 未注册`。

## 唯一正本

```
skills/docx-page-count/scripts/docx_pages.py
```

依赖：**LibreOffice**（`C:\Program Files\LibreOffice\program\soffice.com`）+ `PyMuPDF`。

## 用法

```bash
# 一条命令：md → docx → pdf → 页数（含每页字符分布）
python skills/docx-page-count/scripts/docx_pages.py <md文件> <docx输出> "<标题>" "<副标题>"

# 只数已有 docx 的页数
python skills/docx-page-count/scripts/docx_pages.py --pages-only <docx文件>
```

输出示例：

```
DOCX: 38575 B -> ...\某某标准.docx
PAGES = 2
   p1: 716 chars
   p2: 738 chars
```

**每页字符分布是关键信息**：末页字符数远小于首页（如 p3 只有 199 字符）说明「尾页溢出」，削 200~300 字或去掉一张表就能收回上一页。**只看总页数不够，要看末页占了多少。**

## 压页数的有效手法（按性价比排序）

1. **把附表/报价表拆成独立附件文件** —— 一张 10 行表 ≈ 一整页。正文即刻瘦身。表单本来也该单独回传。
2. **减少表格列数** —— 列多则每格窄，中文会在格内折成 3~4 行。7 列砍到 5 列（把「交付标准」移到表下注）能省半页。
3. **合并同类表行** —— 把「达人探店／直播／投流代投」并成一行。
4. **末页只有 100~300 字符时，优先删这一段而不是全文均匀删** —— 收一页只需削尾，不必重构。

## 改版式不是首选

`toolbox/md2docx.py` 的版式（10.5pt、行距 1.35~1.45、上下边距 2.0cm）是统一范式，**不要为了压页数去改模板行距** —— 那会让所有交付件版式漂移。**先删内容或拆附件。**

## 已知限制

- 需要 LibreOffice；未装时先装（国内用清华镜像，见 TOOLS.md 的 LibreOffice 安装记录）。
- 转换中文路径正常；子进程输出是 GBK，脚本内已按字节捕获并 `errors='replace'` 解码。
- 不处理 .doc（旧格式）以外的 .xlsx/.pptx —— 需要时把 `--convert-to pdf` 换成对应 filter 即可。
