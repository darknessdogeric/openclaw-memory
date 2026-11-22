"""
完整清理 v3:
- 删除 中旅/中国旅游/CTG/心享会/CTS
- 对所有变更过的单元格:trim + collapse multi-spaces (英文描述里的副作用清理)
- 空字符串 → None (避免 openpyxl fallback bug)
"""
import openpyxl
import re
from collections import defaultdict

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'

# 第一步:字串替换
keywords = ['心享会', '中国旅游', 'CTG', '中旅', 'CTS']

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
                    # === 副作用清理 ===
                    # 1. 连续 2+ 空格 → 单空格
                    new_val = re.sub(r' {2,}', ' ', new_val)
                    # 2. trim 首尾空格
                    new_val = new_val.strip()

                    # 空字符串 → None (避免 openpyxl 'inlineStr' fallback bug)
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

# 统计
by_sheet = defaultdict(int)
empty_after = []
space_cleanup_count = 0  # 经过空格清理的(有空格副作用)
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
    print(f'  [{s}] {c}: {o!r}')

# 找出"经过空格清理"的样例 (原值有 2+ 空格 或 首尾空格)
print()
print('=== 空格副作用清理样例 ===')
seen = set()
for s, c, o, n in change_log:
    if n == '<None>':
        continue
    if o != o.strip() or '  ' in o:
        key = (s, c, o, n)
        if key not in seen:
            seen.add(key)
            print(f'  [{s}] {c}:')
            print(f'    OLD: {o!r}')
            print(f'    NEW: {n!r}')

wb.save(SRC)
print(f'\n[OK] Saved to: {SRC}')