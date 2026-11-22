"""md_to_docx_v1.0.py - 简单 Markdown 转 Word(支持表格)
用法: python md_to_docx_v1.0.py <input.md> <output.docx>
"""
import sys
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def parse_md_table(lines, start_idx):
    """解析 Markdown 表格,返回 (rows, end_idx)"""
    rows = []
    i = start_idx
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.startswith('|'):
            break
        if re.match(r'^\|[\s\-:|]+\|$', line):
            i += 1
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
        i += 1
    return rows, i


def set_cell_shading(cell, color_hex):
    """设置单元格背景色"""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)


def add_bold_text(paragraph, text):
    """添加支持 **bold** 的段落"""
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            paragraph.add_run(part)


def add_inline_text(paragraph, text):
    """添加段落文本(支持 **bold** 和 `code`)"""
    # 先处理代码
    parts = re.split(r'(`[^`]+`)', text)
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(10)
            # 中文处理
            r = run._element
            rPr = r.get_or_add_rPr()
            rFonts = rPr.find(qn('w:rFonts'))
            if rFonts is None:
                rFonts = OxmlElement('w:rFonts')
                rPr.append(rFonts)
            rFonts.set(qn('w:eastAsia'), 'Consolas')
        else:
            # 处理加粗
            sub_parts = re.split(r'(\*\*[^*]+\*\*)', part)
            for sub in sub_parts:
                if sub.startswith('**') and sub.endswith('**'):
                    run = paragraph.add_run(sub[2:-2])
                    run.bold = True
                else:
                    paragraph.add_run(sub)


def md_to_docx(md_path, docx_path):
    md_path = Path(md_path)
    docx_path = Path(docx_path)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    doc = Document()

    # 设置默认字体(中文宋体)
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            i += 1
            continue

        # 标题
        if stripped.startswith('#'):
            level = 0
            for ch in stripped:
                if ch == '#':
                    level += 1
                else:
                    break
            text = stripped[level:].strip()
            heading = doc.add_heading('', level=min(level, 4))
            add_inline_text(heading, text)
            i += 1
            continue

        # 代码块
        if stripped.startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束 ```
            if code_lines:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.5)
                for cl in code_lines:
                    run = p.add_run(cl)
                    run.font.name = 'Consolas'
                    run.font.size = Pt(9)
                    r = run._element
                    rPr = r.get_or_add_rPr()
                    rFonts = rPr.find(qn('w:rFonts'))
                    if rFonts is None:
                        rFonts = OxmlElement('w:rFonts')
                        rPr.append(rFonts)
                    rFonts.set(qn('w:eastAsia'), 'Consolas')
            continue

        # 表格
        if stripped.startswith('|'):
            rows, i = parse_md_table(lines, i)
            if not rows:
                continue
            n_cols = max(len(r) for r in rows)
            table = doc.add_table(rows=len(rows), cols=n_cols)
            table.style = 'Table Grid'

            # 表头着色
            for col_idx in range(n_cols):
                if len(rows[0]) > col_idx:
                    cell = table.rows[0].cells[col_idx]
                    set_cell_shading(cell, 'D9E1F2')  # 淡蓝色
                    cell.paragraphs[0].clear()
                    add_inline_text(cell.paragraphs[0], rows[0][col_idx])

            # 数据行
            for row_idx in range(1, len(rows)):
                for col_idx in range(n_cols):
                    cell = table.rows[row_idx].cells[col_idx]
                    if col_idx < len(rows[row_idx]):
                        cell.paragraphs[0].clear()
                        add_inline_text(cell.paragraphs[0], rows[row_idx][col_idx])
            continue

        # 引用
        if stripped.startswith('>'):
            # 多行引用
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            text = '\n'.join(quote_lines)
            for ql in quote_lines:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.5)
                run = p.add_run(ql)
                run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            continue

        # 列表
        if re.match(r'^[\-\*]\s+', stripped):
            text = re.sub(r'^[\-\*]\s+', '', stripped)
            p = doc.add_paragraph(style='List Bullet')
            add_inline_text(p, text)
            i += 1
            continue

        # 数字列表
        if re.match(r'^\d+\.\s+', stripped):
            text = re.sub(r'^\d+\.\s+', '', stripped)
            p = doc.add_paragraph(style='List Number')
            add_inline_text(p, text)
            i += 1
            continue

        # 普通段落
        p = doc.add_paragraph()
        add_inline_text(p, stripped)
        i += 1

    doc.save(docx_path)
    print(f'Converted: {md_path} -> {docx_path}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python md_to_docx_v1.0.py <input.md> <output.docx>')
        sys.exit(1)
    md_to_docx(sys.argv[1], sys.argv[2])