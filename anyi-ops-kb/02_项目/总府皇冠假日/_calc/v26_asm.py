# -*- coding: utf-8 -*-
"""v26 报告装配脚本：按标题键整块替换 + 表格注入 + 图件路径更新"""
import io, os, sys, re, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
def _load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T = _load('T26', os.path.join(CALC,'v26_tables.py'))
P1 = _load('P1', os.path.join(CALC,'_v26_p1.py'))
P2 = _load('P2', os.path.join(CALC,'_v26_p2.py'))
P3 = _load('P3', os.path.join(CALC,'_v26_p3.py'))
NL = chr(10)

CH3B = '''## 3.3 可行性四条件

**（一）造价依据。** 业主第 43 项自编造价 18,000 万元，与洲际 PIP 原件 18,000–20,000 万元区间一致；**品牌方建议的 430 间房量不能作为主方案**——业主方已书面指出「客房面积与实测不符，须以实测口径重算」。据此本报告以实测面积 25.35 ㎡ 为唯一口径，造价按 039 完整造价构成表分三段计量，作为**财务分层成立**的前提。

**（二）主体结构。** 本项目以保留 402 间客房为主方案，且 25.35 ㎡ 客房套内面积低于皇冠实际标准客房净面积门槛，须取得品牌方书面面积例外；结构安全鉴定结论与面积例外共同决定房量方案是否成立。

**（三）财务可行性。** 以市场分析中档价格计，A1 皇冠假日·保留客房体量·轻改路径的 20 年增量口径 NPV 为正 3,457 万元、增量 IRR 11.35%、静态回收期 9.8 年；A2 安逸集团自有五星路径为正 3,290 万元、IRR 11.22%、回收期 9.9 年。**因此本项目的可行性结论是「财务可行」，其前提是保留 402 间客房体量并按市场分析价格承载。**

**（四）工期可行性。** 按工程流水法核定的停业期为 19 个月（保留体量轻改路径），其中不可压缩项为冷源主机订造 9 个月、机电主干 4 个月、系统联调与消防整体验收 2 个月、整改复评 1.5 个月、试营业 1 个月。**建议以 12 个月为停业期控制目标，并对施工方设置工期违约金。**

'''

# ── 表格注入 ──
def inject(s):
    s = s.replace('__T_BRAND_DETAIL__', T.t_brand_detail())
    s = s.replace('__T_BRAND__', T.t_brand())
    s = s.replace('__T_INVEST__', T.t_invest())
    s = s.replace('__T_SCHED__', T.t_sched())
    s = s.replace('__T_FIN__', T.t_fin())
    s = s.replace('__T_GRID_FULL__', T.t_grid('full'))
    s = s.replace('__T_GRID_INC__', T.t_grid('inc'))
    s = s.replace('__T_CAP__', T.t_cap())
    s = s.replace('__T_SENS__', T.t_sens())
    s = s.replace('__T_THR__', T.t_thr())
    return s

# ── 图件引用 ──
FIG_CH6 = NL + '![图5　各路径停业期工程流水核定](_calc/fig26/fig05_停业期流水.png)' + NL
FIG_CH7A = NL + '![图2　八路径 NPV 与 IRR 对比](_calc/fig26/fig02_三路径财务对比.png)' + NL
FIG_CH7B = NL + '![图4　推荐路径的 15 格动态区间](_calc/fig26/fig04_动态区间热力.png)' + NL
FIG_CH8A = NL + '![图1　增量口径 NPV 对 ADR 的敏感性与市场分析价格带](_calc/fig26/fig01_增量NPV对ADR.png)' + NL
FIG_CH8B = NL + '![图3　A1 平衡点左右的阈值区间](_calc/fig26/fig03_敏感性龙卷风.png)' + NL
FIG_CH5 = NL + '![图6　25 个品牌候选增量口径 NPV 比较](_calc/fig26/fig06_25品牌增量NPV.png)' + NL

CH5 = inject(P2.CH5.replace('__T_BRAND_DETAIL__', T.t_brand_detail() + FIG_CH5))
CH6 = inject(P2.CH6).replace('**（二）停业期是本项目第二刚变量。**', FIG_CH6 + NL + '**（二）停业期是本项目第二刚变量。**')
CH7 = inject(P2.CH7)
CH7 = CH7.replace('## 7.2 增量口径', FIG_CH7A + NL + '## 7.2 增量口径')
CH7 = CH7.replace('## 7.4 静态回收期', FIG_CH7B + NL + '## 7.4 静态回收期')
CH8 = inject(P3.CH8)
CH8 = CH8.replace('## 8.2 可承受改造投资上限', FIG_CH8A + NL + '## 8.2 可承受改造投资上限')
CH8 = CH8.replace('## 8.3 敏感性分析', FIG_CH8B + NL + '## 8.3 敏感性分析')
CONC = inject(P1.CONC)
CH1 = inject(P1.CH1)
CH2 = inject(P1.CH2)
CH4B = inject(P3.CH4B)
CH12B = inject(P3.CH12B)
CH16 = inject(P3.CH16)

SRC = os.path.join(KB,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md')
Tx = io.open(SRC, encoding='utf-8').read()
lines = Tx.split(NL)

def hkey(line):
    m = re.match(r'^(#{1,6})\s*([0-9]+(?:\.[0-9]+)*)\.?\s', line+' ')
    return (len(m.group(1)), m.group(2)) if m else None
def find_title(lines, word, after=0):
    for i in range(after, len(lines)):
        if lines[i].startswith('#') and word in lines[i]: return i
    return -1
def block_bounds(lines, start_key, end_key=None, title=None):
    si = -1
    if title is not None:
        si = find_title(lines, title)
    else:
        for i,l in enumerate(lines):
            if hkey(l)==start_key: si=i; break
    if si<0: return None
    if end_key is not None:
        for j in range(si+1, len(lines)):
            if hkey(lines[j])==end_key: return si,j
        return None
    lvl = len(lines[si].split(' ')[0])
    for j in range(si+1, len(lines)):
        if lines[j].startswith('#'):
            if len(lines[j].split(' ')[0])<=lvl: return si,j
    return si, len(lines)

JOBS = [
 (dict(title='结论摘要', end_key=(1,'1')), CONC),
 (dict(start_key=(1,'1'), end_key=(1,'2')), CH1),
 (dict(start_key=(1,'2'), end_key=(1,'3')), CH2),
 (dict(start_key=(2,'3.3'), end_key=(1,'4')), CH3B),
 (dict(start_key=(2,'4.2'), end_key=(3,'4.2.2')), CH4B),
 (dict(start_key=(1,'5'), end_key=(1,'6')), CH5),
 (dict(start_key=(1,'6'), end_key=(1,'7')), CH6),
 (dict(start_key=(1,'7'), end_key=(1,'8')), CH7),
 (dict(start_key=(1,'8'), end_key=(1,'9')), CH8),
 (dict(start_key=(2,'12.2'), end_key=(1,'13')), CH12B),
 (dict(start_key=(1,'16')), CH16),
]
ok=0; fail=[]
for spec, new in JOBS:
    b = block_bounds(lines, spec.get('start_key'), spec.get('end_key'), spec.get('title'))
    if b is None:
        fail.append(str(spec)); continue
    si, ei = b
    lines = lines[:si] + new.split(NL) + lines[ei:]
    ok += 1
Tx = NL.join(lines)

# ── 版本、日期、目录、图件路径 ──
Tx = Tx.replace('（v25.0）','（v26.0）').replace('v25.0_2026-11-16','v26.0_2026-11-20')
Tx = Tx.replace('| 摘要 | **结论摘要（结论先行）** | 能不能做、要做多少、能不能赚钱 |',
                '| 摘要 | **结论摘要（结论先行）** | 能不能做、该做多少、能不能赚钱 |')
Tx = Tx.replace('| 5 | 品牌候选统一比较 | 25 个品牌放一张表 |',
                '| 5 | 品牌候选统一比较 | 25 个品牌统一表（含安逸自有五星） |')
Tx = Tx.replace('| 6 | 路径界定与投资估算 | 每条路径多少钱、顶量减为无量 |',
                '| 6 | 路径界定与投资估算 | 三类路径、八条方案的投资与工期 |')
Tx = Tx.replace('| 7 | 财务测算 | 每条路径赚不赚钱 |',
                '| 7 | 财务测算 | 全口径、增量口径与动态区间矩阵 |')
Tx = Tx.replace('| 8 | 盈亏平衡与敏感性分析 | 结论对假设有多敏感 |',
                '| 8 | 盈亏平衡与敏感性分析 | 平衡点、阈值区间与可承受投资上限 |')
Tx = Tx.replace('_calc/fig/fig5_停业期流水.png', '_calc/fig26/fig05_停业期流水.png')
Tx = Tx.replace('_calc/fig/fig1_现金流曲线.png', '_calc/fig26/fig07_现金流与累计.png')
Tx = Tx.replace('_calc/fig/fig2_NPV路径.png', '_calc/fig26/fig02_三路径财务对比.png')
Tx = Tx.replace('_calc/fig/fig3_敏感性.png', '_calc/fig26/fig03_敏感性龙卷风.png')
Tx = Tx.replace('_calc/fig/fig4_NPV对ADR.png', '_calc/fig26/fig01_增量NPV对ADR.png')
Tx = Tx.replace('![图1　20 年现金流曲线与 TRevPAR 趋势]', '![图7　20 年现金流与累计增量现金流]')
Tx = Tx.replace('![图2　NPV 路径与 IRR 对比]', '![图2　八路径 NPV 与 IRR 对比]')
Tx = Tx.replace('![图4　增量口径 NPV 对 ADR 的敏感性]', '![图1　增量口径 NPV 对 ADR 的敏感性与市场分析价格带]')
Tx = Tx.replace('![图3　P4 敏感性（增量口径 NPV）]', '![图3　A1 平衡点左右的阈值区间]')

OUT = os.path.join(KB,'总府皇冠改造_可行性研究报告_v26.0_2026-11-20.md')
io.open(OUT,'w',encoding='utf-8').write(Tx)
print('replaced %d, failed %s' % (ok, fail))
print('written', OUT, len(Tx))
print('placeholders left:', sorted(set(re.findall(r'\{\{[^}]+\}\}|__T_[A-Z_]+__', Tx))))
print('fig refs:', sorted(set(re.findall(r'_calc/fig\d+/[^)]+', Tx))))