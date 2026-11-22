# -*- coding: utf-8 -*-
import io, sys, os, re, gzip, urllib.request, urllib.parse, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

def show(path, tag, hmax=40, tmax=40, bmax=12, start=0):
    print('=' * 96)
    print('【' + tag + '】')
    if not os.path.exists(path):
        print('  !! 缺失'); return
    t = open(path, encoding='utf-8', errors='replace').read()
    lines = t.split(chr(10))
    print('  长度 %d 字符 / %d 行' % (len(t), len(lines)))
    for h in [l for l in lines if l.strip().startswith('#')][start:start + hmax]:
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
    KEY = ['施工','采购','招标','分包','验收','工期','爬坡','运营','风险','责任','分工','界面','外部','合作方','监理','变更','签证','合规','阶段','节点','不停业','分区','标准','模版','模板','一次','复用','审批','立项']
    for l in lines:
        s = l.strip()
        if len(s) < 14 or s.startswith('#') or s.startswith('|') or s.startswith('>') or s.startswith('```'):
            continue
        if any(k in s for k in KEY):
            print('   * ' + s[:225]); m += 1
            if m >= bmax: break
    print()

# 翻牌改造流程 KB 后半段
show(os.path.join(KB, '05_方法论', '存量全服式酒店翻牌改造流程_KB_v1.0_2026-10-15.md'),
     '翻牌改造流程KB v1.0 — 后半段(模块5-10)', hmax=40, tmax=34, bmax=14)

# 一企一策范式
show(os.path.join(KB, '04_方法论', '一企一策分析范式_v1.0_2026-11-11.md'),
     '一企一策分析范式 v1.0', hmax=26, tmax=26, bmax=10)

# 3方向决策框架
show(os.path.join(KB, '05_方法论', '酒店改造方案_3方向决策框架_v2.1_模板增强_2026-10-17.md'),
     '酒店改造方案3方向决策框架 v2.1', hmax=24, tmax=26, bmax=10)
