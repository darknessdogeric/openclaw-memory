# -*- coding: utf-8 -*-
# 提取外部相关资料（脱敏元素用）
import os
import openpyxl
from pptx import Presentation
import pdfplumber

root = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
dst_root = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\01_集团文件\_report_materials'
os.makedirs(dst_root, exist_ok=True)

out = []

# xlsx
for f in os.listdir(root):
    if not f.endswith('.xlsx'):
        continue
    try:
        wb = openpyxl.load_workbook(os.path.join(root, f), data_only=True)
        txt = [f'=== {f} ===', f'Sheets: {wb.sheetnames}']
        for sn in wb.sheetnames:
            ws = wb[sn]
            txt.append(f'\n--- Sheet: {sn} ({ws.max_row}r x {ws.max_column}c) ---')
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                vals = [str(c).strip() for c in row if c is not None]
                if vals:
                    txt.append(f'R{row_idx}: ' + ' | '.join(vals)[:300])
                if row_idx >= 25:
                    txt.append('...(截断)')
                    break
        out.append('\n'.join(txt))
    except Exception as e:
        out.append(f'=== {f} === ERROR: {e}')

# pptx
for f in os.listdir(root):
    if not f.endswith('.pptx'):
        continue
    try:
        prs = Presentation(os.path.join(root, f))
        txt = [f'=== {f} === (slides: {len(prs.slides)})']
        for idx, slide in enumerate(prs.slides, 1):
            st = []
            for shape in slide.shapes:
                if hasattr(shape, 'text') and shape.text:
                    st.append(shape.text)
            if st:
                txt.append(f'--- Slide {idx} ---')
                txt.append('\n'.join(st)[:600])
        out.append('\n'.join(txt))
    except Exception as e:
        out.append(f'=== {f} === ERROR: {e}')

# pdf
for f in os.listdir(root):
    if not f.endswith('.pdf'):
        continue
    try:
        with pdfplumber.open(os.path.join(root, f)) as pdf:
            txt = [f'=== {f} === (pages: {len(pdf.pages)})']
            for i, page in enumerate(pdf.pages[:8], 1):
                t = page.extract_text() or ''
                if t.strip():
                    txt.append(f'--- P{i} ---')
                    txt.append(t[:600])
        out.append('\n'.join(txt))
    except Exception as e:
        out.append(f'=== {f} === ERROR: {e}')

with open(os.path.join(dst_root, '外部相关资料_提取.txt'), 'w', encoding='utf-8') as f:
    f.write('\n\n' + '='*80 + '\n\n'.join(out))

print(f'提取完成，共 {len(out)} 份文件')
print(f'总大小: {os.path.getsize(os.path.join(dst_root, "外部相关资料_提取.txt"))} bytes')
