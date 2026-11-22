"""
删除 集团价格代码字典.xlsx 中的指定字串: 中旅/中国旅游/CTG/心享会
v2 - 修复 openpyxl bug: 空字符串 fallback 显示 'CTG!A1'
    改为:替换后若值为空,设为 None(真·清空)
"""
import openpyxl
from collections import defaultdict

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'

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
                    # 如果替换后是空字符串 → 设为 None(避免 openpyxl fallback bug)
                    if new_val == '':
                        cell.value = None
                        log_new = '<None>'
                    else:
                        cell.value = new_val
                        log_new = new_val
                    change_log.append((sheet_name, cell.coordinate, original, log_new))
                    total_replacements += 1

print(f'Total cells modified: {total_replacements}')
print()

# 简洁变更报告:按 sheet 统计
by_sheet = defaultdict(int)
empty_after = []
for s, c, o, n in change_log:
    by_sheet[s] += 1
    if n == '<None>':
        empty_after.append((s, c, o))

print('=== 变更分布 ===')
for sheet in sorted(by_sheet.keys(), key=lambda s: -by_sheet[s]):
    print(f'  {sheet}: {by_sheet[sheet]} 处')

print()
print('=== 清空(None)的单元格 ===')
for s, c, o in empty_after:
    print(f'  [{s}] {c}: {o!r} → None')

wb.save(SRC)
print(f'\n[OK] Saved to: {SRC}')