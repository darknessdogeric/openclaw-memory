---
skill_id: "md2all-converter"
title: "MD2ALL Converter - Markdown全能转换技能"
category: "内容生产"
description: "## 技能名称 **MD2ALL Converter** - Markdown转PDF/Word/HTML全能转换器"
when_to_use: ""
size_kb: 5.3
refactored: "2026-06-24"
source: "skills/md2all-converter/SKILL.md"
tags:
  - skills
  - 内容生产
---

# MD2ALL Converter - Markdown全能转换技能

## 技能名称
**MD2ALL Converter** - Markdown转PDF/Word/HTML全能转换器

## 功能特性

✅ **纯Python实现** - 无需外部依赖（wkhtmltopdf/pandoc）  
✅ **完美中文支持** - 自动检测并使用系统中文字体  
✅ **格式完整保留** - 标题、列表、表格、代码块、加粗、斜体  
✅ **一键批量转换** - 支持PDF、Word、HTML同时输出  
✅ **跨平台支持** - Windows/macOS/Linux全平台运行

## 转换能力

| 源格式 | 目标格式 | 支持程度 | 特点 |
|--------|----------|----------|------|
| Markdown | PDF | ⭐⭐⭐⭐⭐ | 专业排版，适合打印 |
| Markdown | Word (.docx) | ⭐⭐⭐⭐⭐ | 可编辑，适合协作 |
| Markdown | HTML | ⭐⭐⭐⭐⭐ | 带样式，适合网页展示 |

## 支持的Markdown语法

- ✅ 标题（H1-H6）
- ✅ 段落和换行
- ✅ 加粗、斜体、删除线
- ✅ 有序/无序列表
- ✅ 链接和图片
- ✅ 代码块（行内和块级）
- ✅ 表格
- ✅ 分隔线
- ✅ 引用块

## 安装方法

### 自动安装（推荐）

双击运行：
```
安装MD2ALL.bat
```

### 手动安装

```bash
# 安装Python依赖
pip install python-docx markdown fpdf2 beautifulsoup4

# 验证安装
python md2all.py
```

## 使用方法

### 方法一：命令行

```bash
# 转换单个文件（输出全部格式）
python md2all.py 文档.md

# 仅转换为PDF
python md2all.py 文档.md pdf

# 仅转换为Word
python md2all.py 文档.md docx

# 仅转换为HTML
python md2all.py 文档.md html
```

### 方法二：Python调用

```python
from md2all import convert_file

# 转换文件
results = convert_file("README.md", output_format="all")
# 返回: [Path('README.pdf'), Path('README.docx'), Path('README.html')]
```

### 方法三：批量转换

```bash
# 转换目录下所有MD文件
for %f in (*.md) do python md2all.py "%f"
```

## 使用示例

### 示例1：转换AHL定价文档

```bash
python md2all.py "AHL综合定价收费体系V1.0.md"
```

输出：
- `AHL综合定价收费体系V1.0.pdf` - 适合打印和分享
- `AHL综合定价收费体系V1.0.docx` - 适合编辑修改
- `AHL综合定价收费体系V1.0.html` - 适合网页展示

### 示例2：仅生成Word版本

```bash
python md2all.py "README.md" docx
```

## 输出效果

### PDF输出特点
- A4纸张格式
- 专业页眉页脚
- 支持页码
- 中文完美显示
- 适合打印和归档

### Word输出特点
- 保留文档结构（标题层级）
- 表格可直接编辑
- 样式与Markdown一致
- 支持协作编辑

### HTML输出特点
- 响应式布局
- 内置美观CSS样式
- 代码高亮
- 适合网页展示

## 故障排除

### 问题1: "未找到模块"
```
ModuleNotFoundError: No module named 'docx'
```
**解决**: 运行 `安装MD2ALL.bat` 或手动执行 `pip install python-docx markdown fpdf2`

### 问题2: PDF中文显示为方框
**解决**: 转换器会自动搜索系统中文字体。如需手动指定：
1. 确保系统安装了中文字体（如：微软雅黑、宋体、黑体）
2. 修改 `md2all.py` 中的 `font_paths` 配置

### 问题3: 表格格式错乱
**解决**: 确保Markdown表格格式正确，使用标准的GitHub Flavored Markdown表格语法。

## 对比其他方案

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **MD2ALL** | 纯Python、无需外部依赖、中文支持好 | 复杂排版有限 | 日常文档转换 |
| wkhtmltopdf | 排版精细 | 需安装额外软件 | 出版级PDF |
| Pandoc | 功能强大 | 配置复杂 | 学术文档 |
| Typora导出 | 界面友好 | 需手动操作 | 单文件转换 |

## 批量转换脚本

### Windows批处理

```batch
@echo off
echo 批量转换Markdown文件...
for %%f in (*.md) do (
    echo 正在转换: %%f
    python md2all.py "%%f"
)
echo 转换完成！
pause
```

### PowerShell脚本

```powershell
Get-ChildItem *.md | ForEach-Object {
    Write-Host "正在转换: $($_.Name)"
    python md2all.py $_.FullName
}
```

## 高级用法

### 自定义PDF样式

```python
from md2all import MarkdownToPDF

converter = MarkdownToPDF("input.md")
converter.pdf.set_author("AHL团队")
converter.pdf.set_title("文档标题")
converter.convert("output.pdf")
```

### 自定义Word样式

```python
from md2all import MarkdownToWord
from docx.shared import Pt, RGBColor

converter = MarkdownToWord("input.md")
# 自定义样式...
converter.convert("output.docx")
```

## 更新日志

- **v1.0** (2026-03-09): 初始版本
  - 支持PDF、Word、HTML三种格式输出
  - 完整支持Markdown常用语法
  - 自动中文字体检测
  - 纯Python实现，无需外部依赖

## 技术栈

- **python-docx**: Word文档生成
- **fpdf2**: PDF文档生成
- **markdown**: Markdown解析
- **beautifulsoup4**: HTML处理（预留）

## 维护信息

- **创建者**: B166ER
- **创建日期**: 2026-03-09
- **适用项目**: AHL去中心化旅行平台及所有Markdown文档
- **开源协议**: MIT

## 相关技能

- `doc-reader` - 文档读取技能
- `document-pdf` - PDF处理技能

---

**提示**: 此技能已完全替代原有的 `md2pdf-converter`，支持更多格式且无需安装wkhtmltopdf。
