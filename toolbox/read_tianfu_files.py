# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import docx

docx_files = [
    r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\省人大下属天府山庄考察报告.docx',
    r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\关于成都东部新区天府山庄资产及拟处置情况的汇报(20250613).docx',
]

for f in docx_files:
    print('\n' + '='*80)
    print('>>> ' + f.split('\\')[-1])
    print('='*80)
    try:
        d = docx.Document(f)
        for i, p in enumerate(d.paragraphs):
            if p.text.strip():
                print('[' + str(i).zfill(3) + '] ' + p.text)
        for ti, t in enumerate(d.tables):
            print('\n  [Table ' + str(ti) + '] rows=' + str(len(t.rows)) + ' cols=' + str(len(t.columns)))
            for ri, row in enumerate(t.rows):
                cells = [c.text.strip().replace(chr(10), ' / ')[:160] for c in row.cells]
                print('    R' + str(ri) + ': ' + ' | '.join(cells))
    except Exception as e:
        print('ERROR: ' + str(e))
