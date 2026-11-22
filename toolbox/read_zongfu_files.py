# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import docx

docx_files = [
    r'C:\Users\ericz\Desktop\安逸酒店集团关于总府四川宾馆自投自营与对外租赁经营模式对比分析报告(3).docx',
    r'C:\Users\ericz\Desktop\关于召开总府皇冠假日酒店重大安全隐患排险处置工作事项专题会的通知.doc',
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
                cells = [c.text.strip().replace(chr(10), ' / ')[:180] for c in row.cells]
                print('    R' + str(ri) + ': ' + ' | '.join(cells))
    except Exception as e:
        print('ERROR: ' + str(e))
