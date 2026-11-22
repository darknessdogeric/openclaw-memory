# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from pypdf import PdfReader
except ImportError:
    print("Need pypdf")
    sys.exit(1)

pdf_files = [
    r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\天府山庄房产证1.pdf',
    r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\天府山庄房产证2.pdf',
    r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\天府山庄土地证.pdf',
]

for f in pdf_files:
    print('\n' + '='*80)
    print('>>> ' + f.split('\\')[-1])
    print('='*80)
    try:
        r = PdfReader(f)
        for pi, p in enumerate(r.pages):
            t = p.extract_text() or ''
            if t.strip():
                print('--- Page ' + str(pi+1) + '/' + str(len(r.pages)) + ' ---')
                print(t[:3000])
    except Exception as e:
        print('ERROR: ' + str(e))
