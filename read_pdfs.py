# -*- coding: utf-8 -*-
import pdfplumber
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

pdf_files = [
    r'E:\桌面20250702\SM-SOP-RM-01 收益管理日常运营流程.pdf',
    r'E:\桌面20250702\SM-SOP-RM-02 收益管理例会流程.pdf',
    r'E:\桌面20250702\SM-SOP-RM-02A 中旅酒店收益管理例会模板.pdf',
    r'E:\管理项目\项目测算表170315 （清凤时代城）.xls.pdf',
]

for pdf_path in pdf_files:
    if not os.path.exists(pdf_path):
        print(f'NOT FOUND: {pdf_path}')
        continue
    
    print(f'\n\n{"="*60}')
    print(f'FILE: {os.path.basename(pdf_path)}')
    print(f'{"="*60}')
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f'Pages: {len(pdf.pages)}')
            for i, page in enumerate(pdf.pages[:8]):
                text = page.extract_text()
                if text and len(text.strip()) > 10:
                    lines = text.split('\n')
                    print(f'\n--- Page {i+1} ---')
                    for line in lines[:40]:
                        if line.strip():
                            print(f'  {line.strip()[:120]}')
    except Exception as e:
        print(f'Error: {e}')
