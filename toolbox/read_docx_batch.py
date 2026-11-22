#!/usr/bin/env python3
"""读取所有周报 docx,提取结构化数据"""
import os
import sys
from docx import Document

WEEKLY_DIR = r"C:\Users\ericz\Desktop\产业发展部\周例会内容"

docx_files = [
    "2026.8.7 四川花园宾馆 周工作汇报（2026年8月7日-8月13日）.docx",
    "安逸美舍酒店-周工作汇报（8月第2周）8月7日-8月13日.docx",
    "成都总府皇冠假日酒店-周工作汇报（2026.8.7-2026.8.13).docx",
    "锦江金桥酒店)-周工作汇报（8月第2周8月7日-8月13日.docx",
    "乐山锦江嘉州宾馆-周工作汇报（8月7日-8月13日）.docx",
    "(华龙酒店)-周工作汇报（8月7日-8月13日）.docx",
    "(新良大酒店)-周工作汇报（8月7日-8月13日）(1).docx",
]

for fn in docx_files:
    path = os.path.join(WEEKLY_DIR, fn)
    if not os.path.exists(path):
        print(f"### FILE NOT FOUND: {fn}\n")
        continue
    print(f"\n{'='*80}")
    print(f"### FILE: {fn}")
    print(f"{'='*80}")
    try:
        doc = Document(path)
        for para in doc.paragraphs:
            t = para.text.strip()
            if t:
                print(t)
        # Tables
        for i, tbl in enumerate(doc.tables):
            print(f"\n--- TABLE {i+1} ---")
            for row in tbl.rows:
                cells = [c.text.strip() for c in row.cells]
                print(" | ".join(cells))
    except Exception as e:
        print(f"ERROR: {e}")
    print()