#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_docx.py - Markdown 转 Word (Eric 桌面)
Eric 2026-09-07 08:36 指令：产业发展部考核指标 v1.0 → Word
"""
import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\07_战略与改革\产业发展部_2026年集团考核指标_v1.0.md'

# 输出目标（双备份）
OUT_PRIMARY = r'C:\Users\ericz\Desktop\产业发展部_2026年集团考核指标_v1.0.docx'
OUT_SECONDARY = r'C:\Users\ericz\Desktop\产业发展部\产业发展部_2026年集团考核指标_v1.0.docx'

# Markdown 解析（轻量级手写解析，避免依赖）
def parse_inline(text):
    """解析粗体 **xxx** 和代码 `xxx`"""
    return text  # 简化处理，docx 会自动处理

def md_to_docx(md_path, docx_path):
    doc = Document()
    # 设置全局样式
    style = doc.styles['Normal']
    style.font.name = 'Microsoft YaHei'  # 中文字体
    style.font.size = Pt(10.5)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_rows = []

    def flush_table():
        if not table_rows:
            return
        cols = len(table_rows[0])
        tbl = doc.add_table(rows=len(table_rows), cols=cols)
        tbl.style = 'Light Grid Accent 1'
        for r_idx, row in enumerate(table_rows):
            for c_idx, cell_text in enumerate(row):
                if c_idx < cols:
                    tbl.rows[r_idx].cells[c_idx].text = cell_text.strip()
        doc.add_paragraph('')
        table_rows.clear()

    for line in lines:
        raw = line.rstrip('\n')
        stripped = raw.strip()

        # 跳过空行（在表格外）
        if not stripped and not in_table:
            continue

        # 标题
        if stripped.startswith('# '):
            flush_table()
            doc.add_heading(stripped[2:], level=0)
        elif stripped.startswith('## '):
            flush_table()
            doc.add_heading(stripped[3:], level=1)
        elif stripped.startswith('### '):
            flush_table()
            doc.add_heading(stripped[4:], level=2)
        elif stripped.startswith('#### '):
            flush_table()
            doc.add_heading(stripped[5:], level=3)
        # 引用
        elif stripped.startswith('> '):
            flush_table()
            p = doc.add_paragraph(stripped[2:], style='Quote')
        # 分隔线
        elif stripped == '---':
            flush_table()
            doc.add_paragraph('─' * 40)
        # 表格
        elif stripped.startswith('|') and not in_table:
            in_table = True
            # 第一行是表头
            table_rows.append([c.strip() for c in stripped.strip('|').split('|')])
        elif stripped.startswith('|') and in_table:
            # 跳过分隔行 |---|---|
            if not stripped.replace('|', '').replace('-', '').replace(':', '').strip():
                continue
            table_rows.append([c.strip() for c in stripped.strip('|').split('|')])
        elif in_table and not stripped:
            in_table = False
            flush_table()
        # 列表
        elif stripped.startswith('- '):
            flush_table()
            doc.add_paragraph(stripped[2:], style='List Bullet')
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] in ['. ', ') ']:
            flush_table()
            doc.add_paragraph(stripped[3:], style='List Number')
        # 普通段落
        else:
            flush_table()
            if stripped:
                doc.add_paragraph(stripped)

    flush_table()

    # 添加页脚
    doc.add_paragraph('─' * 40)
    footer = doc.add_paragraph()
    footer_run = footer.add_run('来源文件: anyi-ops-kb/07_战略与改革/产业发展部_2026年集团考核指标_v1.0.md')
    footer_run.italic = True
    footer_run.font.size = Pt(8)
    footer_run.font.color.rgb = RGBColor(128, 128, 128)

    doc.save(docx_path)
    print(f'  [OK] {docx_path}')
    print(f'    Size: {os.path.getsize(docx_path)/1024:.1f} KB')

print('=' * 60)
print('Markdown → Word 转换 (Eric 桌面)')
print('=' * 60)

print(f'\n[1/3] 读取源文件: {SRC}')
print(f'    Size: {os.path.getsize(SRC)/1024:.1f} KB')

print(f'\n[2/3] 转换 → {OUT_PRIMARY}')
md_to_docx(SRC, OUT_PRIMARY)

print(f'\n[3/3] 备份 → {OUT_SECONDARY}')
os.makedirs(os.path.dirname(OUT_SECONDARY), exist_ok=True)
md_to_docx(SRC, OUT_SECONDARY)

print('\n=== 完成 ===')
print('两份 docx 已就绪：')
print(f'  1. 桌面根目录: {OUT_PRIMARY}')
print(f'  2. 桌面\\产业发展部: {OUT_SECONDARY}')