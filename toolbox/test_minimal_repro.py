"""
最小复现测试:只修改 E9 一个单元格(CTG → '')
看是否复现 'CTG!A1' 问题
"""
import openpyxl
import shutil

src = 'D:/B166ER-OpenClaw/workspace/memory/backups/集团价格代码字典_原始备份_20260818.xlsx'
dst = 'D:/B166ER-OpenClaw/workspace/toolbox/test_minimal.xlsx'
shutil.copy2(src, dst)

wb = openpyxl.load_workbook(dst)
ws = wb['市场代码']

print('=== 修改前 E9 ===')
cell = ws['E9']
print(f'  value: {cell.value!r}')
print(f'  data_type: {cell.data_type}')

# 直接修改
cell.value = ''

print()
print('=== 修改后(内存中)E9 ===')
print(f'  value: {cell.value!r}')
print(f'  data_type: {cell.data_type}')

# 保存
wb.save(dst)

# 重新读取验证
wb2 = openpyxl.load_workbook(dst)
ws2 = wb2['市场代码']
cell2 = ws2['E9']
print()
print('=== 保存后重新读取 E9 ===')
print(f'  value: {cell2.value!r}')
print(f'  data_type: {cell2.data_type}')

# 顺便看共享字符串表 (sharedStrings)
import zipfile
print()
print('=== xlsx 包内容 ===')
with zipfile.ZipFile(dst, 'r') as z:
    print(f'  files: {z.namelist()}')
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            # 找 CTG
            for line in content.split('\n'):
                if 'CTG' in line or 'CTG!A1' in line or '!A1' in line:
                    print(f'  sharedStrings line: {line.strip()[:200]}')

# 看 sheet1 的 raw xml
with zipfile.ZipFile(dst, 'r') as z:
    sheet_xml = z.read('xl/worksheets/sheet1.xml').decode('utf-8')
    # 找 E9
    import re
    # E9 = 第 9 行, 第 5 列 (E 是第5列)
    # 在 Excel 内部, E9 用 r="E9" 表示
    matches = re.findall(r'<c r="E9"[^>]*>(.*?)</c>', sheet_xml, re.DOTALL)
    print()
    print('=== sheet1.xml 中 E9 的 XML ===')
    for m in matches:
        print(f'  {m[:300]}')