"""最终验证 v3"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import openpyxl

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'
wb = openpyxl.load_workbook(SRC, data_only=True)

# === 1. 5 关键词清除验证 ===
print('=== 检查 1: 5 个关键词残留 ===')
keywords = ['中旅', '中国旅游', 'CTG', '心享会', 'CTS']
keywords_lower = [k.lower() for k in keywords]
remaining = []
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
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
    for r in remaining:
        print(f'    {r}')
else:
    print(f'  [OK] 全部清除')

# === 2. 空格副作用清理验证 ===
print()
print('=== 检查 2: 空格副作用 ===')
space_issues = []
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                v = cell.value
                # 末尾空格 / 开头空格 / 多空格
                if v != v.strip() or '  ' in v:
                    space_issues.append((sheet_name, cell.coordinate, v))

if space_issues:
    print(f'  [X] 发现 {len(space_issues)} 处空格问题:')
    for sn, c, v in space_issues[:20]:
        print(f'    [{sn}] {c}: {v!r}')
else:
    print(f'  [OK] 无空格问题')

# === 3. 关键样本抽查 ===
print()
print('=== 检查 3: 关键样本 ===')
print()
print('[市场代码] (含 CTS 英文副作用)')
for coord in ['E9', 'G5', 'I5', 'G9', 'H9', 'I9']:
    c = wb['市场代码'][coord]
    print(f'  {coord}: {c.value!r}')
print()
print('[集团] (含 CTS 价格代码)')
for coord in ['H1', 'E6', 'E9', 'H3', 'H4', 'H5']:
    c = wb['集团'][coord]
    print(f'  {coord}: {c.value!r}')
print()
print('[RAC] 抽样')
for coord in ['B6', 'F9', 'B10', 'F10', 'B18', 'F18']:
    c = wb['RAC'][coord]
    print(f'  {coord}: {c.value!r}')

# === 4. 用 pandas 独立验证 (避免 openpyxl bug 干扰) ===
print()
print('=== 检查 4: pandas 独立验证 ===')
import pandas as pd
df = pd.read_excel(SRC, sheet_name='市场代码', header=None)
print(f'  pandas 市场代码 E9 (idx [8,4]): {df.iloc[8,4]!r}')
print(f'  pandas 市场代码 G5 (idx [4,6]): {df.iloc[4,6]!r}')
print(f'  pandas 市场代码 I5 (idx [4,8]): {df.iloc[4,8]!r}')

df_grp = pd.read_excel(SRC, sheet_name='集团', header=None)
print(f'  pandas 集团 H1 (idx [0,7]): {df_grp.iloc[0,7]!r}')
print(f'  pandas 集团 H3 (idx [2,7]): {df_grp.iloc[2,7]!r}')
print(f'  pandas 集团 H4 (idx [3,7]): {df_grp.iloc[3,7]!r}')
print(f'  pandas 集团 H5 (idx [4,7]): {df_grp.iloc[4,7]!r}')