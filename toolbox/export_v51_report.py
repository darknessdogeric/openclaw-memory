#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v5.1 md → docx 转换"""
import os
import sys
import re

sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from md_to_docx_v3 import (
    set_font, parse_inline, add_heading_custom, add_body, add_quote,
    add_list, add_list_numbered, set_cell_content, set_cell_shading, add_table
)
from docx import Document
from docx.shared import Cm

SRC = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\07_战略与改革\半年报告\2026-H1\半年报_v5.1_完整数据版_2026-09-07.md'

OUTS = [
    r'C:\Users\ericz\Desktop\酒店行业H1半年报_v5.1_完整数据版_2026-09-07.docx',
    r'C:\Users\ericz\Desktop\产业发展部\项目\酒店行业H1半年报_v5.1_完整数据版_2026-09-07.docx',
    r'C:\Users\ericz\Desktop\产业发展部\酒店行业H1半年报_v5.1_完整数据版_2026-09-07.docx',
]

def md_to_docx_v51(md_path, docx_path):
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

        if stripped.startswith('# '):
            add_heading_custom(doc, stripped[2, 'stripped.startswith('## '
            add_heading_custom(doc, 'stripped.startswith('### '
            add_heading_custom(doc, 'stripped.startswith('#### '
        elif stripped.startswith('> '):
            add_quote(doc, stripped[2:])
        elif stripped == '---':
            continue
        elif stripped.startswith('- '):
            add_list(doc, stripped[2:])
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.':
            add_list_numbered(doc, re.sub(r'^\d+\.\s', '', stripped))
        else:
            add_body(doc, stripped)

    flush_table()

    doc.add_paragraph('')
    p = doc.add_paragraph()
    set_font(p.add_run('来源：anyi-ops-kb/07_战略与改革/半年报告/2026-H1/半年报_v5.1_完整数据版_2026-09-07.md'),
             '仿宋', 9, color=(128, 128,), italic=True)

    doc.save(docx_path)
    return os.path.getsize(docx_path) / 1024

print('半年报 v5.1 → Word')
for out in OUTS:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    size = md_to_docx_v51(SRC, out)
    print(f'  [OK] {out} ({size:.1f} KB)')
print('=== 完成 ===')