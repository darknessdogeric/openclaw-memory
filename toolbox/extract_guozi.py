#!/usr/bin/env python3
"""Extract 国资要闻 PDF"""
import fitz
import sys

fp = r'C:\Users\ericz\Desktop\产业发展部\重要文件\《国资要闻》2026年-第8期.pdf'

doc = fitz.open(fp)
print(f'Pages: {len(doc)}', file=sys.stderr)
md = doc.metadata or {}
print(f'Title: {md.get("title", "")}', file=sys.stderr)
print(f'Author: {md.get("author", "")}', file=sys.stderr)
print(file=sys.stderr)

# Extract all text
all_text = []
for i, page in enumerate(doc):
    text = page.get_text()
    all_text.append(f'=== PAGE {i+1} ({len(text)} chars) ===\n{text}')

doc.close()

# Save full text to toolbox/.tmp
import os
out_dir = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\guozi_ynews_8'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'full_text.txt')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))
print(f'Saved {sum(len(t) for t in all_text)} chars to {out_path}', file=sys.stderr)

# Print first 3 pages to stdout
print('\n\n'.join(all_text[:3]))