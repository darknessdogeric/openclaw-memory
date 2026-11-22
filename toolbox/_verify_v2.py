# -*- coding: utf-8 -*-
import io, sys, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from collections import Counter

DESK = 'C:\\Users\\ericz\\Desktop'
WS = 'D:\\B166ER-openclaw\\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
NAME = '2026-11-21_对大运营体系建设实施方案草案的意见建议_一页纸'
DX = os.path.join(DESK, NAME + '.docx')

print('=== 1. 交付物核验 ===')
print('存在:', os.path.exists(DX), ' 大小:', os.path.getsize(DX) // 1024, 'KB')
print('修改时间:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(DX))))
d = Document(DX)
c = Counter()
for p in d.paragraphs:
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
s = d.sections[0]
print('页边距 上%.1f 下%.1f 左%.1f 右%.1f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('段落 %d' % len(d.paragraphs))
print('')
print('=== 全文 ===')
for p in d.paragraphs:
    t = p.text.strip()
    if t:
        print(t)

# ---------- KB 追加架构修正 ----------
KBF = os.path.join(KB, '2026-11-21_大运营体系建设实施方案_问题分析_v1.0.md')
MARK = '架构前提修正（Eric 2026-11-21）'
ADD = '''

---

## 补充：架构前提修正（Eric 2026-11-21）

> **修正**：本分析稿初版（2026-11-21 00:38）按"产业发展部视角"提出 16 条意见。Eric 于 2026-11-21 10:27 给出集团架构口径并明确要求"不以产业发展部为中心，完全按照分工协作来"，初版 16 条中多数不在产业发展部管理序列，已于同日重做为 13 条分工协作口径一页纸。

### 一、集团架构口径（Eric 2026-11-21 10:27 口述）

| 层级 | 主体 | 承接范围 |
|---|---|---|
| 集团本部 | 保留**品牌、标准、IT架构、产品模型**四项工作 | 不参与具体经营和执行行为 |
| 集团本部 | 产业发展部 | 集团对外合作整体纳入 |
| 集团本部 | 资产运营中心 | 资产部分收归 |
| 集团本部 | 运营管理中心 | **合并至饭店管理公司** |
| 三级公司 | 饭店管理公司（其内设大运营中心） | 承接全部酒店项目的经营、管理与拓展，含旗下自营酒店；可独立开展业务 |

### 二、初版 16 条的取舍映射

| 初版条目 | 处理 | 理由 |
|---|---|---|
| 管道费与商业化岗 | **保留并升级** | 升格为集团本部定价权与管公司执行权分离的跨主体机制，非单一岗位 |
| 收益管理独立 | **保留并改写** | 主体改为饭店管理公司大运营中心；集团本部输出价格体系与价格代码标准 |
| 中央集采服务费 | **保留** | 纳入统一管道费口径 |
| 业主关系维护单列 | **保留并改写** | 主体改为饭店管理公司 |
| 增列筹开岗 | **保留并改写** | 主体改为饭店管理公司 |
| 品牌标准与管理放集团本部 | **保留（Eric 新增）** | 与"集团只留四件事"一致 |
| AI 体系与架构放集团本部 | **保留（Eric 新增）** | 与"集团只留四件事"一致 |
| 亏损治理与绩效考核不划出 | **删除** | 属资产运营中心与饭店管理公司序列 |
| 量化目标、投入产出、风险退出、验收主体 | **删除** | 属集团经营与考核序列 |
| 100 家以上承接机制 | **删除** | 属饭店管理公司序列 |
| 三家样板店产出标准 | **改写并入** | 改为"标准以改造样板店为验证载体、分模块发布、版本管理" |
| 品牌经理制 | **改写并入** | 改为"品牌标准与品牌管理归本部，管公司负责开发与拓展" |
| 数字化与 AI-RMS 接口 | **改写并入** | 改为"架构归本部、应用归管公司、开发与拓展纳入管道费体系" |
| AK 替代与数字旅投交接 | **删除** | 属集团内部划转安排 |
| 改造技术标准库 | **删除** | 属饭店管理公司序列 |
| 筹开以外的新增岗位（会员、集采、新零售等） | **删除** | 属饭店管理公司序列 |

### 三、重做后新增的三条（初版未提，为新架构所必需）

1. **集团本部服务目录与响应机制**——本部只留品牌、标准、IT架构、产品模型且不参与执行，须以"标准＋服务＋授权"方式交付，避免只出文件不落地。
2. **资产运营中心—饭店管理公司—门店三层界面**——轻重分离落地的前置：租赁定价、委托管理费、考核与亏损分担规则，以及品牌授权与管道费收入在三层中的归属与确认口径。
3. **对外合作两条线的统一出口与授权规则**——集团对外合作归产业发展部、饭店管理公司可独立开展业务，两者之间的品牌与系统授权边界须事先划定，避免多口径授权、品牌稀释与收入体外循环。

### 四、一页纸结构（13 条，四板块）

| 板块 | 条数 | 主题 |
|---|---|---|
| 一 | 5 | 集团本部与饭店管理公司的分工 |
| 二 | 2 | 资产运营中心与饭店管理公司的分工 |
| 三 | 3 | 跨主体的定价机制：管道费体系 |
| 四 | 3 | 饭店管理公司的内部建制 |

*交付：`C:\\Users\\ericz\\Desktop\\2026-11-21_对大运营体系建设实施方案草案的意见建议_一页纸.docx`（11.0pt 仿宋、行距固定 16 磅、LibreOffice 实测 1 页）*
'''

if os.path.exists(KBF):
    t = open(KBF, encoding='utf-8', errors='replace').read()
    if MARK in t:
        print('')
        print('KB 架构修正段已存在，跳过追加')
    else:
        open(KBF, 'a', encoding='utf-8').write(ADD)
        print('')
        print('KB 已追加架构修正段 -> %d B' % os.path.getsize(KBF))
else:
    open(KBF, 'w', encoding='utf-8').write(ADD)
    print('KB 新建 -> %d B' % os.path.getsize(KBF))

# 归档目录核对
arch = os.path.join(DESK, '产业发展部', '重要文件')
print('')
print('=== 归档目录核对 ===')
for f in sorted(os.listdir(arch)):
    if '大运营' in f or '一页纸' in f:
        print('  ' + f + '  ' + str(os.path.getsize(os.path.join(arch, f)) // 1024) + 'KB')
