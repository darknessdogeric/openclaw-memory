# -*- coding: utf-8 -*-
"""修正：回滚用户版 → 在“四是一店一档”之前插入四川宾馆段 → 该段重排为五是"""
import io, sys, os, re, copy, shutil, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

P = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'
BAK = r'D:\B166ER-openclaw\workspace\tmp\_述职_用户版备份_1644.docx'

NEW = ('四是四川宾馆改造前期工作扎实推进。该项目2025年已完成立项，与锦江宾馆东楼改造一并纳入集团下属酒店固定资产改造汇报上报集团；'
       '2026年9月10日与深圳投资人就深圳华强北世万大厦四川宾馆改造与合作方案开展专项沟通，逐项摸排项目范围内40余名小业主及产权申办、'
       '硬件老旧、机电与停车场多楼共用等现状，明确以物业租赁为最清爽路径、第三方评估价作底价、保底租金加浮动收益的合作边界，'
       '并确认该项目属集团已过会的代改项目、合作方提出更优方案可调整原有规划；同时锁定四川宾馆品牌标识必须完整保留、'
       '承载政治经济文化三重诉求、定位巴蜀文化对外展示窗口的核心要求，成都店改造后定价目标600至800元每晚、'
       '深圳店精品定位预期1000元每晚以上，客房规模控制在80至130间，并完成全季5.0、丽芮等合作品牌适配比选。')

shutil.copy2(BAK, P)
print('已回滚至用户 16:44 版')
d = Document(P)
p54 = d.paragraphs[54]

runs = p54.runs
target = None
for i, r in enumerate(runs):
    t = r.text.strip()
    if t.startswith('四是') and '一店一档' in t:
        target = i
        break
if target is None:
    for i, r in enumerate(runs):
        if '一店一档' in r.text and r.text.strip().startswith('四'):
            target = i
            break
if target is None:
    print('!! 未定位到“四是一店一档”run'); sys.exit(2)
print('定位 run 索引 %d : %s' % (target, runs[target].text[:50]))

tpl = None
for r in runs:
    rpr = r._element.find(qn('w:rPr'))
    if rpr is not None and rpr.find(qn('w:highlight')) is None:
        tpl = copy.deepcopy(rpr)
        break

nr = p54.add_run(NEW)
old = nr._element.find(qn('w:rPr'))
if old is not None:
    nr._element.remove(old)
nr._element.insert(0, copy.deepcopy(tpl))
rpr = nr._element.find(qn('w:rPr'))
for tag in (qn('w:highlight'), qn('w:color')):
    el = rpr.find(tag)
    if el is not None:
        rpr.remove(el)
runs[target]._element.addprevious(nr._element)
print('四川宾馆段已插入于“四是一店一档”之前')

for r in p54.runs:
    if '一店一档' in r.text and r.text.strip().startswith('四是'):
        b = r.text
        r.text = r.text.replace('四是', '五是', 1)
        print('序号重排：%s  ->  %s' % (b[:24], r.text[:24]))
        break

d.save(P)
print('已保存: %s' % os.path.basename(P))

# ---------------- 校验 ----------------
d2 = Document(P)
P2 = d2.paragraphs
print()
print('=== P54 全文（验证插入位置）===')
print(P2[54].text)
print()
a = {n for n in zipfile.ZipFile(BAK).namelist() if not n.endswith('/')}
b = {n for n in zipfile.ZipFile(P).namelist() if not n.endswith('/')}
print('部件 %d -> %d，丢失 %s' % (len(a), len(b), ', '.join(sorted(a - b)) or '无'))
bad = 0
for r in P2[54].runs:
    rpr = r._element.find(qn('w:rPr'))
    ea = sz = hl = None
    if rpr is not None:
        f = rpr.find(qn('w:rFonts'))
        if f is not None:
            ea = f.get(qn('w:eastAsia'))
        h = rpr.find(qn('w:highlight'))
        if h is not None:
            hl = h.get(qn('w:val'))
        s = rpr.find(qn('w:sz'))
        if s is not None:
            sz = int(s.get(qn('w:val'))) / 2.0
    if hl != 'yellow' and (ea != '仿宋_GB2312' or sz != 16.0):
        bad += 1
        print('  !! 异常 run ea=%s sz=%s | %s' % (ea, sz, r.text[:36]))
print('P54 异常run = %d' % bad)
print('四川宾馆段位置校验: %s' % ('OK' if P2[54].text.index('四川宾馆改造前期工作') > P2[54].text.index('三是重点改造项目') else '位置错误'))
print('P52 未改动: %s' % ('OK' if len(P2[52].text) == len(Document(BAK).paragraphs[52].text) else '已变'))
mk = sum(1 for p in P2 if re.search(r'（待[^）]*）', p.text))
print('保留待补充标记 %d 处' % mk)
