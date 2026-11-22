from docx import Document
import os

desktop = r'C:\Users\ericz\Desktop'

# 列出所有相关 doc
print('=== All .doc files on Desktop (matching keywords) ===')
candidates = []
for f in os.listdir(desktop):
    if f.endswith('.doc') and ('十五五' in f or '研讨' in f or '规划' in f or '安逸' in f):
        candidates.append(f)

print(f'Candidates: {len(candidates)}')
for f in candidates:
    print(' ', repr(f))

# 选第一个（按 Eric 描述就是它）
if not candidates:
    print('No matching file. All .doc files on Desktop:')
    for f in sorted(os.listdir(desktop)):
        if f.endswith('.doc'):
            print(' ', repr(f), os.path.getsize(os.path.join(desktop, f)), 'bytes')
    raise SystemExit(1)

target = candidates[0]
path = os.path.join(desktop, target)
print(f'\n=== TARGET FILE ===')
print('Path:', path)
print('Size:', os.path.getsize(path), 'bytes')

doc = Document(path)
print(f'TOTAL PARAGRAPHS: {len(doc.paragraphs)}')
print(f'TOTAL TABLES: {len(doc.tables)}')
print('=' * 70)
print('FULL CONTENT:')
print('=' * 70)
for i, para in enumerate(doc.paragraphs):
    if para.text.strip():
        print(f'[{i:02d}] {para.text}')
print('=' * 70)
print('TABLES:')
for ti, table in enumerate(doc.tables):
    print(f'--- Table {ti} ({len(table.rows)}x{len(table.columns)}) ---')
    for ri, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        print(f'  Row {ri}: {" | ".join(cells)}')
