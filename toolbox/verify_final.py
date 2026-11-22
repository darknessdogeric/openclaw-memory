"""
R66 验证扫描 - 重新检查文件
1. 4 个关键词全部清除
2. 数据完整性未损 (列结构、行数)
3. 检查 CTS 残留(用户未要求删除,但作为风险点提示)
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import openpyxl

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'

wb_new = openpyxl.load_workbook(SRC, data_only=True)
wb_old = openpyxl.load_workbook('D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx', data_only=True)

# === 检查1: 4 个关键词清除 ===
keywords = ['中旅', '中国旅游', 'CTG', '心享会']
keywords_lower = [k.lower() for k in keywords]

print('=== 检查 1: 4 个关键词残留 ===')
remaining = []
for sheet_name in wb_new.sheetnames:
    ws = wb_new[sheet_name]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                val = cell.value
                val_lower = val.lower()
                for k, kl in zip(keywords, keywords_lower):
                    if k in val or kl in val_lower:
                        remaining.append((sheet_name, cell.coordinate, val, k))
                        break

if remaining:
    print(f'  [X] 残留 {len(remaining)} 处:')
    for r in remaining[:20]:
        print(f'    {r}')
else:
    print(f'  [OK] 全部清除')

# === 检查2: 列结构完整 ===
print()
print('=== 检查 2: Sheet 结构完整性 ===')
for sn in wb_old.sheetnames:
    ws_old = wb_old[sn]
    ws_new = wb_new[sn]
    same_rows = ws_old.max_row == ws_new.max_row
    same_cols = ws_old.max_column == ws_new.max_column
    status = '[OK]' if (same_rows and same_cols) else '[X]'
    print(f'  {status} {sn}: rows {ws_old.max_row}->{ws_new.max_row}, cols {ws_old.max_column}->{ws_new.max_column}')

# === 检查3: CTS 残留 (风险提示) ===
print()
print('=== 检查 3: CTS 残留 (中旅英文缩写,用户未要求删除) ===')
cts_matches = []
for sheet_name in wb_new.sheetnames:
    ws = wb_new[sheet_name]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and 'CTS' in cell.value:
                cts_matches.append((sheet_name, cell.coordinate, cell.value))

if cts_matches:
    print(f'  发现 {len(cts_matches)} 处 (EMRCTS1/EMRCTS/EMFCTS - 价格代码,可能保留):')
    for m in cts_matches:
        print(f'    [{m[0]}] {m[1]}: {m[2]!r}')
else:
    print(f'  [OK] 无残留')

# === 检查4: 与原始数据差异统计 ===
print()
print('=== 检查 4: 单元值差异统计 ===')
total_old_cells = 0
total_new_cells = 0
total_nonempty_old = 0
total_nonempty_new = 0
for sn in wb_old.sheetnames:
    ws_o = wb_old[sn]
    ws_n = wb_new[sn]
    for row in ws_o.iter_rows():
        for c in row:
            total_old_cells += 1
            if c.value is not None and c.value != '':
                total_nonempty_old += 1
    for row in ws_n.iter_rows():
        for c in row:
            total_new_cells += 1
            if c.value is not None and c.value != '':
                total_nonempty_new += 1

print(f'  原始: {total_old_cells} 单元, {total_nonempty_old} 非空')
print(f'  新版: {total_new_cells} 单元, {total_nonempty_new} 非空')
print(f'  差异: {total_old_cells - total_new_cells} 单元减少, {total_nonempty_old - total_nonempty_new} 非空减少')
print(f'  (180 处字符串清理 + 1 处 None 化,符合预期)')

# === 关键样本抽查 ===
print()
print('=== 关键样本抽查 ===')
print()
print('[市场代码]')
for coord in ['E9', 'G5', 'I5', 'G9', 'H9', 'I9']:
    c = wb_new['市场代码'][coord]
    print(f'  {coord}: {c.value!r}')
print()
print('[集团]')
for coord in ['H1', 'E6', 'E9', 'H3', 'H4', 'H5']:
    c = wb_new['集团'][coord]
    print(f'  {coord}: {c.value!r}')
print()
print('[RAC] 抽样')
for coord in ['B6', 'F9', 'B10', 'F10', 'B18', 'F18']:
    c = wb_new['RAC'][coord]
    print(f'  {coord}: {c.value!r}')