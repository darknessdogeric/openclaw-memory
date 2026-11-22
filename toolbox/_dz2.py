# -*- coding: utf-8 -*-
import io, sys, os, re, glob, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部'

def dump_docx(path, tag, keywords, maxp=26, maxt=40, maxh=40):
    print('=' * 94)
    print('【' + tag + '】' + os.path.basename(path))
    if not os.path.exists(path):
        print('  !! 缺失'); return
    d = Document(path)
    print('  段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
    print('  --- 结构 ---')
    n = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        st = p.style.name if p.style is not None else ''
        if 'Head' in st or '标题' in st or 'Title' in st:
            print('   [%s] %s' % (st[:12], t[:96])); n += 1
            if n >= maxh:
                break
    print('  --- 关键段落 ---')
    n = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if len(t) < 14:
            continue
        if any(k in t for k in keywords):
            print('   * ' + t[:225]); n += 1
            if n >= maxp:
                break
    print('  --- 表格 ---')
    n = 0
    for tb in d.tables:
        for row in tb.rows:
            cells = [c.text.strip().replace('\n', ' ')[:34] for c in row.cells]
            line = ' | '.join([c for c in cells if c])
            if len(line) < 8:
                continue
            print('   ' + line[:190]); n += 1
            if n >= maxt:
                break
        if n >= maxt:
            break
    print()

KWS = ('数字化', '中台', '一期', '二期', '立项', '存量改造', '标准', '流程', '品牌', 'CRS', '会员', '轻改', '模块')

dump_docx(os.path.join(DESK, '意见建议', '关于安逸集团十五五规划存量改造与数智化建设的建议_v7.0_2026-09-16.docx'),
          'Eric 存量改造与数智化建议 v7.0（2026-09-16）', KWS, maxp=30, maxt=44, maxh=46)

dump_docx(os.path.join(DESK, '意见建议', '关于安逸集团十五五规划战略部分调整建议（存量改造与数智化）.docx'),
          'Eric 十五五战略部分调整建议（存量改造与数智化）', KWS, maxp=16, maxt=30, maxh=30)

# KB 总览四步路线
p = os.path.join(KB, '00_安逸集团知识库总览.md')
if os.path.exists(p):
    print('=' * 94)
    print('【安逸集团知识库总览 — 四步路线与数字化定位】')
    t = open(p, encoding='utf-8', errors='replace').read()
    for l in t.split('\n'):
        s = l.strip()
        if any(k in s for k in ('第一步', '第二步', '第三步', '第四步', '数字化', '中台', '轻重分离', '标杆', '标准输出', '品牌运营')):
            print('   ' + s[:210])
    print()
