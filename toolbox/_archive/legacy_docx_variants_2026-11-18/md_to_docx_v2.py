#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_docx_v2.py - Markdown 转 Word（规范排版版）
Eric 2026-09-07 08:40：排版问题，重新弄
排版规范：
  - 标题：黑体加粗（居中一级 / 左对齐二三级）
  - 正文：仿宋 12pt（小四）
  - 表格：Table Grid 简洁网格 + 表头加粗灰底
  - 引用：楷体 灰色
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\07_战略与改革\产业发展部_2026年集团考核指标_v1.0.md'
OUT = r'C:\Users\ericz\Desktop\产业发展部_2026年集团考核指标_v1.0.docx'

def set_font(run, name_zh, name_en, size, bold=False, color=None, italic=False):
    """设置中文字体（需同时设置 eastAsia）"""
    run.font.name = name_en
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name_zh)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_heading_custom(doc, text, level):
    """自定义标题（避免 built-in 样式中文字体问题）"""
    p = doc.add_paragraph()
    if level == 0:  # 文档主标题
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.add_run(text), '黑体', 'SimHei', 18, bold=True)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.space_before = Pt(6)
    elif level == 1:  # 一级标题 ##
        set_font(p.add_run(text), '黑体', 'SimHei', 15, bold=True)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
    elif level == 2:  # 二级标题 ###
        set_font(p.add_run(text), '黑体', 'SimHei', 13, bold=True)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(6)
    elif level == 3:  # 三级标题 ####
        set_font(p.add_run(text), '楷体', 'KaiTi', 12, bold=True)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
    return p

def add_body(doc, text):
    """正文段落"""
    p = doc.add_paragraph()
    set_font(p.add_run(text), '仿宋', 'FangSong', 12)
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_after = Pt(3)
    return p

def add_quote(doc, text):
    """引用段落（楷体灰色）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    set_font(p.add_run(text), '楷体', 'KaiTi', 11, color=(100, 100, 100))
    p.paragraph_format.space_after = Pt(3)
    return p

def add_list(doc, text, numbered=False):
    """列表段落"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    prefix = '•  ' if not numbered else '1.  '
    set_font(p.add_run(prefix + text), '仿宋', 'FangSong', 12)
    p.paragraph_format.space_after = Pt(2)
    return p

def set_cell_shading(cell, color_hex):
    """设置单元格背景色"""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)

def set_cell_font(cell, text, size=10.5, bold=False):
    """设置单元格文字（含字体）"""
    cell.text = ''
    p = cell.paragraphs[0]
    set_font(p.add_run(text), '宋体', 'SimSun', size, bold=bold)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)

def add_table(doc, rows_data):
    """添加规范表格"""
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
            # 表头（第一行）加粗 + 灰底
            if r_idx == 0:
                set_cell_font(cell, text, size=10.5, bold=True)
                set_cell_shading(cell, 'D9E2F3')
            else:
                set_cell_font(cell, text, size=10.5, bold=False)

    doc.add_paragraph('')
    return tbl

def md_to_docx(md_path, docx_path):
    doc = Document()
    # 页面边距
    for section in doc.sections:
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_rows = []
    list_counter = 0

    def flush_table():
        nonlocal table_rows, in_table
        if table_rows:
            add_table(doc, table_rows)
        table_rows = []
        in_table = False

    for line in lines:
        raw = line.rstrip('\n')
        stripped = raw.strip()

        # 表格处理优先
        if stripped.startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            # 跳过分隔行 |---|---|
            if not stripped.replace('|', '').replace('-', '').replace(':', '').strip():
                continue
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            table_rows.append(cells)
            continue
        elif in_table and not stripped:
            flush_table()
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
        # 分隔线
        elif stripped == '---':
            p = doc.add_paragraph()
            set_font(p.add_run(''), '仿宋', 'FangSong', 6)
        # 无序列表
        elif stripped.startswith('- '):
            add_list(doc, stripped[2:], numbered=False)
        # 有序列表
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.':
            add_list(doc, stripped.split('. ', 1)[1] if '. ' in stripped else stripped[2:], numbered=True)
        # 普通正文
        else:
            add_body(doc, stripped)

    flush_table()

    # 页脚
    doc.add_paragraph('')
    p = doc.add_paragraph()
    set_font(p.add_run('来源：anyi-ops-kb/07_战略与改革/产业发展部_2026年集团考核指标_v1.0.md'),
             '仿宋', 'FangSong', 9, color=(128, 128, 128), italic=True)

    doc.save(docx_path)
    return os.path.getsize(docx_path) / 1024

print('=' * 55)
print('Markdown → Word（规范排版版）')
print('=' * 55)
print(f'\n源文件: {SRC}')
print(f'  大小: {os.path.getsize(SRC)/1024:.1f} KB')
print(f'\n输出: {OUT}')
size = md_to_docx(SRC, OUT)
print(f'  [OK] {size:.1f} KB')
print('\n=== 完成 ===')
print('排版规范：')
print('  · 主标题：黑体 18pt 居中')
print('  · 一级标题：黑体 15pt')
print('  · 二级标题：黑体 13pt')
print('  · 正文：仿宋 12pt 1.4 倍行距')
print('  · 表格：Table Grid 网格 + 表头蓝灰底加粗')
print('  · 引用：楷体 11pt 灰色缩进')