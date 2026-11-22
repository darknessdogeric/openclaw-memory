# -*- coding: utf-8 -*-
"""量化清单 v1.3 -> v1.4：并入旅投总经会纪〔2026〕25号（5-1）派生的产发部任务"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

IMP = r'C:\Users\ericz\Desktop\产业发展部\重要文件'
KB7 = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革'
SRC = os.path.join(IMP, '2026-10-27_近期重点工作量化清单_v1.3.md')
if not os.path.exists(SRC):
    c = glob.glob(os.path.join(IMP, '*v1.3.md')) if False else None
import glob as _g
if not os.path.exists(SRC):
    _c = _g.glob(os.path.join(IMP, '*v1.3.md'))
    SRC = _c[0] if _c else os.path.join(KB7, '2026-10-27_近期重点工作量化清单_v1.3.md')
OUT_MD = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.md')
OUT_MD_KB = os.path.join(KB7, '2026-11-09_近期重点工作量化清单_v1.4.md')
OUT_DX = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.docx')

t = open(SRC, encoding='utf-8').read()
L = t.split(chr(10))
print('源:', os.path.basename(SRC), len(t), '字符', len(L), '行')

# ---------- 打印现有标题，核对结构 ----------
print('--- 现有章节 ---')
for l in L:
    if l.startswith('## ') or l.startswith('### '):
        print('   ' + l[:70])

def insert_after(anchor_sub, rows):
    for i, l in enumerate(L):
        if anchor_sub in l:
            for r in reversed(rows):
                L.insert(i + 1, r)
            return True
    print('   [MISS] ' + anchor_sub[:40])
    return False

def insert_before(anchor_sub, rows):
    for i, l in enumerate(L):
        if l.startswith(anchor_sub):
            for r in rows:
                L.insert(i, r)
            return True
    print('   [MISS] ' + anchor_sub[:40])
    return False

# ---------- 1. 关键节点表新增 ----------
insert_after('二销与空港意向转协议', [
    '| 产发部穿透式监管举措上报 | **11-30** | 5.11 | 未按"成熟一个、上报一个"报送，办公室督办时被点名 |',
    '| 议题合规性审查（美团等） | 指引到手后 5 日 | 5.12 | 议题材料不合规，退回重报 |',
    '| 十五五意见核销（党委会前置前） | 党委会前置研究前 | 5.13 | 18 条意见未落进规划稿 |',
])

# ---------- 2. 工作项一览新增 ----------
insert_after('全产业链四方向合作', [
    '| 4.5 | 集团合规与穿透式监管应对 | 合规 | 总经会 11 号议题落成产发部动作 | 11-30 | 第15/20次总经会决议原文 |',
])

# ---------- 3. 管理动作新增 5.11-5.15 ----------
insert_before('### 5.2', [
    '| 5.11 | 穿透式监管举措 | 按"成熟一个、上报一个"制定并上报本部门穿透式监管具体工作举措 | 首版上报旅投集团 | 11-30 |',
    '| 5.12 | 议题合规性审查 | 所有上会议题先过《规范议题合规性审查工作指引》，索取指引全文并宣贯 | 美团、商投、空港、新启航、中演等议题材料自查 | 指引到手后 5 日 |',
    '| 5.13 | 十五五意见核销 | 对 10-21 的 18 条 OA 意见逐条标注采纳情况，重点核销国堰零提及与测算不闭合 | 核销表 | 党委会前置研究前 |',
    '| 5.14 | 三项认领 | 认领决算整改台账中涉及安逸条目；确认二销是否属贸易业务及准入清单；对齐法人层级压减口径 | 三份认领／确认件 | 11-15 前两项 |',
    '| 5.15 | 招采与合作合规自查 | 对委托运营及合作类合同统一费率口径与对价形式披露，响应招采新规与违规投资问责办法修订 | 自查台账 | 11-30 |',
])

# ---------- 4. 六、上级对标 新增 6.5 ----------
sec65 = [
    '### 6.5　旅投总经会纪〔2026〕25 号（5-1）对标（2026-11-09 吸收）',
    '',
    '> 10-27 旅投总经理办公会决议，是 10-26 安逸联合例会全部部署的集团级上位依据。以下六项已落为产发部动作。',
    '',
    '| 总经会要求 | 产发部落点 |',
    '|---|---|',
    '| 第 11 号议题：各部门制定本部门穿透式监管具体工作举措，按"成熟一个、上报一个"报送 | 5.11 |',
    '| 第 10 号议题：《规范议题合规性审查工作指引》印发并宣贯培训 | 5.12 |',
    '| 第 8 号议题："十五五"规划送审稿原则同意，修订后报党委会前置研究 | 5.13 |',
    '| 第 2 号议题：对照整改台账细化举措责任到人；法人层级压减分析报告 | 5.14 |',
    '| 第 3 号议题：贸易业务监督管理工作规则与企业准入清单 | 5.14 |',
    '| 第 9 号议题：修订《违规经营投资责任追究实施办法》 | 5.15 |',
    '| 10-23 政治局会议：巡视整改意识融入日常经营，举一反三自查自纠 | 5.15 |',
    '',
]
insert_before('## 附：', sec65)

# ---------- 5. 附缺口新增 ----------
# 定位附缺口表最后一行
start = None
for i, l in enumerate(L):
    if l.startswith('## 附：'):
        start = i
        break
last = None
for i in range(start, len(L)):
    if L[i].startswith('| '):
        last = i
if last is not None:
    for r in reversed([
        '| 15 | **旅投总经会纪〔2026〕25 号 5-2 至 5-5 期全文（第 4、6、7 项议题）** | 集团级事项完整性 | 集团办公室（赵禹／陈川） | 11-15 |',
        '| 16 | **集团第 15 次（7/3）、第 20 次（9/10）总经会决议原文，及《规范议题合规性审查工作指引》全文** | 5.11／5.12 举措依据 | 集团办公室／法务合规部 | 11-15 |',
    ]):
        L.insert(last + 1, r)
    print('附缺口表最后一行已定位: ' + L[last][:40])

t2 = chr(10).join(L)

# ---------- 6. 计数与页脚 ----------
work = len(re.findall(r'(?m)^\| \d+\.\d+ \|', t2))
gaps = len(re.findall(r'(?m)^\| \d+ \|', t2))
try:
    i0 = t2.index('## 〇')
    i1 = t2.index('| # | 工作项 |')
    seg = t2[i0:i1]
    kn = len([x for x in seg.split(chr(10)) if x.startswith('| ') and not x.startswith('|---') and '关键节点' not in x and not x.startswith('| 关键节点')]) - 1
except Exception:
    kn = 0
print('计数：工作项 %d 项 / 关键节点 %d 个 / 缺口 %d 处' % (work, kn, gaps))
t2 = re.sub(r'(?m)^## 〇.*$', '## 〇　汇总：%d 项工作 · %d 个关键节点 · %d 处待补数据' % (work, kn, gaps), t2, count=1)

t2 = t2.replace('*编制：B166ER · 2026-10-27 · 近期重点工作量化清单 v1.3*',
                '*编制：B166ER · 2026-11-09 · 近期重点工作量化清单 v1.4*')
t2 = t2.replace('> **编制**：B166ER（安逸集团产业发展部）｜**版本**：v1.3（2026-10-27）',
                '> **编制**：B166ER（安逸集团产业发展部）｜**版本**：v1.4（2026-11-09）\n> **v1.4 变更来源**：吸收旅投总经会纪〔2026〕25 号（5-1，10-27）——新增第四节合规应对动作 5.11–5.15、6.5 节总经会对标表、3 个关键节点与 2 处待补数据')
t2 = t2.replace('*相关文件：2026-11-09_近期重点工作量化清单_v1.4.md｜',
                '*相关文件：2026-11-09_旅投总经会纪〔2026〕25号（5-1）_要点吸收_v1.0.md｜')

open(OUT_MD, 'w', encoding='utf-8').write(t2)
open(OUT_MD_KB, 'w', encoding='utf-8').write(t2)
print('v1.4 MD 已写入:')
print('  ' + OUT_MD)
print('  ' + OUT_MD_KB)

# ---------- 7. 转 docx ----------
CONV = r'D:\B166ER-openclaw\workspace\skills\docx-md-bridge\scripts\md_to_docx.py'
r = subprocess.run([sys.executable, CONV, OUT_MD, OUT_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:180])
shutil.copy2(OUT_DX, os.path.join(KB7, os.path.basename(OUT_DX)))

# ---------- 8. 校验 ----------
from docx import Document
d = Document(OUT_DX)
f = ''.join(x.text for x in d.paragraphs) + chr(10) + ''.join(c.text for tb in d.tables for rr in tb.rows for c in rr.cells)
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(OUT_DX)/1024, len(d.paragraphs), len(d.tables)))
for k in ['5.11 | 穿透式监管举措', '5.12 | 议题合规性审查', '5.13 | 十五五意见核销', '5.14 | 三项认领', '5.15 | 招采与合作合规自查', '6.5　旅投总经会纪', '4.5 | 集团合规与穿透式监管应对', '5-2 至 5-5 期全文', 'v1.4']:
    print('  %-32s %s' % (k, 'OK' if k in f else 'MISSING'))
