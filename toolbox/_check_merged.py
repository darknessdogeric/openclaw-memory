# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

cands = [x for x in glob.glob(r'C:\Users\ericz\Desktop\*战略合作框架协议_合并稿_*.docx')
         if not os.path.basename(x).startswith('~$')]
M = cands[0]
print('FILE:', M)
d = Document(M)
f = ''.join(x.text for x in d.paragraphs)

print()
print('=== 合并稿全文 ===')
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    print('%2d | %s' % (i, t if t else '(空)'))

print()
print('=== 修正后的校验 ===')
must_absent = [
    '收入分配方式为9:1',
    '原告所在地',
    '设置（）小时免费权益方案',
    '不再与其他第三方',
    '排他',
    '独家',
    '有效期一年',
    '乙方：美团（XXXX）',
    '（专属约定）',
    '具体以双方约定为准',
]
must_present = [
    '天津三快信息技术有限公司',
    '不约定具体执行细则、点位数量、收益分成',
    '显示甲方会员入口',
    '乙方应支持甲方会员积分体系',
    '甲方对所提供的标识纹样及设计图案享有知识产权',
    '第四条 数据与会员',
    '本框架协议合作期限：3年',
    '提交甲方所在地人民法院诉讼解决',
    '经甲方审核同意后方可变更',
    '组建联合工作小组',
]
bad = 0
for k in must_absent:
    ok = k not in f
    if not ok:
        bad += 1
    print('  [应无] %-30s %s' % (k, 'OK' if ok else '*** 仍存在 ***'))
for k in must_present:
    ok = k in f
    if not ok:
        bad += 1
    print('  [应有] %-30s %s' % (k, 'OK' if ok else '*** 缺失 ***'))
print()
print('FAIL COUNT =', bad)
print('段落 %d  字数 %d' % (len(d.paragraphs), len(f)))
