# -*- coding: utf-8 -*-
import json
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

# Read PDF files - check project measurement files
pdf_files = []
desktop_files = os.listdir(r'E:\桌面')
for f in desktop_files:
    if f.endswith('.pdf') or '测算' in f or '项目' in f:
        print('Desktop PDF:', f)

# Check project measurement files
proj_dirs = [r'E:\管理项目', r'E:\桌面20250702']
for d in proj_dirs:
    if os.path.exists(d):
        print(f'\n=== {d} ===')
        for f in os.listdir(d):
            if '测算' in f or '项目' in f or f.endswith('.pdf'):
                print(f'  {f}')

# Read the budget guidelines xlsx files
print('\n\n=== Budget Guidelines ===')
with open(r'C:\Users\ericz\.openclaw\workspace\excel_data_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if '指导意见' in item['file'] or '注意事项' in item['file']:
        print(f'\nFile: {item["file"]}')
        for sheet in item.get('sheets', [])[:2]:
            print(f'\nSheet: {sheet["name"]}')
            for row in sheet['rows'][:30]:
                cells = row['cells']
                non_empty = [c for c in cells if c and c != '#REF!' and c != '#DIV/0!']
                if non_empty:
                    print('  Row', row['row'], ':', ' | '.join(non_empty[:8]))
