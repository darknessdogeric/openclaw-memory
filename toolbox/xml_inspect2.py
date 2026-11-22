"""看 sheet1.xml 当前 E9 实际写了什么"""
import zipfile
import re

SRC = 'C:/Users/ericz/Desktop/产业发展部/外部相关资料/集团价格代码字典.xlsx'

with zipfile.ZipFile(SRC, 'r') as z:
    sheet_xml = z.read('xl/worksheets/sheet1.xml').decode('utf-8')

# Find row 9
rows = re.findall(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_xml, re.DOTALL)
for row_num, row_content in rows:
    if int(row_num) == 9:
        print(f'=== Row {row_num} (full) ===')
        print(row_content)
        break

# Also show all of sheet1.xml for E9 area
print()
print('=== Search E9 anywhere ===')
e9_matches = re.findall(r'(<c r="E9"[^>]*?(?:/>|>.*?</c>))', sheet_xml, re.DOTALL)
for m in e9_matches:
    print(m)