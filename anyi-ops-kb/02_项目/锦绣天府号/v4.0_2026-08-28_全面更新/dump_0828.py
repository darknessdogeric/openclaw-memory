import docx, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PATH = r"C:\Users\ericz\Desktop\产业发展部\熊猫专列\安逸-铁路成都局-心已远-锦绣天府号经营转委确认书（三方）0828.docx"
d = docx.Document(PATH)
print(f'=== 0828 转委确认书 全文打印 ===')
print(f'段落数: {len(d.paragraphs)}, 表格数: {len(d.tables)}')
print('---')
for i, p in enumerate(d.paragraphs):
    if p.text.strip():
        print(f'[P{i:02d}] {p.text}')
print('---')
print('=== Tables ===')
for i, t in enumerate(d.tables):
    print(f'--- Table {i} ---')
    for r in t.rows:
        print(' | '.join(c.text for c in r.cells))