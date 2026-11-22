# -*- coding: utf-8 -*-
"""落库 + 固化时间戳纪律（来源台账 / AGENTS.md / MEMORY.md / self-improving 规则）"""
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb')
MARK = '安逸集团文件时间戳纪律'


def append_once(path, marker, block):
    """幂等追加：已含 marker 则跳过"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(block)
        print('  新建: %s' % os.path.basename(path))
        return True
    t = open(path, encoding='utf-8', errors='replace').read()
    if marker in t:
        print('  已含该规则，跳过: %s' % os.path.basename(path))
        return False
    if not t.endswith('\n'):
        t += '\n'
    open(path, 'w', encoding='utf-8').write(t + '\n' + block)
    print('  追加: %s' % os.path.basename(path))
    return True


# ============ 1. 来源台账 ============
print('=== 1. 来源台账 ===')
ledger = os.path.join(KB, '00_来源台账.md')
block = '''## 📥 入库清单（2026-11-12 追加 — 安逸集团重大事项请示：安逸连锁改革脱困 + 古尔沟改革盘活）

> **任务来源**：Eric 2026-11-12 11:22 "重要项目情况吸收。同时要求你对安逸集团此类文件要做时间戳。以后在调阅和引述的时候需要有时间标示。"
> **归档执行**：B166ER 2026-11-12，两份请示全文解析（docx 直读 + 自研 Word 97 piece-table 解析），全部数据带 as-of 时点
> **新增纪律**：本批起，安逸集团类文件一律建立时间戳台账（成文日／最后修改／数据截止／提取时间四要素）

| # | 材料 | 原始路径 | 成文日期 | 文件最后修改 | 数据截止 | 类型 | 入库位置 |
|---|------|----------|---------|------------|---------|------|----------|
| 1 | **安逸酒店集团有限责任公司关于恳请集团同意四川安逸连锁酒店有限公司系统性改革脱困有关事项的请示(4).docx** | `C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件\\重要项目情况\\` | 2026-11-04 | 2026-11-11 14:07 | 财务 2026-09-30／借款明细 2026-09-14 | 公文（请示） | `07_战略与改革/2026-11-12_安逸集团重大事项请示_要点吸收_v1.0.md` |
| 2 | **安逸酒店集团有限责任公司关于恳请集团同意四川古尔沟神峰温泉有限公司系统性改革盘活实施方案的请示.doc** | 同上 | 2026-11-04 | 2026-11-12 10:10 | 财务 2026-06-30／人员 2026-06-30 | 公文（请示，OLE2 二进制） | 同上 |

**时间戳纪律落点**：见 AGENTS.md「安逸集团文件时间戳纪律」与 `self-improving/rules_安逸文件时间戳标注.md`。

'''
append_once(ledger, '2026-11-12 追加 — 安逸集团重大事项请示', block)

# ============ 2. AGENTS.md ============
print()
print('=== 2. AGENTS.md ===')
agents = os.path.join(WS, 'AGENTS.md')
block2 = '''## 安逸集团文件时间戳纪律（2026-11-12 Eric 指令）

**适用范围**：所有安逸集团类文件——请示、报告、会议纪要、方案、台账、合同、批注稿。

**入库与调阅一律保留时间戳四要素，缺一不可**：
1. **成文日期**：以文件落款／文号日期为准，不是文件系统时间
2. **文件最后修改时间**：文件系统时间
3. **数据截止时点（as-of）**：文件内部各口径的数据时点常不一致，须逐项标注，不得用成文日代替
4. **提取／入库时间**

**引述格式**：`《文件名》（YYYY-MM-DD 成文，数据截至 YYYY-MM-DD）`

**三条易错点**：
- **落款日不等于最后修改日**。2026-11-12 批次两份请示落款同为 11-04，其中一份最后修改为 11-12，必须分别标注。
- **同一文件内口径不同**。例：安逸连锁请示财务截至 09-30、借款明细截至 09-14；古尔沟请示财务截至 06-30。**跨文件合并分析前先核时点差**（本例相差一个季度，不可直接比数）。
- **时效性要单独验**。请示中记载的未来时点（如"推迟至 11-10 开庭"）在吸收时可能已过期，引用时须标"结果待核"。

**吸收文件落库位置**：`anyi-ops-kb/07_战略与改革/` 或对应项目目录，文件名含日期与版本。

'''
append_once(agents, MARK, block2)

# ============ 3. MEMORY.md ============
print()
print('=== 3. MEMORY.md ===')
mem = os.path.join(WS, 'MEMORY.md')
block3 = '''### 2026-11-12 安逸集团文件时间戳纪律（Eric 指令）

- **要求**：安逸集团类文件入库与调阅一律带时间戳，引述时必须有时间标示。
- **四要素**：成文日期（落款）／文件最后修改／数据截止 as-of（逐项标注）／提取时间。
- **引述格式**：`《文件名》（YYYY-MM-DD 成文，数据截至 YYYY-MM-DD）`。
- **落款日 ≠ 最后修改日**；**同文件内口径不同须逐项标注**；**记载的未来时点可能已过期须标待核**。
- 规则全文：AGENTS.md「安逸集团文件时间戳纪律」。
- 首批发样：`07_战略与改革/2026-11-12_安逸集团重大事项请示_要点吸收_v1.0.md`（安逸连锁改革脱困 + 古尔沟改革盘活两份请示）。

'''
append_once(mem, '安逸集团文件时间戳纪律（Eric 指令）', block3)

# ============ 4. self-improving 规则文件 ============
print()
print('=== 4. self-improving 规则文件 ===')
cands = [os.path.join(WS, 'self-improving'), os.path.join(os.path.expanduser('~'), 'self-improving')]
target = None
for c in cands:
    if os.path.isdir(c):
        target = c
        break
if target is None:
    target = cands[0]
    os.makedirs(target, exist_ok=True)
    print('  新建目录: %s' % target)
else:
    print('  规则目录: %s' % target)
rule = os.path.join(target, 'rules_安逸文件时间戳标注.md')
block4 = '''# 规则：安逸集团文件的时间戳标注

> **来源**：Eric 2026-11-12 11:22 指令 —— "同时要求你对安逸集团此类文件要做时间戳。以后在调阅和引述的时候需要有时间标示。"
> **适用范围**：安逸集团全部公文类文件（请示、报告、会议纪要、方案、台账、合同、批注稿）

## 核心要求

调阅和引述安逸集团文件时，**必须带时间标示**。入库时建立时间戳台账，引述时按标准格式输出。

## 时间戳四要素

| 要素 | 取值来源 | 备注 |
|---|---|---|
| 成文日期 | 文件落款或文号日期 | **不是**文件系统时间 |
| 文件最后修改时间 | 文件系统 | 与成文日常不同，须分别标注 |
| 数据截止时点（as-of） | 文件内部各表口径 | 逐项标注，不得用成文日代替 |
| 提取／入库时间 | 实际处理时间 | — |

## 引述格式

    《文件名》（YYYY-MM-DD 成文，数据截至 YYYY-MM-DD）

## 三类高频错误

1. **落款日当成最后修改日**：2026-11-12 批次两份请示落款同为 11-04，一份最后修改为 11-12。
2. **用成文日充当数据时点**：安逸连锁请示财务截至 09-30、借款明细截至 09-14；古尔沟请示财务截至 06-30。跨文件比数前先核时点差（本例差一个季度）。
3. **照抄文件里的未来时点**：请示写"推迟至 11-10 开庭"，吸收时已过期，须标"结果待核"。

## 落地

- 吸收文件：`anyi-ops-kb/07_战略与改革/` 或对应项目目录，文件名含日期与版本。
- 来源台账：`anyi-ops-kb/00_来源台账.md`，入库即登记四要素。
- 首批发样：`2026-11-12_安逸集团重大事项请示_要点吸收_v1.0.md`。
'''
append_once(rule, '安逸集团文件的时间戳标注', block4)

# ============ 5. 验证 ============
print()
print('=== 验证 ===')
for p in [ledger, agents, mem, rule]:
    t = open(p, encoding='utf-8', errors='replace').read()
    hit = ('时间戳' in t) or ('时间标示' in t)
    print('  %-46s %8d B  含时间戳规则=%s' % (os.path.basename(p), os.path.getsize(p), '是' if hit else '否'))
