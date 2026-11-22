"""
删除 集团价格代码字典.xlsx 中的指定字串: 中旅/中国旅游/CTG/心享会
"""
import openpyxl
from collections import defaultdict

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'

# 替换顺序:先替换长的避免误伤(中旅、中国旅游会包含"旅"字,但不会包含"心享会")
# 但要注意:"心享会"包含"享","中旅集团"包含"中"和"旅"
# 安全顺序: 心享会 → 中国旅游 → CTG → 中旅
keywords = ['心享会', '中国旅游', 'CTG', '中旅']

wb = openpyxl.load_workbook(SRC)

change_log = []
total_replacements = 0

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                original = cell.value
                new_val = original
                for kw in keywords:
                    if kw in new_val:
                        new_val = new_val.replace(kw, '')
                if new_val != original:
                    cell.value = new_val
                    change_log.append((sheet_name, cell.coordinate, original, new_val))
                    total_replacements += 1

print(f'Total cells modified: {total_replacements}')
print()
print('=== 变更明细 ===')

by_sheet = defaultdict(list)
for s, c, o, n in change_log:
    by_sheet[s].append((c, o, n))

for sheet in sorted(by_sheet.keys()):
    print(f'\n--- [{sheet}] {len(by_sheet[sheet])} 处 ---')
    for c, o, n in by_sheet[sheet]:
        print(f'  {c}:')
        print(f'    OLD: {o!r}')
        print(f'    NEW: {n!r}')

# Save
wb.save(SRC)
print(f'\n[OK] Saved to: {SRC}')