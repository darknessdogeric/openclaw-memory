"""Read all 3 安逸茶山 files."""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r'C:\Users\ericz\Desktop\安逸茶山'

# 1. DOCX
docx_path = os.path.join(base, '安逸美舍简介.docx')
try:
    import docx
    d = docx.Document(docx_path)
    print('=== 安逸美舍简介.docx ===')
    for i, p in enumerate(d.paragraphs):
        if p.text.strip():
            print(f'  [{i:02d}] {p.text}')
    print()
    # tables
    for ti, t in enumerate(d.tables):
        print(f'  -- TABLE {ti} --')
        for ri, row in enumerate(t.rows):
            cells = ' | '.join(c.text.strip() for c in row.cells)
            print(f'    R{ri}: {cells}')
    print()
except Exception as e:
    print('DOCX ERROR:', e)
    print()

# 2. PDF
pdf_path = os.path.join(base, '企业介绍-四川蒙顶山茶业有限公司.pdf')
try:
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    print('=== 蒙顶山茶业 PDF ===')
    print(f'Pages: {len(r.pages)}')
    for i, page in enumerate(r.pages):
        txt = page.extract_text() or ''
        print(f'--- Page {i+1} ({len(txt)} chars) ---')
        print(txt[:1800])
        print()
except Exception as e:
    print('PDF ERROR:', e)
    print()

# 3. PPTX
pptx_path = os.path.join(base, '250306安逸茶山康养休生谷项目汇报PPT(修)(3).pptx')
try:
    from pptx import Presentation
    prs = Presentation(pptx_path)
    print('=== PPTX ===')
    print(f'Slides: {len(prs.slides)}')
    for si, slide in enumerate(prs.slides):
        print(f'--- Slide {si+1} ---')
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    txt = ''.join(r.text for r in para.runs)
                    if txt.strip():
                        print(f'  | {txt}')
            elif shape.shape_type == 19 or 'table' in str(shape.shape_type).lower() or shape.has_table:
                if hasattr(shape, 'has_table') and shape.has_table:
                    for ri, row in enumerate(shape.table.rows):
                        cells = ' | '.join(c.text.strip() for c in row.cells)
                        print(f'  T R{ri}: {cells}')
except Exception as e:
    print('PPTX ERROR:', e)