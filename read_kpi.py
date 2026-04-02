# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\ericz\.openclaw\workspace\excel_data_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the performance evaluation file
for item in data:
    if '考核' in item['file']:
        print('=== Performance Evaluation ===')
        print('File:', item['file'])
        for sheet in item.get('sheets', []):
            print(f'\nSheet: {sheet["name"]}')
            for row in sheet['rows']:
                cells = row['cells']
                non_empty = [c for c in cells if c and c != '#REF!' and c != '#DIV/0!']
                if non_empty:
                    print('  Row', row['row'], ':', ' | '.join(non_empty[:10]))
        print()
    
    if 'KPI' in item['file']:
        print('=== KPI ===')
        print('File:', item['file'])
        for sheet in item.get('sheets', []):
            print(f'\nSheet: {sheet["name"]}')
            for row in sheet['rows']:
                cells = row['cells']
                non_empty = [c for c in cells if c and c != '#REF!' and c != '#DIV/0!']
                if non_empty:
                    print('  Row', row['row'], ':', ' | '.join(non_empty[:10]))
        print()
