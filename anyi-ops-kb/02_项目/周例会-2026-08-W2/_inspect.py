import os
import sys
from docx import Document

folder = r'C:\Users\ericz\Desktop\产业发展部\周例会内容'
out_folder = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\02_项目\周例会-2026-08-W2'
os.makedirs(out_folder, exist_ok=True)


def cell_text(cell):
    # 单元格包含多段落
    return ' / '.join([p.text.strip() for p in cell.paragraphs if p.text.strip()])


def extract_doc(full):
    doc = Document(full)
    lines = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            lines.append(t)
    for ti, tbl in enumerate(doc.tables):
        for ri, row in enumerate(tbl.rows):
            cells = [cell_text(c) for c in row.cells]
            cells = [c for c in cells if c]
            if cells:
                lines.append('[' + str(ti) + '.' + str(ri) + '] ' + ' | '.join(cells))
    return lines


def inspect(full):
    doc = Document(full)
    lines = []
    lines.append('---PARAGRAPHS---')
    for p in doc.paragraphs:
        if p.text.strip():
            lines.append(p.text[:200])
    lines.append('---TABLES---')
    for ti, tbl in enumerate(doc.tables):
        for ri, row in enumerate(tbl.rows):
            cells = [cell_text(c) for c in row.cells]
            cells = [c for c in cells if c]
            if cells:
                lines.append('[' + str(ti) + '.' + str(ri) + '] ' + ' | '.join(cells)[:300])
    return lines


files = sorted([f for f in os.listdir(folder) if f.lower().endswith('.docx')])
mode = sys.argv[1] if len(sys.argv) > 1 else 'extract'

for f in files:
    full = os.path.join(folder, f)
    name = os.path.splitext(f)[0]
    out_path = os.path.join(out_folder, name + '.txt')
    try:
        if mode == 'inspect':
            lines = inspect(full)
        else:
            lines = extract_doc(full)
        with open(out_path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))
        print(f'{f[:30]:30s} {len(lines):4d} lines  -> {os.path.basename(out_path)}')
    except Exception as e:
        print(f'ERR {f}: {e}')
