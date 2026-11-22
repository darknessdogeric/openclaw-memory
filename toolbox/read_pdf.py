#!/usr/bin/env python3
"""读取 PDF 调研纪要"""
from pypdf import PdfReader
import os

pdf_dir = r"C:\Users\ericz\Desktop\产业发展部\酒店调研"
pdfs = [
    "都江堰国堰宾馆考察调研会议纪要0810.pdf",
    "安逸花园宾馆考察调研会议纪要0813.pdf",
    "乐山锦江嘉州宾馆考察调研会议纪要0813.pdf",
]

for fn in pdfs:
    path = os.path.join(pdf_dir, fn)
    if not os.path.exists(path):
        print(f"### NOT FOUND: {fn}")
        continue
    print(f"\n{'='*80}\n### FILE: {fn}\n{'='*80}")
    try:
        reader = PdfReader(path)
        for i, page in enumerate(reader.pages):
            print(f"\n--- PAGE {i+1} ---")
            text = page.extract_text()
            if text:
                print(text)
    except Exception as e:
        print(f"ERROR: {e}")