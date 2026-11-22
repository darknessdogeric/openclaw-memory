# -*- coding: utf-8 -*-
"""量化清单 v1.3 -> v1.4（修正版）：按表结构定位，正确计数"""
import io, sys, os, re, subprocess, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

IMP = r'C:\Users\ericz\Desktop\产业发展部\重要文件'
KB7 = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革'
_c = glob.glob(os.path.join(IMP, '*_v1.3.md')) or glob.glob(os.path.join(KB7, '*_v1.3.md'))
SRC = _c[0]
OUT_MD = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.md')
OUT_MD_KB = os.path.join(KB7, '2026-11-09_近期重点工作量化清单_v1.4.md')
OUT_DX = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.docx')

L = open(SRC, encoding='utf-8').read().split(chr(10))
print('源:', os.path.basename(SRC), len(L), '行')


def idx(pred, start=0):
    for i in range(start, len(L)):
        if pred(L[i]):
            return i
    return -1


def table_block(after_idx):
    """返回 (表头行号, 数据行起, 数据行止)；数据行为连续 '| ' 行"""
    h = idx(lambda l: l.startswith('| '), after_idx)
    if h < 0:
        return None
    s = h
    if h + 1 < len(L) and L[h + 1].startswith('|---'):
        s = h + 2
    e = s
    while e < len(L) and L[e].startswith('| '):
        e += 1
    return h, s, e


def rows_of(block):
    h, s, e = block
    return [L[i] for i in range(s, e)]


# ---------- 1. 关键节点总表：新增 3 行 ----------
b_kn = table_block(idx(lambda l: l.strip() == '### 关键节点总表'))
assert b_kn, '关键节点总表未找到'
kn_new = [
    '| 产发部穿透式监管举措上报 | **11-30** | 5.11 | 未按“成熟一个、上报一个”报送，办公室督办时被点名 |',
    '| 议题合规性审查（美团等） | 指引到手后 5 日 | 5.12 | 议题材料不合规，退回重报 |',
    '| 十五五意见核销（党委会前置前） | 党委会前置研究前 | 5.13 | 18 条意见未落进规划稿 |',
]
for r in reversed(kn_new):
    L.insert(b_kn[2], r)
print('关键节点总表: 插入 %d 行（数据行 %d→%d）' % (len(kn_new), b_kn[2] - len(kn_new), b_kn[2]))

# ---------- 2. 工作项一览：新增 1 行 ----------
b_wi = table_block(idx(lambda l: l.strip() == '### 工作项一览'))
assert b_wi, '工作项一览未找到'
wi_new = ['| 4.5 | 集团合规与穿透式监管应对 | 合规 | 总经会 11 号议题落成产发部动作 | 11-30 | 第15/20次总经会决议原文 |']
L.insert(b_wi[2], wi_new[0])
print('工作项一览: 插入 1 行')

# ---------- 3. 管理动作表（5.1）新增 5.11-5.15 ----------
b_51 = table_block(idx(lambda l: l.strip() == '### 5.1　管理动作'))
assert b_51, '5.1 表未找到'
act_new = [
    '| 5.11 | 穿透式监管举措 | 按“成熟一个、上报一个”制定并上报本部门穿透式监管具体工作举措 | 首版上报旅投集团 | 11-30 |',
    '| 5.12 | 议题合规性审查 | 所有上会议题先过《规范议题合规性审查工作指引》，索取指引全文并宣贯 | 美团、商投、空港、新启航、中演等议题材料自查 | 指引到手后 5 日 |',
    '| 5.13 | 十五五意见核销 | 对 10-21 的 18 条 OA 意见逐条标注采纳情况，重点核销国堰零提及与测算不闭合 | 核销表 | 党委会前置研究前 |',
    '| 5.14 | 三项认领 | 认领决算整改台账中涉及安逸条目；确认二销是否属贸易业务及准入清单；对齐法人层级压减口径 | 三份认领／确认件 | 11-15 前两项 |',
    '| 5.15 | 招采与合作合规自查 | 对委托运营及合作类合同统一费率口径与对价形式披露，响应招采新规与违规投资问责办法修订 | 自查台账 | 11-30 |',
]
for r in reversed(act_new):
    L.insert(b_51[2], r)
print('5.1 管理动作表: 插入 %d 行' % len(act_new))

# ---------- 4. 六、上级对标 新增 6.5 ----------
sec65 = [
    '### 6.5　旅投总经会纪〔2026〕25 号（5-1）对标（2026-11-09 吸收）',
    '',
    '> 10-27 旅投总经理办公会决议，是 10-26 安逸联合例会全部部署的集团级上位依据。以下六项已落为产发部动作。',
    '',
    '| 总经会要求 | 产发部落点 |',
    '|---|---|',
    '| 第 11 号议题：各部门制定本部门穿透式监管具体工作举措，按“成熟一个、上报一个”报送 | 5.11 |',
    '| 第 10 号议题：《规范议题合规性审查工作指引》印发并宣贯培训 | 5.12 |',
    '| 第 8 号议题：“十五五”规划送审稿原则同意，修订后报党委会前置研究 | 5.13 |',
    '| 第 2 号议题：对照整改台账细化举措责任到人；法人层级压减分析报告 | 5.14 |',
    '| 第 3 号议题：贸易业务监督管理工作规则与企业准入清单 | 5.14 |',
    '| 第 9 号议题：修订《违规经营投资责任追究实施办法》 | 5.15 |',
    '| 10-23 政治局会议：巡视整改意识融入日常经营，举一反三自查自纠 | 5.15 |',
    '',
]
i_fu = idx(lambda l: l.startswith('## 附：'))
assert i_fu > 0
for r in reversed(sec65):
    L.insert(i_fu, r)
print('六、上级党委会对标: 插入 6.5 节（%d 行）' % len(sec65))

# ---------- 5. 附缺口主表：新增 2 行 ----------
i_fu = idx(lambda l: l.startswith('## 附：'))
b_gap = table_block(i_fu)
assert b_gap, '附缺口主表未找到'
gap_new = [
    '| 15 | **旅投总经会纪〔2026〕25 号 5-2 至 5-5 期全文（第 4、6、7 项议题）** | 集团级事项完整性 | 集团办公室（赵禹／陈川） | 11-15 |',
    '| 16 | **集团第 15 次（7/3）、第 20 次（9/10）总经会决议原文，及《规范议题合规性审查工作指引》全文** | 5.11／5.12 举措依据 | 集团办公室／法务合规部 | 11-15 |',
]
for r in reversed(gap_new):
    L.insert(b_gap[2], r)
print('附缺口主表: 插入 %d 行（位置行号 %d）' % (len(gap_new), b_gap[2]))

# ---------- 6. 修正 v1.3 遗留编号错误 ----------
fixed = 0
for i, l in enumerate(L):
    if l.strip().startswith('### 4.3　已闭环事项'):
        L[i] = l.replace('### 4.3　已闭环事项', '### 5.3　已闭环事项')
        fixed += 1
print('修正遗留编号: %d 处' % fixed)

t2 = chr(10).join(L)

# ---------- 7. 重新计算计数（按表结构） ----------
def count_rows(lines, start_marker):
    i = idx(lambda l: l.strip() == start_marker, 0) if False else -1
    for k, l in enumerate(lines):
        if l.strip() == start_marker:
            i = k
            break
    if i < 0:
        return 0
    s = i + 1
    while s < len(lines) and not lines[s].strip():
        s += 1
    e = s
    while e < len(lines) and lines[e].startswith('| '):
        e += 1
    rows = lines[s:e]
    if rows and rows[0].startswith('|---'):
        rows = rows[1:]
    return len(rows)


n_kn = count_rows(L, '### 关键节点总表')
n_wi = count_rows(L, '### 工作项一览')
i_fu = idx(lambda l: l.startswith('## 附：'))
n_gap = count_rows(L, '## 附：需补齐的 14 处量化缺口'.split('14')[0].strip() + '14 处量化缺口') if False else 0
# 附缺口主表
h, s, e = table_block(idx(lambda l: l.startswith('## 附：')))
n_gap = e - s
print('计数：关键节点 %d 个 / 工作项 %d 项 / 缺口 %d 处' % (n_kn, n_wi, n_gap))
t2 = re.sub(r'(?m)^## 〇.*$', '## 〇　汇总：%d 项工作 · %d 个关键节点 · %d 处待补数据' % (n_wi, n_kn, n_gap), t2, count=1)
t2 = t2.replace('## 附：需补齐的 14 处量化缺口', '## 附：需补齐的 %d 处量化缺口' % n_gap)

# ---------- 8. 页脚 ----------
t2 = t2.replace('*编制：B166ER · 2026-10-27 · 近期重点工作量化清单 v1.3*',
                '*编制：B166ER · 2026-11-09 · 近期重点工作量化清单 v1.4*')
t2 = t2.replace('> **编制**：B166ER（安逸集团产业发展部）｜**版本**：v1.3（2026-10-27）',
                '> **编制**：B166ER（安逸集团产业发展部）｜**版本**：v1.4（2026-11-09）\n> **v1.4 变更来源**：吸收旅投总经会纪〔2026〕25 号（5-1，10-27）——新增管理动作 5.11–5.15、6.5 节总经会对标表、3 个关键节点、1 项工作与 2 处待补数据；并修正 v1.3 遗留的 5.3 节编号错误')

open(OUT_MD, 'w', encoding='utf-8').write(t2)
open(OUT_MD_KB, 'w', encoding='utf-8').write(t2)
print('MD ->', OUT_MD)

CONV = r'D:\B166ER-openclaw\workspace\skills\docx-md-bridge\scripts\md_to_docx.py'
r = subprocess.run([sys.executable, CONV, OUT_MD, OUT_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:160])
shutil.copy2(OUT_DX, os.path.join(KB7, os.path.basename(OUT_DX)))

# ---------- 9. 校验（按单元格逐个匹配） ----------
from docx import Document
d = Document(OUT_DX)
cells = set()
for tb in d.tables:
    for rr in tb.rows:
        for c in rr.cells:
            cells.add(c.text.strip())
paras = [x.text.strip() for x in d.paragraphs]
alltext = chr(10).join(cells) + chr(10) + chr(10).join(paras)
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(OUT_DX)/1024, len(d.paragraphs), len(d.tables)))
print('--- 逐项校验 ---')
checks = ['5.11', '5.12', '5.13', '5.14', '5.15', '4.5', '6.5　旅投总经会纪', '5.3　已闭环事项',
          '穿透式监管举措', '议题合规性审查', '十五五意见核销', '三项认领', '招采与合作合规自查',
          '集团合规与穿透式监管应对', '5-2 至 5-5 期全文', '第15/20次总经会决议原文', 'v1.4']
for k in checks:
    ok = (k in cells) or (k in alltext)
    print('  %-26s %s' % (k, 'OK' if ok else 'MISSING'))
print('--- 汇总标题 ---')
for x in paras:
    if x.startswith('## 〇') or x.startswith('## 附：'):
        print('  ' + x)
