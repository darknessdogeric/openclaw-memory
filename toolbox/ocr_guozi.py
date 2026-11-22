#!/usr/bin/env python3
"""OCR the国资要闻 PDF"""
import fitz
import subprocess
import os
import sys
import time

PDF = r'C:\Users\ericz\Desktop\产业发展部\重要文件\《国资要闻》2026年-第8期.pdf'
OUT_DIR = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\guozi_ynews_8'
TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSDATA = os.path.expanduser(r'~\.tessdata')

os.makedirs(OUT_DIR, exist_ok=True)
os.environ['TESSDATA_PREFIX'] = TESSDATA

doc = fitz.open(PDF)
print(f'Pages: {len(doc)}', file=sys.stderr)

all_text = []
for i, page in enumerate(doc):
    # Render page to image at 200 DPI
    pix = page.get_pixmap(dpi=200)
    img_path = os.path.join(OUT_DIR, f'page_{i+1:02d}.png')
    pix.save(img_path)

    # Run tesseract OCR (Chinese simplified + English)
    t0 = time.time()
    result = subprocess.run(
        [TESSERACT, img_path, os.path.join(OUT_DIR, f'page_{i+1:02d}'), '-l', 'chi_sim+eng', '--psm', '6', '-c', 'preserve_interword_spaces=1'],
        capture_output=True, text=True, timeout=120
    )
    elapsed = time.time() - t0

    txt_path = os.path.join(OUT_DIR, f'page_{i+1:02d}.txt')
    if os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            page_text = f.read()
    else:
        page_text = f'[OCR FAILED: {result.stderr}]'

    all_text.append(f'=== PAGE {i+1} ({elapsed:.1f}s, {len(page_text)} chars) ===\n{page_text}')
    print(f'Page {i+1}: {elapsed:.1f}s, {len(page_text)} chars', file=sys.stderr)

doc.close()

# Save combined
combined_path = os.path.join(OUT_DIR, 'full_text.txt')
with open(combined_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

print(f'\nTotal: {sum(len(t) for t in all_text)} chars', file=sys.stderr)
print(f'Saved to: {combined_path}', file=sys.stderr)