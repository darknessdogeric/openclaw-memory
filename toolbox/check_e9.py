"""检查 E9 单元格(原始 vs 修改后)"""
import openpyxl

# 修改后
wb_new = openpyxl.load_workbook('C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx', data_only=False)
ws_new = wb_new['市场代码']
cell_new = ws_new['E9']
print('=== 修改后 E9 (data_only=False) ===')
print(f'  value: {cell_new.value!r}')
print(f'  data_type: {cell_new.data_type}')

# 原始 - 两种模式
wb_old = openpyxl.load_workbook('D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx', data_only=False)
ws_old = wb_old['市场代码']
cell_old = ws_old['E9']
print()
print('=== 原始 E9 (data_only=False) ===')
print(f'  value: {cell_old.value!r}')
print(f'  data_type: {cell_old.data_type}')

wb_old2 = openpyxl.load_workbook('D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx', data_only=True)
ws_old2 = wb_old2['市场代码']
cell_old2 = ws_old2['E9']
print()
print('=== 原始 E9 (data_only=True) ===')
print(f'  value: {cell_old2.value!r}')
print(f'  data_type: {cell_old2.data_type}')