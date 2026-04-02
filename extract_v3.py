# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\ericz\.openclaw\workspace\excel_data_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print all sheets for the budget template files
for item in data:
    fname = item['file']
    if any(x in fname for x in ['预算模板', 'Flash Report', 'P&L', '经营数据']):
        print('=' * 80)
        print('FILE:', fname)
        print('=' * 80)
        for sheet in item.get('sheets', []):
            print(f'\n--- Sheet: {sheet["name"]} ({sheet["max_row"]} rows) ---')
            for row in sheet['rows'][:40]:
                cells = row['cells']
                # Find non-empty cells
                non_empty = [(i, c) for i, c in enumerate(cells) if c and c != '#REF!']
                if non_empty:
                    print(f'  Row{row["row"]}: ' + ' | '.join(f'[{i}]{c[:40]}' for i, c in non_empty[:8]))
        print()
