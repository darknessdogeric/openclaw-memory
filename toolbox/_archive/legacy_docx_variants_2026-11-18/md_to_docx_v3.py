#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_docx_v3.py - Markdown �?Word（去除所�?Markdown 符号�?Eric 2026-09-07 08:47 指令：不要再�?MD �?* 等符号带入，就是正常文字表格
关键：正确解�?**粗体** / *斜体* / `代码`，输出纯文字+格式
"""
import os
import re
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\07_战略与改革\产业发展部_2026年集团考核指标_v1.0.md'
OUT = r'C:\Users\ericz\Desktop\产业发展部_2026年集团考核指标_v1.0.docx'

def set_font(run, name_zh, size, bold=False, color=None, italic=False, mono=False):
    """设置中文字体"""
    if mono:
        run.font.name = 'Consolas'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    else:
        run.font.name = name_zh
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name_zh)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def parse_inline(p, text, base_name, base_size, base_bold=False, base_color=None, base_italic=False):
    """解析行内 Markdown，输出多�?run（正确处�?**粗体** / *斜体* / `代码`�?    核心：去掉所�?markdown 符号，保留文�?+ 格式
    """
    # 先处�?**粗体**（贪婪）
    # 正则�?*xxx** �?__xxx__
    pos = 0
    # �?tokenizer 方式处理
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`|__.*?__)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**') and len(token) >= 4:
            # 粗体
            inner = token[2:-2]
            set_font(p.add_run(inner), base_name, base_size, bold=True, color=base_color, italic=base_italic)
        elif token.startswith('__') and token.endswith('__') and len(token) >= 4:
            inner = token[2:-2]
            set_font(p.add_run(inner), base_name, base_size, bold=True, color=base_color, italic=base_italic)
        elif token.startswith('`') and token.endswith('`') and len(token) >= 2:
            inner = token[1:-1]
            set_font(p.add_run(inner), '宋体', base_size, bold=base_bold, color=base_color, mono=True)
        elif token.startswith('*') and token.endswith('*') and len(token) >= 2:
            inner = token[1:-1]
            set_font(p.add_run(inner), base_name, base_size, bold=base_bold, color=base_color, italic=True)
        else:
            set_font(p.add_run(token), base_name, base_size, bold=base_bold, color=base_color, italic=base_italic)

def add_heading_custom(doc, text, level):
    p = doc.add_paragraph()
    # 标题里的 markdown 符号也去�?    text = text.replace('**', '').replace('*', '').replace('`', '')
    if level == 0:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.add_run(text), '黑体', 18, bold=True)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.space_before = Pt(6)
    elif level == 1:
        set_font(p.add_run(text), '黑体', 15, bold=True)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
    elif level == 2:
        set_font(p.add_run(text), '黑体', 13, bold=True)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(6)
    elif level == 3:
        set_font(p.add_run(text), '楷体', 12, bold=True)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
    return p

def add_body(doc, text):
    p = doc.add_paragraph()
    parse_inline(p, text, '仿宋', 12)
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_after = Pt(3)
    return p

def add_quote(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    parse_inline(p, text, '楷体', 11, base_color=(100, 100, 100))
    p.paragraph_format.space_after = Pt(3)
    return p

def add_list(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.space_after = Pt(2)
    # 前置项目符号
    set_font(p.add_run('�? '), '仿宋', 12)
    parse_inline(p, text, '仿宋', 12)
    return p

def add_list_numbered(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.space_after = Pt(2)
    set_font(p.add_run('·  '), '仿宋', 12)
    parse_inline(p, text, '仿宋', 12)
    return p

def set_cell_shading(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)

def set_cell_content(cell, text, bold=False):
    """单元格内容，同样去除 markdown 符号"""
    cell.text = ''
    p = cell.paragraphs[0]
    parse_inline(p, text, '宋体', 10.5, base_bold=bold)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)

def add_table(doc, rows_data):
    if not rows_data:
        return
    n_rows = len(rows_data)
    n_cols = max(len(r) for r in rows_data)
    tbl = doc.add_table(rows=n_rows, cols=n_cols)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r_idx, row in enumerate(rows_data):
        for c_idx in range(n_cols):
            cell = tbl.rows[r_idx].cells[c_idx]
            text = row[c_idx].strip() if c_idx < len(row) else ''
            if r_idx == 0:
                set_cell_content(cell, text, bold=True)
                set_cell_shading(cell, 'D9E2F3')
            else:
                set_cell_content(cell, text, bold=False)

    doc.add_paragraph('')

def md_to_docx(md_path, docx_path):
    doc = Document()
    for section in doc.sections:
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if table_rows:
            add_table(doc, table_rows)
        table_rows = []
        in_table = False

    for line in lines:
        raw = line.rstrip('\n')
        stripped = raw.strip()

        # 表格
        if stripped.startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            if not stripped.replace('|', '').replace('-', '').replace(':', '').strip():
                continue
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            table_rows.append(cells)
            continue
        elif in_table:
            flush_table()

        if not stripped:
            continue

        # 标题
        if stripped.startswith('# '):
            add_heading_custom(doc, stripped[2:], 0)
        elif stripped.startswith('## '):
            add_heading_custom(doc, stripped[3:], 1)
        elif stripped.startswith('### '):
            add_heading_custom(doc, stripped[4:], 2)
        elif stripped.startswith('#### '):
            add_heading_custom(doc, stripped[5:], 3)
        # 引用
        elif stripped.startswith('> '):
            add_quote(doc, stripped[2:])
        # 分隔�?        elif stripped == '---':
            continue
        # 列表
        elif stripped.startswith('- '):
            add_list(doc, stripped[2:])
        elif re.match(r'^\d+\.\s', stripped):
            add_list_numbered(doc, re.sub(r'^\d+\.\s', '', stripped))
        # 正文
        else:
            add_body(doc, stripped)

    flush_table()

    # 页脚
    doc.add_paragraph('')
    p = doc.add_paragraph()
    import os as _os
    footer_name = _os.path.basename(SRC)
    set_font(p.add_run(f'来源：{SRC}'),
             '仿宋', 9, color=(128, 128, 128), italic=True)

    doc.save(docx_path)
    return os.path.getsize(docx_path) / 1024

print('=' * 55)
print('Markdown �?Word（去除所�?Markdown 符号�?)
print('=' * 55)
print(f'\n源文�? {SRC}')
print(f'  大小: {os.path.getsize(SRC)/1024:.1f} KB')
import sys as _sys_out
_OUT = _sys_out.argv[2] if len(_sys_out.argv) > 2 else OUT
size = md_to_docx(SRC, _OUT)
print(f'  [OK] {size:.1f} KB')
print('已去除所�?Markdown 符号�?)
print('  · **粗体** �?加粗文字（星号已去除�?)
print('  · *斜体* �?斜体文字（星号已去除�?)
print('  · `代码` �?等宽字体（反引号已去除）')
print('  · # 标题 �?黑体分级')
print('  · > 引用 �?楷体灰色缩进')
print('  · - 列表 �?项目符号')
print('  · | 表格 �?正常网格表格')
