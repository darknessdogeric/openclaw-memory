# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

def show(path, tag, hmax=30, tmax=46, bmax=14):
    print('=' * 96)
    print('【' + tag + '】')
    if not os.path.exists(path):
        print('  !! 缺失'); return
    t = open(path, encoding='utf-8', errors='replace').read()
    lines = t.split(chr(10))
    print('  长度 %d 字符 / %d 行' % (len(t), len(lines)))
    for h in [l for l in lines if l.strip().startswith('#')][:hmax]:
        print('   ' + h.strip()[:100])
    print('  --- 表格 ---')
    n = 0
    for l in lines:
        s = l.strip()
        if s.startswith('|'):
            print('   ' + s[:180]); n += 1
            if n >= tmax: break
    print('  --- 关键段落 ---')
    m = 0
    KEY = ['流程','步骤','阶段','阶段','标准','改造','轻','重','投资','审批','合规','招采','分工','界面','集团','单店','外部','合作方','工期','停业','分级','分类','基准','回收','拆','保留','新建','置换','客房数','翻牌','轻重']
    for l in lines:
        s = l.strip()
        if len(s) < 14 or s.startswith('#') or s.startswith('|') or s.startswith('>') or s.startswith('```'):
            continue
        if any(k in s for k in KEY):
            print('   * ' + s[:225]); m += 1
            if m >= bmax: break
    print()

show(os.path.join(KB, '05_方法论', '存量全服式酒店翻牌改造流程_KB_v1.0_2026-10-15.md'),
     '存量全服式酒店翻牌改造流程 KB v1.0', hmax=34, tmax=42, bmax=12)
show(os.path.join(KB, '05_轻重分离研究', '6大酒店改造_批次时序.md'),
     '6大酒店改造_批次时序', hmax=26, tmax=36, bmax=12)
show(os.path.join(KB, '00_全域商业市场认知', '01_酒店行业', '酒店分级分类基准参数体系_v2.0_2026-09-29.md'),
     '酒店分级分类基准参数体系 v2.0', hmax=26, tmax=40, bmax=10)
