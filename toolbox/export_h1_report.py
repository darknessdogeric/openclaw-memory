#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""半年报 v4.0 md → docx（去 Markdown 符号版）"""
import os
import sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from md_to_docx_v3 import md_to_docx

SRC = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\07_战略与改革\半年报告\2026-H1\半年报_v4.0_完整版_2026-09-07.md'

# 输出三份（Eric 工作流：桌面 + 产业发展部/项目）
OUTS = [
    r'C:\Users\ericz\Desktop\酒店行业H1半年报_v4.0_完整版_2026-09-07.docx',
    r'C:\Users\ericz\Desktop\产业发展部\项目\酒店行业H1半年报_v4.0_完整版_2026-09-07.docx',
    r'C:\Users\ericz\Desktop\产业发展部\酒店行业H1半年报_v4.0_完整版_2026-09-07.docx',
]

for out in OUTS:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    size = md_to_docx(SRC, out)
    print(f'  [OK] {out} ({size:.1f} KB)')

print('\n=== 完成 ===')
print('半年报 v4.0 Word 版已生成 3 份，Eric 可在桌面看到。')