# -*- coding: utf-8 -*-
# 提取 715 定稿 + 3 份酒店调研 + 外部相关资料
import os
import pdfplumber
import fitz
from pptx import Presentation

dst_root = r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\01_集团文件\_report_materials'
os.makedirs(dst_root, exist_ok=True)

def extract_pdf(src, dst):
    text_parts = []
    page_count = 0
    # 先试 pdfplumber 文字
    try:
        with pdfplumber.open(src) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                t = page.extract_text() or ''
                if t.strip():
                    text_parts.append(t)
    except Exception as e:
        pass
    full = '\n\n--- [PAGE BREAK] ---\n\n'.join(text_parts)
    # 如果文字太少，用 PyMuPDF 再试
    if len(full) < 500:
        try:
            doc = fitz.open(src)
            text_parts2 = []
            for p in doc:
                t = p.get_text() or ''
                if t.strip():
                    text_parts2.append(t)
            doc.close()
            full2 = '\n\n--- [PAGE BREAK] ---\n\n'.join(text_parts2)
            if len(full2) > len(full):
                full = full2
                page_count = len(text_parts2)
        except Exception:
            pass
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(full)
    return len(full), page_count

# 715 定稿
r = extract_pdf(r'C:\Users\ericz\Desktop\产业发展部\安逸酒店集团改革发展工作专题汇报材料（715定稿）.pdf',
                os.path.join(dst_root, '715定稿.txt'))
print(f'[715定稿] {r[0]} chars / {r[1]} pages')

# 3 份酒店调研
for name in ['都江堰国堰宾馆考察调研会议纪要0810', '安逸花园宾馆考察调研会议纪要0813', '乐山锦江嘉州宾馆考察调研会议纪要0813']:
    r = extract_pdf(rf'C:\Users\ericz\Desktop\产业发展部\酒店调研\{name}.pdf',
                    os.path.join(dst_root, f'{name}.txt'))
    print(f'[{name}] {r[0]} chars / {r[1]} pages')

print('\nDONE')
