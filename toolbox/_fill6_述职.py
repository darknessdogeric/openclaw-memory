# -*- coding: utf-8 -*-
import io, sys, os, re, copy, shutil, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

P = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'
BAK = r'D:\B166ER-openclaw\workspace\tmp\_述职_用户版备份_1644.docx'
MARK = '（待资产部核对补充）'

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

rs = None
for i, r in enumerate(runs):
    if '【补充】' in r.text:
        rs = i
        break
if rs is None:
    print('!! 未找到【补充】'); sys.exit(2)

tail = ''.join(r.text for r in runs[rs:])
assert MARK in tail
body_part, marker_part = tail[:tail.index(MARK)], tail[tail.index(MARK):]

k = body_part.index('一店一档')
pos = body_part.rindex('四是', 0, k)
old4 = body_part[pos:pos + 8]
print('原“四是…”片段: %r' % old4)

# 四是 = 2 个字符
new_body = body_part[:pos] + NEW + '五是' + body_part[pos + 2:]

tpl = None
for r in runs:
    rpr = r._element.find(qn('w:rPr'))
    if rpr is not None and rpr.find(qn('w:highlight')) is None:
        tpl = copy.deepcopy(rpr)
        break

for r in list(runs[rs:]):
    r._element.getparent().remove(r._element)


def add(text, highlight=None, color=None):
    r = p54.add_run(text)
    if tpl is not None:
        old = r._element.find(qn('w:rPr'))
        if old is not None:
            r._element.remove(old)
        r._element.insert(0, copy.deepcopy(tpl))
        rpr = r._element.find(qn('w:rPr'))
        for tag in (qn('w:highlight'), qn('w:color')):
            el = rpr.find(tag)
            if el is not None:
                rpr.remove(el)
    if highlight or color:
        rpr = r._element.get_or_add_rPr()
        if highlight:
            rpr.append(rpr.makeelement(qn('w:highlight'), {qn('w:val'): highlight}))
        if color:
            rpr.append(rpr.makeelement(qn('w:color'), {qn('w:val'): color}))
    return r


add(new_body)
add(marker_part, 'yellow', 'FF0000')
print('已重建补充段（正文 1 + 标记 1）')

d.save(P)
print('已保存: %s' % os.path.basename(P))

# ---------------- 校验 ----------------
d2 = Document(P)
P2 = d2.paragraphs
t = P2[54].text
print()
print('=== P54 补充段全文 ===')
print(t[t.index('【补充】'):])
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
print('四川宾馆段出现次数 = %d（应为 1）' % t.count('四川宾馆改造前期工作'))
print('插入位置 = %s' % ('OK' if (t.index('四川宾馆改造前期工作') > t.index('三是重点改造项目') and t.index('四川宾馆改造前期工作') < t.index('五是一店一档') if '五是一店一档' in t else False) else '需查'))
print('序号检查: 四是四川宾馆=%s   五是一店一档=%s' % ('OK' if '四是四川宾馆改造前期工作' in t else 'X', 'OK' if '五是“一店一档”' in t else 'X'))
print('资产标记 = %s' % ('OK' if MARK in t else 'MISSING'))
print('P52 未改动 = %s' % ('OK' if len(P2[52].text) == len(Document(BAK).paragraphs[52].text) else '已变'))
print('保留待补充标记 %d 处' % sum(1 for p in P2 if re.search(r'（待[^）]*）', p.text)))
print('P54 长度 %d' % len(t))
