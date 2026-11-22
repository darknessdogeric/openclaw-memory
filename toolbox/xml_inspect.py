import zipfile
import re

dst = 'D:/B166ER-OpenClaw/workspace/toolbox/test_minimal.xlsx'
with zipfile.ZipFile(dst, 'r') as z:
    sheet_xml = z.read('xl/worksheets/sheet1.xml').decode('utf-8')

# Find row 9
rows = re.findall(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_xml, re.DOTALL)
for row_num, row_content in rows:
    if int(row_num) == 9:
        print(f'=== Row {row_num} (full) ===')
        print(row_content[:2000])
        break