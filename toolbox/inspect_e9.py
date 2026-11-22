"""检查 E9 完整属性 - 找出为什么变成 CTG!A1"""
import openpyxl
from openpyxl.utils import get_column_letter

# 原始备份
wb = openpyxl.load_workbook('D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx', data_only=False)
ws = wb['市场代码']

cell = ws['E9']
print('=== 原始 E9 完整属性 ===')
print(f'  coord: {cell.coordinate}')
print(f'  value: {cell.value!r}')
print(f'  data_type: {cell.data_type}')
print(f'  number_format: {cell.number_format!r}')
print(f'  is formula?: {cell.data_type == "f"}')

# Workbook 级 defined names
print()
print('=== Workbook defined names ===')
if hasattr(wb, 'defined_names'):
    print(f'  defined_names: {list(wb.defined_names)}')
    for name, defn in wb.defined_names.items():
        print(f'    {name}: {defn.value if hasattr(defn, "value") else defn}')

# 检查 external links / external references
print()
print('=== External links ===')
if hasattr(wb, '_external_links'):
    print(f'  _external_links: {wb._external_links}')

# 看周围几个单元格的值
print()
print('=== 周围单元格 (D9, E9, F9, G9, H9) ===')
for coord in ['D9', 'E9', 'F9', 'G9', 'H9']:
    c = ws[coord]
    print(f'  {coord}: value={c.value!r}, data_type={c.data_type}, font={c.font.name if c.font else None}')

# 检查 data_only=True 模式下, E9 的实际值
wb2 = openpyxl.load_workbook('D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx', data_only=True)
ws2 = wb2['市场代码']
cell2 = ws2['E9']
print()
print('=== 原始 E9 (data_only=True, 显示计算值) ===')
print(f'  value: {cell2.value!r}')
print(f'  data_type: {cell2.data_type}')