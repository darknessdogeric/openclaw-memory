# -*- coding: utf-8 -*-
import fitz
import os

desktop = r'C:\Users\ericz\Desktop'
pdf_file = None
for f in os.listdir(desktop):
    if 'AHL' in f and 'V6.0' in f and f.endswith('.pdf'):
        pdf_file = os.path.join(desktop, f)
        break

if pdf_file:
    print(f"Reading: {pdf_file}")
    doc = fitz.open(pdf_file)
    print(f"Total pages: {len(doc)}")
    
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            lines = text.split('\n')
            title_lines = [l.strip() for l in lines if l.strip() and len(l.strip()) < 80][:5]
            if title_lines:
                print(f"P{i+1}: {' | '.join(title_lines[:3])}")
else:
    print("No PDF found")
