#!/usr/bin/env python3
"""OCR the 十五五规划修订稿 PDF (scanned)"""
import pypdfium2 as pdfium
import subprocess
import os
import sys
import time

PDF = r'C:\Users\ericz\Desktop\产业发展部\重要文件\安逸酒店集团十五五规划修订稿.pdf'
PAGES_DIR = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\15wu_pdf\pages'
OUT_DIR = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\15wu_pdf'
TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSDATA = os.path.expanduser(r'~\.tessdata')

os.makedirs(OUT_DIR, exist_ok=True)
os.environ['TESSDATA_PREFIX'] = TESSDATA

pdf_doc = pdfium.PdfDocument(PDF)
print(f'Pages: {len(pdf_doc)}', file=sys.stderr)

all_text = []
for i in range(len(pdf_doc)):
    img_path = os.path.join(PAGES_DIR, f'p{i+1:03d}.png')
    if not os.path.exists(img_path):
        page = pdf_doc[i]
        pil_image = page.render(scale=2.5).to_pil()
        pil_image.save(img_path)

    t0 = time.time()
    result = subprocess.run(
        [TESSERACT, img_path, os.path.join(OUT_DIR, f'p{i+1:03d}'), '-l', 'chi_sim+eng', '--psm', '6', '-c', 'preserve_interword_spaces=1'],
        capture_output=True, text=True, timeout=180
    )
    elapsed = time.time() - t0

    txt_path = os.path.join(OUT_DIR, f'p{i+1:03d}.txt')
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            page_text = f.read()
    else:
        page_text = f'[OCR FAILED: {result.stderr[:200]}]'

    all_text.append(f'=== PAGE {i+1} ({elapsed:.1f}s, {len(page_text)} chars) ===\n{page_text}')
    print(f'Page {i+1}: {elapsed:.1f}s, {len(page_text)} chars', file=sys.stderr)

pdf_doc.close()

combined_path = os.path.join(OUT_DIR, 'full_text.txt')
with open(combined_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

print(f'\nTotal: {sum(len(t) for t in all_text)} chars', file=sys.stderr)
print(f'Saved to: {combined_path}', file=sys.stderr)