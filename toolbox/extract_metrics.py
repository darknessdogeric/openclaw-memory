#!/usr/bin/env python3
"""提取每家酒店的核心数据"""
import re
from docx import Document

WEEKLY_DIR = r"C:\Users\ericz\Desktop\产业发展部\周例会内容"

hotels = [
    ("四川花园宾馆", "2026.8.7 四川花园宾馆 周工作汇报（2026年8月7日-8月13日）.docx"),
    ("安逸美舍酒店", "安逸美舍酒店-周工作汇报（8月第2周）8月7日-8月13日.docx"),
    ("总府皇冠假日", "成都总府皇冠假日酒店-周工作汇报（2026.8.7-2026.8.13).docx"),
    ("锦江金桥", "锦江金桥酒店)-周工作汇报（8月第2周8月7日-8月13日.docx"),
    ("乐山锦江嘉州", "乐山锦江嘉州宾馆-周工作汇报（8月7日-8月13日）.docx"),
    ("华龙酒店", "(华龙酒店)-周工作汇报（8月7日-8月13日）.docx"),
    ("新良大酒店", "(新良大酒店)-周工作汇报（8月7日-8月13日）(1).docx"),
]

import os
for hname, fn in hotels:
    path = os.path.join(WEEKLY_DIR, fn)
    if not os.path.exists(path):
        print(f"### NOT FOUND: {hname}")
        continue
    print(f"\n{'='*70}\n### {hname}\n{'='*70}")
    doc = Document(path)
    # Get only the FIRST occurrence of each row (dedupe by line)
    text_lines = []
    seen = set()
    for p in doc.paragraphs:
        t = p.text.strip()
        if t and t not in seen:
            seen.add(t)
            text_lines.append(t)
    # Get tables, dedupe cells in each row
    for tbl in doc.tables:
        for row in tbl.rows:
            cells_seen = set()
            cells = []
            for c in row.cells:
                ct = c.text.strip()
                if ct not in cells_seen:
                    cells_seen.add(ct)
                    cells.append(ct)
            line = " | ".join(cells)
            if line and line not in seen:
                seen.add(line)
                text_lines.append(line)
    for line in text_lines:
        print(line)