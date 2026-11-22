"""
小红书多图笔记 - 2026 H1 酒店行业全景复盘
- 15 张主图 + 1 张商品指引
- 竖版 3:4 比例 (1080x1440)
- 配色：东方美学（朱红/金/青/赭/灰）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

font_path = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans SC'
plt.rcParams['axes.unicode_minus'] = False

OUT = 'D:/B166ER-OpenClaw/workspace/reports/xhs'
os.makedirs(OUT, exist_ok=True)

# 东方美学配色
CRIMSON = '#C73E1D'
GOLD = '#C99A3D'
JADE = '#3A8B6E'
INDIGO = '#2C5F7C'
UMBER = '#7A5230'
ASH = '#5C5742'
BG = '#FDFBF6'
INK = '#2a2a2a'

# 3:4 竖版 (1080x1440)
W, H = 10.8, 14.4  # 放大 10 倍方便统一单位

def add_title_logo(fig, title, subtitle=None, accent=CRIMSON):
    """添加标题栏（小红书风格顶部装饰条）"""
    fig.patches.append(plt.Rectangle((0, 0), W, 0.6, color=accent, alpha=0.92))
    fig.text(W/2, 0.3, title, ha='center', va='center', fontsize=18, color='white', fontweight='bold')
    if subtitle:
        fig.text(W/2, 0.95, subtitle, ha='center', va='bottom', fontsize=10, color=ASH, style='italic')

def add_footer(fig, page_num, total=15, brand="ERIC的B166ER出品"):
    """添加底部页码 + 品牌"""
    fig.text(0.5, 0.15, f"{page_num} / {total}", ha='center', va='bottom', fontsize=10, color=ASH)
    fig.text(0.5, 0.4, brand, ha='center', va='bottom', fontsize=9, color=ASH, style='italic')

# ====================================================
# 图 1：封面（吸睛关键）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.04, right=0.96, top=0.96, bottom=0.04)

# 顶部装饰条
fig.patches.append(plt.Rectangle((0, 0), 1, 0.04, color=CRIMSON, transform=fig.transFigure))

# 大标题（中央）
fig.text(0.5, 0.78, '2026 H1', ha='center', va='center', fontsize=60, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.66, '中国酒店行业全景复盘', ha='center', va='center', fontsize=32, color=INK, fontweight='bold')

# 副标题：核心数字（吸睛）
fig.text(0.5, 0.52, '同比上一年原则 | 58 维度', ha='center', va='center', fontsize=18, color=ASH)
fig.text(0.5, 0.46, '端午 +4.4% | 五一双降 | 春节内资+28-35%', ha='center', va='center', fontsize=15, color=JADE)

# 装饰：金线 + 文房四宝
fig.patches.append(plt.Rectangle((0.1, 0.35), 0.8, 0.005, color=GOLD, transform=fig.transFigure))
fig.text(0.5, 0.28, '供给结构升级', ha='center', va='center', fontsize=14, color=ASH)
fig.text(0.5, 0.23, '中端酒店占比 35.1% 首次超经济型', ha='center', va='center', fontsize=14, color=CRIMSON, fontweight='bold')

fig.text(0.5, 0.12, 'ERIC 出品  |  2026-07-23', ha='center', va='center', fontsize=10, color=UMBER)

plt.savefig(f'{OUT}/01_cover.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 1 cover')

# ====================================================
# 图 2：核心数字（视觉冲击）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '核心数字', 'CORE NUMBERS', CRIMSON)

fig.text(0.5, 0.88, '2026 H1 三大关键指标', ha='center', va='center', fontsize=22, fontweight='bold', color=INK)

# 三大指标卡片式
y_positions = [0.7, 0.5, 0.3]
data_main = [
    ('端午', '1.24 亿/人次', '+4.4% YoY', CRIMSON, '文旅部'),
    ('五一酒店 OCC', '63.5%', '-7.92pp 高基数效应', GOLD, '酒店之家'),
    ('内资前 5 RevPAR', '+28-35%', '春节同比 2025', JADE, '财报'),
]
for y, (label, value, delta, color, src) in zip(y_positions, data_main):
    fig.patches.append(plt.Rectangle((0.1, y-0.05), 0.8, 0.12, color=color, alpha=0.1, transform=fig.transFigure))
    fig.text(0.15, y+0.04, label, ha='left', va='center', fontsize=15, color=INK, fontweight='bold')
    fig.text(0.5, y+0.01, value, ha='center', va='center', fontsize=22, color=color, fontweight='bold')
    fig.text(0.85, y-0.02, delta, ha='right', va='center', fontsize=11, color=ASH)
    fig.text(0.15, y-0.04, f'来源: {src}', ha='left', va='center', fontsize=9, color=UMBER)

fig.text(0.5, 0.18, '⚠️ 同比基准 = 2025 同期（非 2024）', ha='center', va='center', fontsize=12, color=CRIMSON, fontweight='bold', style='italic')
fig.text(0.5, 0.12, '关键发现：2025 五一历史高位 → 2026 高基数效应', ha='center', va='center', fontsize=11, color=ASH)

add_footer(fig, 2)
plt.savefig(f'{OUT}/02_core_numbers.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 2 core numbers')

# ====================================================
# 图 3：内资前 5 上市集团
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '内资前 5 上市集团', '2026 春节同比 2025 春节', CRIMSON)

groups = ['锦江酒店', '华住集团', '首旅酒店', '亚朵集团', '格林酒店']
revpar = [35, 33, 32, 28, 28]
adr = [298, 312, 285, 571, 228]

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
x = np.arange(len(groups))
bars = ax.bar(x, revpar, 0.6, color=[CRIMSON]*4 + [UMBER], edgecolor='#3a1f15', linewidth=0.8)
for b, r in zip(bars, revpar):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.8, f'+{r}%', ha='center', fontsize=14, color=CRIMSON, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=12, color=ASH, rotation=15)
ax.set_ylim(0, 42)
ax.set_ylabel('RevPAR YoY (%)', fontsize=11, color=ASH)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)

fig.text(0.5, 0.25, '⭐ 亚朵 ADR ¥571 领跑（春节档）', ha='center', fontsize=12, color=GOLD, fontweight='bold')
fig.text(0.5, 0.20, '锦江 ¥298 / 华住 ¥312 / 首旅 ¥285 / 格林 ¥228', ha='center', fontsize=10, color=ASH)
fig.text(0.5, 0.13, '头部 5 家合计 4.2 万+ 门店 / 320+ 万客房', ha='center', fontsize=11, color=JADE)

add_footer(fig, 3)
plt.savefig(f'{OUT}/03_internal_top5.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 3 internal')

# ====================================================
# 图 4：外资前 5 上市集团
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '外资前 5 上市集团', '2026 春节同比 2025 春节', INDIGO)

groups = ['万豪\n国际', '洲际\n酒店', '希尔顿', '雅高\n集团', '凯悦\n酒店']
revpar = [28, 26, 27, 24, 22]
revpar_val = [493, 419, 446, 375, 938]

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
x = np.arange(len(groups))
bars1 = ax.bar(x-0.15, revpar, 0.3, label='RevPAR YoY %', color=INDIGO, edgecolor='#162d3a', linewidth=0.8)
bars2 = ax.bar(x+0.15, [r/30 for r in revpar_val], 0.3, label='RevPAR/30 元', color=GOLD, edgecolor='#3a2410', linewidth=0.8)
for b, r in zip(bars1, revpar):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f'+{r}%', ha='center', fontsize=11, color=INDIGO, fontweight='bold')
for b, r in zip(bars2, revpar_val):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+5, f'¥{r}', ha='center', fontsize=9, color=GOLD, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=11, color=ASH)
ax.set_ylim(0, 42)
ax.legend(loc='upper right', frameon=False, fontsize=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)

fig.text(0.5, 0.25, '⭐ 凯悦 RevPAR ¥938 最高（奢华定位）', ha='center', fontsize=12, color=GOLD, fontweight='bold')
fig.text(0.5, 0.20, '外资奢华市场份额 ~80% / 高端 ~60%', ha='center', fontsize=11, color=ASH)
fig.text(0.5, 0.13, '2026 雅高扭亏为盈 + 与华住战略合作', ha='center', fontsize=10, color=JADE)

add_footer(fig, 4)
plt.savefig(f'{OUT}/04_foreign_top5.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 4 foreign')

# ====================================================
# 图 5：连锁化率 41.80%
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '连锁化率', 'CHAIN RATE 2022-2025', JADE)

years = ['2022', '2023', '2024', '2025末']
chain = [35, 38, 40.09, 41.80]
top10 = [50, 54, 57, 59.38]

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
ax2 = ax.twinx()
ax2.set_facecolor(BG)
bars = ax.bar(years, chain, 0.5, color=CRIMSON, edgecolor='#3a1f15', linewidth=0.8, alpha=0.9, label='连锁化率 %')
line = ax2.plot(years, top10, marker='o', linewidth=3, color=JADE, markersize=14, markeredgecolor='#1d3a30', markeredgewidth=2, label='TOP10 集中度 %')
for b, v in zip(bars, chain):
    ax.text(b.get_x()+b.get_width()/2, v+0.5, f'{v}%', ha='center', fontsize=14, color=CRIMSON, fontweight='bold')
for x_p, v in zip(range(len(years)), top10):
    ax2.text(x_p, v+1, f'{v}%', ha='center', fontsize=12, color=JADE, fontweight='bold')
ax.set_ylim(0, 50); ax2.set_ylim(0, 70)
ax.set_ylabel('连锁化率 %', fontsize=11, color=CRIMSON)
ax2.set_ylabel('TOP10 集中度 %', fontsize=11, color=JADE)
ax.spines['top'].set_visible(False); ax2.spines['top'].set_visible(False)
ax.spines['left'].set_color(CRIMSON); ax2.spines['right'].set_color(JADE)
ax.grid(axis='y', linestyle='--', alpha=0.3)
L1, l1 = ax.get_legend_handles_labels(); L2, l2 = ax2.get_legend_handles_labels()
ax.legend(L1+L2, l1+l2, loc='upper left', frameon=False, fontsize=10)

fig.text(0.5, 0.27, '⭐ 连锁化率 +1.71pp / TOP10 集中度 +2.38pp', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.22, 'TOP10 占连锁新增 74% — 马太效应显著', ha='center', fontsize=11, color=ASH)
fig.text(0.5, 0.14, '前 50 家集团客房 594 万间 / TOP10 = 59.38%', ha='center', fontsize=10, color=JADE)

add_footer(fig, 5)
plt.savefig(f'{OUT}/05_chain_rate.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 5 chain rate')

# ====================================================
# 图 6：中端酒店超经济型（转折点）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '结构性转折', '2026 H1 关键拐点', GOLD)

fig.text(0.5, 0.87, '中端酒店首次超经济型', ha='center', va='center', fontsize=22, color=INK, fontweight='bold')

categories = ['奢华', '高档', '中高端', '中端 ⭐', '经济型', '民宿']
share = [3, 12, 15, 35.1, 27.3, 7.6]
colors = [INDIGO, UMBER, GOLD, CRIMSON, JADE, '#A0456F']

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
wedges, texts, autotexts = ax.pie(share, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11, 'color': INK}, wedgeprops={'edgecolor': BG, 'linewidth': 2})
for at in autotexts:
    at.set_color('white'); at.set_fontweight('bold')
ax.text(0, 0, '35.1%\nvs\n27.3%', ha='center', va='center', fontsize=14, color=CRIMSON, fontweight='bold',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor=CRIMSON, linewidth=1.5))

fig.text(0.5, 0.22, '⭐ 中端占比 35.1% ⏫ 首次超经济型 27.3% ⏬', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.16, '本土系品牌 90.4% | 新店超 70% ≤150 间（集体瘦身）', ha='center', fontsize=10, color=ASH)
fig.text(0.5, 0.11, '行业从"量增"切换到"质升"', ha='center', fontsize=11, color=JADE, fontweight='bold')

add_footer(fig, 6)
plt.savefig(f'{OUT}/06_mid_vs_economy.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 6 mid vs econ')

# ====================================================
# 图 7：2026 五一 vs 2025 五一（高基数）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '五一高基数效应', '2026 vs 2025', CRIMSON)

fig.text(0.5, 0.87, '2026 五一双降是基数效应', ha='center', va='center', fontsize=20, color=INK, fontweight='bold')

metrics = ['OCC\n(%)', 'ADR\n(元)', 'RevPAR\n(元)']
y25 = [71.42, 448.58, 320]
y26 = [63.5, 295.98, 187.33]

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
x = np.arange(len(metrics)); w = 0.35
b1 = ax.bar(x-0.2, y25, w, label='2025 五一 (订单来了)', color=GOLD, edgecolor='#3a2410', linewidth=0.8, alpha=0.85)
b2 = ax.bar(x+0.2, y26, w, label='2026 五一 (酒店之家)', color=CRIMSON, edgecolor='#3a1f15', linewidth=0.8)
for b, v in zip(b1, y25):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f'{v}' if v < 100 else f'¥{v:.0f}', ha='center', fontsize=10, color=GOLD, fontweight='bold')
for i, (b, v) in enumerate(zip(b2, y26)):
    delta_pct = (v - y25[i]) / y25[i] * 100
    delta_pp = v - y25[i] if i == 0 else 0
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f'{v}' if v < 100 else f'¥{v:.0f}',
            ha='center', fontsize=10, color=CRIMSON, fontweight='bold')
    if i == 0:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+30, f'{delta_pp:+.1f}pp', ha='center', fontsize=9, color=CRIMSON)
    else:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+30, f'{delta_pct:+.0f}%', ha='center', fontsize=9, color=CRIMSON)
ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=12, color=INK)
ax.legend(loc='upper right', frameon=False, fontsize=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)

fig.text(0.5, 0.25, '⭐ 2025 五一是历史高位', ha='center', fontsize=13, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.20, 'OCC 71.42% / ADR ¥448.58（订单来了数据）', ha='center', fontsize=11, color=ASH)
fig.text(0.5, 0.14, '口径差异 + 高基数 → 2026 双降 ≠ 行业衰退', ha='center', fontsize=11, color=GOLD, fontweight='bold')

add_footer(fig, 7)
plt.savefig(f'{OUT}/07_wuyi_baseline.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 7 wuyi')

# ====================================================
# 图 8：民宿冰火两重天
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '民宿冰火两重天', 'HOMESTAY 冰 vs 火', JADE)

# 上下两列对比
fig.text(0.5, 0.85, '预约首超酒店 | 价格冰封', ha='center', va='center', fontsize=20, color=INK, fontweight='bold')

# 火
fig.patches.append(plt.Rectangle((0.1, 0.5), 0.38, 0.25, color=CRIMSON, alpha=0.1, transform=fig.transFigure))
fig.text(0.29, 0.71, '🔥 火', ha='center', va='center', fontsize=16, color=CRIMSON, fontweight='bold')
fig.text(0.29, 0.65, '2026 H1 预订占', ha='center', fontsize=10, color=INK)
fig.text(0.29, 0.61, '53%', ha='center', fontsize=20, color=CRIMSON, fontweight='bold')
fig.text(0.29, 0.55, '首次超传统酒店', ha='center', fontsize=9, color=ASH)

# 冰
fig.patches.append(plt.Rectangle((0.52, 0.5), 0.38, 0.25, color=INDIGO, alpha=0.1, transform=fig.transFigure))
fig.text(0.71, 0.71, '❄️ 冰', ha='center', va='center', fontsize=16, color=INDIGO, fontweight='bold')
fig.text(0.71, 0.65, '2024 民宿均价', ha='center', fontsize=10, color=INK)
fig.text(0.71, 0.61, '¥367 -30%', ha='center', fontsize=20, color=INDIGO, fontweight='bold')
fig.text(0.71, 0.55, 'OCC 仅 36%', ha='center', fontsize=9, color=ASH)

# 下半：数据曲线
fig.text(0.5, 0.42, '2025 五一民宿反弹（订单来了）', ha='center', va='center', fontsize=14, color=INK, fontweight='bold')

years = ['2024', '2025 H1', '2026 H1']
market = [422.7, 380, 360]
ax = fig.add_subplot(212)
ax.set_facecolor(BG)
ax.plot(years, market, marker='o', linewidth=2.5, color=CRIMSON, markersize=12)
for x_p, v in zip(years, market):
    ax.text(x_p, v+10, f'¥{v}亿', ha='center', fontsize=10, color=CRIMSON, fontweight='bold')
ax.set_ylim(300, 480)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_title('民宿市场规模（亿元）', fontsize=11, color=ASH)

fig.text(0.5, 0.18, '⭐ 冰火共存：头部精品+淘汰单体', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.13, '中产+银发+亲子 客群转向旅居康养', ha='center', fontsize=10, color=ASH)

add_footer(fig, 8)
plt.savefig(f'{OUT}/08_homestay.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 8 homestay')

# ====================================================
# 图 9：上海/广州/三亚 韧性
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '高端市场韧性', 'JLL H1 2026', INDIGO)

cities = ['上海\n奢华', '广州\n高端', '三亚\n奢华']
occ = [3, 5.9, 0]
adr = [7, 0, 17]

ax = fig.add_subplot(111)
ax.set_facecolor(BG)
x = np.arange(len(cities))
b1 = ax.bar(x-0.2, occ, 0.4, label='OCC YoY (pp)', color=JADE, edgecolor='#1d3a30', linewidth=0.8)
b2 = ax.bar(x+0.2, adr, 0.4, label='ADR YoY (%)', color=CRIMSON, edgecolor='#3a1f15', linewidth=0.8)
for b, v in zip(b1, occ):
    if v > 0:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f'+{v}pp', ha='center', fontsize=11, color=JADE, fontweight='bold')
for b, v in zip(b2, adr):
    if v > 0:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f'+{v}%', ha='center', fontsize=11, color=CRIMSON, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(cities, fontsize=12, color=INK)
ax.legend(loc='upper right', frameon=False, fontsize=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)

# 注释
ax.text(0-0.2, 3.5, 'OCC +3pp', ha='center', fontsize=11, color=JADE, fontweight='bold')
ax.text(0+0.2, 7.5, 'ADR +7%', ha='center', fontsize=11, color=CRIMSON, fontweight='bold')
ax.text(1, 4, '广州 RevPAR\n¥754 (+5.9%)', ha='center', fontsize=10, color=ASH,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ASH))
ax.text(2+0.2, 18, 'ADR +17%', ha='center', fontsize=11, color=CRIMSON, fontweight='bold')

fig.text(0.5, 0.27, '⭐ 一线/奢华市场具备韧性', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.21, '上海 1-5月国际入境 438 万人次 (+29.1%)', ha='center', fontsize=11, color=ASH)
fig.text(0.5, 0.15, '上海 H1 酒店交易额占全国 22% (JLL)', ha='center', fontsize=10, color=JADE)

add_footer(fig, 9)
plt.savefig(f'{OUT}/09_premium.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 9 premium')

# ====================================================
# 图 10：REITs 退出打通
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, 'REITs 退出打通', 'JLL 6.25 重磅', GOLD)

fig.text(0.5, 0.87, '酒店资产证券化新阶段', ha='center', va='center', fontsize=20, color=INK, fontweight='bold')

fig.patches.append(plt.Rectangle((0.15, 0.55), 0.7, 0.22, color=GOLD, alpha=0.1, transform=fig.transFigure))
fig.text(0.5, 0.72, '2026-06-25', ha='center', va='center', fontsize=14, color=GOLD, fontweight='bold')
fig.text(0.5, 0.67, '中国酒店 REITs 白皮书', ha='center', va='center', fontsize=18, color=INK, fontweight='bold')
fig.text(0.5, 0.61, '44 页 | JLL 仲量联行', ha='center', va='center', fontsize=12, color=ASH)
fig.text(0.5, 0.57, '行业资本化新阶段', ha='center', va='center', fontsize=11, color=CRIMSON, fontweight='bold')

fig.text(0.5, 0.45, '⭐ 关键意义', ha='center', va='center', fontsize=14, color=CRIMSON, fontweight='bold')
implications = [
    '酒店资产类型扩容至酒店（解锁退出通道）',
    '雅高 2026 扭亏为盈 + REITs 并行',
    '投资人可配置酒店资产（像 REITs 一样）',
    '业主可 REITs 退出 / 投资人可 REITs 入场',
]
for i, imp in enumerate(implications):
    fig.text(0.5, 0.40-i*0.04, f'• {imp}', ha='center', va='center', fontsize=10, color=ASH)

fig.text(0.5, 0.18, '⚡ 中长期最大结构性机会', ha='center', va='center', fontsize=12, color=CRIMSON, fontweight='bold')

add_footer(fig, 10)
plt.savefig(f'{OUT}/10_reits.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 10 REITs')

# ====================================================
# 图 11：旅居康养 8 万亿
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '旅居康养 8 万亿', '国务院明确支持', JADE)

fig.text(0.5, 0.87, '结构性的长期机会', ha='center', va='center', fontsize=20, color=INK, fontweight='bold')

# 中央核心数字
fig.patches.append(plt.Circle((0.5, 0.62), 0.13, color=JADE, alpha=0.2, transform=fig.transFigure))
fig.text(0.5, 0.65, '8', ha='center', va='center', fontsize=64, color=JADE, fontweight='bold')
fig.text(0.5, 0.55, '万亿元', ha='center', va='center', fontsize=14, color=JADE)

fig.text(0.5, 0.43, '银发文旅市场规模（2025E）', ha='center', va='center', fontsize=12, color=ASH)
fig.text(0.5, 0.38, '国务院《关于发展银发经济增进老年人福祉的意见》', ha='center', va='center', fontsize=9, color=GOLD, fontweight='bold')

# 三个支持数据
fig.patches.append(plt.Rectangle((0.05, 0.18), 0.28, 0.12, color=CRIMSON, alpha=0.1, transform=fig.transFigure))
fig.text(0.19, 0.27, '+82%', ha='center', fontsize=18, color=CRIMSON, fontweight='bold')
fig.text(0.19, 0.22, '东北老人\n赴云南订单', ha='center', fontsize=9, color=INK)

fig.patches.append(plt.Rectangle((0.36, 0.18), 0.28, 0.12, color=GOLD, alpha=0.1, transform=fig.transFigure))
fig.text(0.5, 0.27, '600万', ha='center', fontsize=18, color=GOLD, fontweight='bold')
fig.text(0.5, 0.22, '2025E\n云南旅居', ha='center', fontsize=9, color=INK)

fig.patches.append(plt.Rectangle((0.67, 0.18), 0.28, 0.12, color=INDIGO, alpha=0.1, transform=fig.transFigure))
fig.text(0.81, 0.27, '+124%', ha='center', fontsize=18, color=INDIGO, fontweight='bold')
fig.text(0.81, 0.22, '美团本地\n酒店度假', ha='center', fontsize=9, color=INK)

fig.text(0.5, 0.12, '⭐ 民宿旅居康养 18%（酒店仅 0% — 巨大空间）', ha='center', fontsize=10, color=CRIMSON, fontweight='bold')

add_footer(fig, 11)
plt.savefig(f'{OUT}/11_lvju_health.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 11 lvju')

# ====================================================
# 图 12：三大权威信息源
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '权威信息源', 'AUTHORITATIVE', ASH)

fig.text(0.5, 0.87, '4 大 + 4 大行 + 7 券商', ha='center', va='center', fontsize=20, color=INK, fontweight='bold')

# 三列布局
groups = [
    ('4 大审计', CRIMSON, ['普华永道', '德勤', '安永', '毕马威'], '审计/税务/咨询'),
    ('4 大行', JADE, ['工商', '建设', '农业', '中国'], '商旅/跨境'),
    ('7 券商', INDIGO, ['中信', '中金', '华泰', '国信', '海通', '招商', '国君'], '研报覆盖'),
]
for i, (name, color, items, role) in enumerate(groups):
    x_center = 0.17 + i * 0.33
    fig.patches.append(plt.Rectangle((x_center-0.13, 0.62), 0.26, 0.2, color=color, alpha=0.1, transform=fig.transFigure))
    fig.text(x_center, 0.78, name, ha='center', fontsize=14, color=color, fontweight='bold')
    for j, item in enumerate(items[:4]):
        fig.text(x_center, 0.72-j*0.025, '• ' + item, ha='center', fontsize=10, color=INK)
    fig.text(x_center, 0.50, role, ha='center', fontsize=9, color=ASH, style='italic')

# 三大数据库
fig.text(0.5, 0.40, '⭐ 三大金融数据库', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
databases = ['Wind 资讯', 'Bloomberg 彭博', 'QuestMobile']
for i, db in enumerate(databases):
    fig.text(0.5, 0.35 - i*0.04, '▸ ' + db, ha='center', fontsize=11, color=INK)

fig.text(0.5, 0.20, '⭐ Eric 强调："报告基础"，所有数据均可追溯', ha='center', fontsize=11, color=GOLD, fontweight='bold', style='italic')

add_footer(fig, 12)
plt.savefig(f'{OUT}/12_big4_banks_brokers.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 12 big4 banks')

# ====================================================
# 图 13：三句话总结
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '三句话总结', 'BOTTOM LINE', CRIMSON)

fig.text(0.5, 0.87, '2026 H1 三个核心判断', ha='center', va='center', fontsize=18, color=INK, fontweight='bold')

# 三句话
sentences = [
    ('01', '供给结构升级 + 节假日高基数效应', '中端酒店占比 35.1% 首次超经济型 (27.3%)，2026 五一双降是 2025 高基数效应'),
    ('02', '内资前 5 全部 RevPAR +28-35%', '锦江/华住/首旅/亚朵/格林 头部集中度提升，2026 春节同比 2025'),
    ('03', 'REITs + 旅居康养 = 长期机会', 'JLL 6.25 白皮书 + 8 万亿银发市场 = 资本化新阶段'),
]

for i, (num, title, desc) in enumerate(sentences):
    y = 0.72 - i * 0.20
    fig.patches.append(plt.Circle((0.12, y+0.04), 0.04, color=CRIMSON, transform=fig.transFigure))
    fig.text(0.12, y+0.04, num, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    fig.text(0.20, y+0.07, title, ha='left', fontsize=13, color=INK, fontweight='bold')
    fig.text(0.20, y+0.01, desc, ha='left', fontsize=10, color=ASH)
    fig.patches.append(plt.Rectangle((0.20, y-0.03), 0.75, 0.005, color=GOLD, alpha=0.5, transform=fig.transFigure))

fig.text(0.5, 0.13, '⭐ 这就是 2026 H1', ha='center', fontsize=14, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.10, '质量 × 集中 × 资本化', ha='center', fontsize=12, color=GOLD)

add_footer(fig, 13)
plt.savefig(f'{OUT}/13_three_lines.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 13 three lines')

# ====================================================
# 图 14：行动建议（业主/投资人/从业者）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

add_title_logo(fig, '行动建议', 'WHO & WHAT TO DO', GOLD)

fig.text(0.5, 0.87, '你的身份 → 该做什么', ha='center', va='center', fontsize=18, color=INK, fontweight='bold')

actions = [
    ('投资人', GOLD, ['聚焦中端连锁', '配置 REITs', '关注旅居康养']),
    ('业主', CRIMSON, ['押注中端酒店', '绑定康养产品', '使用 AHL SaaS']),
    ('从业者', JADE, ['加入头部集团', '拥抱连锁化 + 数字化', '关注 AHL 试点']),
    ('政策方', INDIGO, ['推动 REITs 落地', '配套银发旅居', '简化审批']),
]

for i, (role, color, acts) in enumerate(actions):
    y = 0.72 - i * 0.16
    x_pos = 0.20 if i % 2 == 0 else 0.62
    fig.patches.append(plt.Rectangle((x_pos, y-0.06), 0.20, 0.13, color=color, alpha=0.15, transform=fig.transFigure))
    fig.text(x_pos+0.10, y+0.05, role, ha='center', va='center', fontsize=12, color=color, fontweight='bold')
    for j, a in enumerate(acts):
        fig.text(x_pos+0.10, y-j*0.03, '• ' + a, ha='center', fontsize=8, color=INK)

fig.text(0.5, 0.13, '⭐ 不同身份 → 不同策略', ha='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.10, 'AHL 试点：乐山锦江嘉州宾馆（已部署）', ha='center', fontsize=10, color=GOLD, style='italic')

add_footer(fig, 14)
plt.savefig(f'{OUT}/14_actions.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 14 actions')

# ====================================================
# 图 15：商品指引（CTA）
# ====================================================
fig = plt.figure(figsize=(W/2, H/2), dpi=120)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

# CTA 顶部装饰
fig.patches.append(plt.Rectangle((0, 0.93), 1, 0.07, color=CRIMSON, transform=fig.transFigure))
fig.text(0.5, 0.965, '⭐ 个人出品 — 酒店业知识商品 ⭐', ha='center', va='center', fontsize=18, color='white', fontweight='bold')

fig.text(0.5, 0.85, '想深入学习？ERIC 出品 5 项', ha='center', va='center', fontsize=22, color=INK, fontweight='bold')

products = [
    ('🏨', '酒店投资测算 / 选址 / 筹开', '精装方案 + 测算表 + SOP'),
    ('📋', 'AHL / AI Agent 落地', '完整方案 + 1V1 咨询'),
    ('🌄', '民宿 / 旅居 / 康养', '大理 0 号实验室案例'),
    ('💼', '收益管理 + 餐饮收益', '实战手册 + 案例库'),
    ('📚', '酒店行业知识库订阅', '完整 542 首音乐 + KB + 周报'),
]

for i, (icon, name, desc) in enumerate(products):
    y = 0.74 - i * 0.12
    fig.patches.append(plt.Rectangle((0.08, y-0.04), 0.84, 0.10, color=GOLD, alpha=0.08, transform=fig.transFigure))
    fig.text(0.13, y+0.01, icon, ha='center', va='center', fontsize=20)
    fig.text(0.20, y+0.025, name, ha='left', va='center', fontsize=12, color=INK, fontweight='bold')
    fig.text(0.20, y-0.02, desc, ha='left', va='center', fontsize=9, color=ASH)

fig.text(0.5, 0.13, '购买方式：', ha='center', va='center', fontsize=12, color=CRIMSON, fontweight='bold')
fig.text(0.5, 0.10, '私信 "ERIC 出品" 获取方案 + 1V1 咨询', ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')
fig.text(0.5, 0.07, '备注：景区民宿 / 酒店投资 / AHL 试点', ha='center', va='center', fontsize=9, color=UMBER, style='italic')

add_footer(fig, 15)
plt.savefig(f'{OUT}/15_products_cta.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('[OK] 15 CTA')

print('\n[DONE] 15 张小红书笔记图已生成 ->', OUT)
import os
for f in sorted(os.listdir(OUT)):
    if f.startswith(tuple([f'0{i}_' for i in range(1, 10)]) + ['10_', '11_', '12_', '13_', '14_', '15_']):
        print(f'  {os.path.getsize(os.path.join(OUT, f)):>7} {f}')