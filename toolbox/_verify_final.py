# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

DESK = r'C:\Users\ericz\Desktop'
files = sorted(x for x in glob.glob(os.path.join(DESK, '*战略合作框架协议_合并稿_*.docx'))
               if not os.path.basename(x).startswith('~$'))

MUST_ABSENT = ['收入分配方式为9:1', '原告所在地', '设置（）小时免费权益方案',
               '不再与其他第三方', '排他', '独家', '有效期一年',
               '乙方：美团（XXXX）', '（专属约定）', '具体以双方约定为准']
MUST_PRESENT = ['天津三快信息技术有限公司',
                '不约定具体执行细则、点位数量、收益分成',
                '显示甲方会员入口',
                '乙方应支持甲方会员积分体系',
                '甲方对所提供的标识纹样及设计图案享有知识产权',
                '第四条 数据与会员',
                '本框架协议合作期限：3年',
                '提交甲方所在地人民法院诉讼解决',
                '经甲方审核同意后方可变更',
                '组建联合工作小组']
# 解析器残留：正文不应出现字面量标签
JUNK = ['B 甲方', 'B 乙方', 'B 统一', 'B 地址', 'B 联系', 'B 法定', 'B 日期',
        '2 一、甲方', '2 二、乙方', 'NB ']

for fp in files:
    print('=' * 72)
    print(os.path.basename(fp))
    print('=' * 72)
    d = Document(fp)
    f = ''.join(x.text for x in d.paragraphs)
    print('段落 %d  字数 %d' % (len(d.paragraphs), len(f)))
    bad = 0
    for k in MUST_ABSENT:
        if k in f:
            bad += 1
            print('  [应无] %-32s *** 仍存在 ***' % k)
    for k in MUST_PRESENT:
        if k not in f:
            bad += 1
            print('  [应有] %-32s *** 缺失 ***' % k)
    for k in JUNK:
        if k in f:
            bad += 1
            print('  [无残渣] %-30s *** 仍存在 ***' % k)
    print('  FAIL COUNT =', bad)
    print('  首部: %s / %s' % (d.paragraphs[0].text.strip()[:40], d.paragraphs[1].text.strip()[:30]))
    print('  标题段落抽样:')
    for i in (2, 8, 14, 18, 19, 23, 24, 31, 32, 33, 37, 42, 46, 50, 54, 56):
        if i < len(d.paragraphs):
            t = d.paragraphs[i].text.strip()
            if t:
                print('    p%-3d %s' % (i, t[:64]))
    print()
