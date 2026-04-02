# -*- coding: utf-8 -*-
import json

with open(r'C:\Users\ericz\.openclaw\workspace\excel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print summary of each file
for item in data:
    print('File:', item['file'])
    if 'error' in item:
        print('  ERROR:', item['error'])
    else:
        print('  Sheets:', item.get('sheet_names', []))
        for sheet in item.get('sheets', []):
            print(f'    Sheet: {sheet["name"]} ({sheet["max_row"]} rows x {sheet["max_col"]} cols)')
            if sheet['rows']:
                print('    First row:', sheet['rows'][0]['cells'][:6])
                if len(sheet['rows']) > 1:
                    print('    Second row:', sheet['rows'][1]['cells'][:6])
    print()
