# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from collections import Counter
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部'
WS = 'D:\\B166ER-openclaw\\workspace'

F1 = os.path.join(DESK, '旗下酒店', '安逸直营酒店名录（17及32名录）_脱敏版_2026-11-04.xlsx')
F2 = os.path.join(DESK, '旗下酒店', '轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx')
F3 = os.path.join(DESK, '重要文件', '202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx')

def dump_headers(path, sheets):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    for sn in sheets:
        ws = wb[sn]
        print('=== ' + os.path.basename(path) + ' :: ' + sn + ' ===')
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i > 3:
                break
            c = [('' if x is None else str(x).strip().replace(chr(10), ' ')) for x in row]
            print('   H' + str(i) + ': ' + ' | '.join([str(j) + '=' + c[j][:22] for j in range(len(c)) if c[j]])[:400])
    wb.close()
    print('')

dump_headers(F1, ['直营酒店17家', '直营酒店32家（含26年闭店停业）'])
dump_headers(F2, ['管理名录', '到期单位'])
dump_headers(F3, ['自有资产', '已开业委托管理项目'])