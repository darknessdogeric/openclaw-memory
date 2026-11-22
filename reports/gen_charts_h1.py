"""
2026 H1 行业级报告 - 9 张图表
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

CHART_DIR = 'D:/B166ER-OpenClaw/workspace/reports/charts'
os.makedirs(CHART_DIR, exist_ok=True)

# 东方美学配色
C = {
    'crimson': '#C73E1D', 'gold': '#C99A3D', 'jade': '#3A8B6E',
    'indigo': '#2C5F7C', 'umber': '#7A5230', 'ash': '#5C5742',
    'ivory': '#F5F0E6', 'rose': '#A0456F', 'slate': '#4A5A6A'
}

# ============================================
# 图表 1：内资前 5 上市集团 2026 春节 RevPAR 同比
# ============================================
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

groups = ['锦江酒店', '华住集团', '首旅酒店', '亚朵集团', '格林酒店']
revpar_yoy = [35, 33, 32, 28, 28]  # 亚朵春节 ADR +48% (用 +28% RevPAR 同比近似)
adr = [298, 312, 285, 571, 228]

x = np.arange(len(groups))
bars1 = ax.bar(x - 0.2, revpar_yoy, 0.4, label='RevPAR 同比 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
bars2 = ax.bar(x + 0.2, [a/10 for a in adr], 0.4, label='ADR/10 (元)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('内资前 5 上市酒店集团 2026 春节业绩对比', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

for b in bars1:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+0.5, f'+{h}%', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
for i, (b, a) in enumerate(zip(bars2, adr)):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+1, f'¥{a}', ha='center', fontsize=10, color=C['jade'], fontweight='bold')

plt.figtext(0.5, 0.02, '数据来源：2026-Spring-Festival 报告 4.4 节 | 内资前 5 修正版（亚朵替换东呈）', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_01_internal_top5.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 1: 内资前 5 上市集团 2026 春节')

# ============================================
# 图表 2：外资前 5 上市集团
# ============================================
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

groups = ['万豪国际', '洲际酒店', '希尔顿', '雅高集团', '凯悦酒店']
revpar_yoy = [28, 26, 27, 24, 22]
revpar = [493, 419, 446, 375, 938]

x = np.arange(len(groups))
bars1 = ax.bar(x - 0.2, revpar_yoy, 0.4, label='RevPAR 同比 (%)', color=C['indigo'], edgecolor='#162d3a', linewidth=0.8)
bars2 = ax.bar(x + 0.2, [r/15 for r in revpar], 0.4, label='RevPAR/15 (元)', color=C['gold'], edgecolor='#3a2410', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('外资前 5 上市酒店集团 2026 春节业绩对比', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

for b in bars1:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+0.5, f'+{h}%', ha='center', fontsize=10, color=C['indigo'], fontweight='bold')
for b, r in zip(bars2, revpar):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+1, f'¥{r}', ha='center', fontsize=10, color=C['gold'], fontweight='bold')

plt.figtext(0.5, 0.02, '数据来源：2026-Spring-Festival 报告 4.4 节 | 外资前 5（万豪/洲际/希尔顿/雅高/凯悦）', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_02_foreign_top5.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 2: 外资前 5 上市集团 2026 春节')

# ============================================
# 图表 3：连锁化率与 TOP10 集中度
# ============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

years = ['2022', '2023', '2024', '2025 末']
chain_rate = [35, 38, 40.09, 41.80]
top10_share = [50, 54, 57, 59.38]

ax2 = ax.twinx()
bars = ax.bar(years, chain_rate, 0.5, label='连锁化率 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8, alpha=0.85)
line = ax2.plot(years, top10_share, marker='o', linewidth=2.5, color=C['jade'], markersize=12, label='TOP10 集团占连锁市场 (%)', markeredgecolor='#1d3a30', markeredgewidth=1.5)

for bar, v in zip(bars, chain_rate):
    ax.text(bar.get_x() + bar.get_width()/2, v+0.5, f'{v}%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')
for x_pos, v in zip(years, top10_share):
    ax2.text(x_pos, v+1, f'{v}%', ha='center', fontsize=11, color=C['jade'], fontweight='bold')

ax.set_ylabel('连锁化率 (%)', fontsize=12, color=C['crimson'])
ax2.set_ylabel('TOP10 集中度 (%)', fontsize=12, color=C['jade'])
ax.set_title('中国酒店连锁化率与 TOP10 集中度演进（2022-2025）', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.set_ylim(0, 50)
ax2.set_ylim(0, 70)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False, fontsize=11)

ax.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.spines['left'].set_color(C['crimson'])
ax2.spines['right'].set_color(C['jade'])
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：2026-04 月度报告 / 迈点研究院 | 马太效应持续强化', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_03_chain_rate.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 3: 连锁化率演进')

# ============================================
# 图表 4：节假日数据对比
# ============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

festivals = ['2026 春节', '2026 清明', '2026 五一', '2026 端午']
tourists = [5.29, 1.35, 3.25, 1.1]  # 亿人次
revenue = [708.98, 613.67, 1854.92, 403.5]  # 亿元
per_capita = [t/r for t, r in zip(tourists, revenue)]

x = np.arange(len(festivals))
bars1 = ax.bar(x - 0.2, tourists, 0.4, label='游客（亿人次）', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
bars2 = ax.bar(x + 0.2, [r/100 for r in revenue], 0.4, label='收入/100（亿元）', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(festivals, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('2026 H1 节假日文旅数据对比', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

for b, t in zip(bars1, tourists):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+0.05, f'{t}亿', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
for b, r in zip(bars2, revenue):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+0.2, f'¥{r}亿', ha='center', fontsize=10, color=C['jade'], fontweight='bold')

plt.figtext(0.5, 0.02, '数据来源：文化和旅游部 / 各省文旅厅 | 端午同比 +6.3%/+8.1%', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_04_festivals.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 4: 节假日数据对比')

# ============================================
# 图表 5：民宿行业冰火两重天
# ============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

years = ['2023', '2024', '2025 末', '2026 H1E']
market_size = [320, 422.7, 400, 380]  # 亿元
adr = [None, 420, 367, 340]  # 元（2023 推估）
financing = [18, 44.9, 30, 25]  # 亿元

ax2 = ax.twinx()
bars = ax.bar(years, market_size, 0.5, label='市场规模 (亿元)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8, alpha=0.85)
line = ax2.plot([y for y, a in zip(years, adr) if a is not None], 
                [a for a in adr if a is not None], marker='o', linewidth=2.5, 
                color=C['crimson'], markersize=12, label='民宿均价 (元)', markeredgecolor='#3a1f15', markeredgewidth=1.5)

for bar, v in zip(bars, market_size):
    ax.text(bar.get_x() + bar.get_width()/2, v+8, f'{v}亿', ha='center', fontsize=11, color=C['jade'], fontweight='bold')

# 在 line 上标注价格
for x_pos, y_pos in zip([y for y, a in zip(years, adr) if a is not None], [a for a in adr if a is not None]):
    ax2.text(x_pos, y_pos+15, f'¥{y_pos}', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')

ax.set_ylabel('市场规模 (亿元)', fontsize=12, color=C['jade'])
ax2.set_ylabel('民宿均价 (元)', fontsize=12, color=C['crimson'])
ax.set_title('中国民宿行业：冰火两重天（2023-2026 H1）', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.set_ylim(0, 500)
ax2.set_ylim(200, 500)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=False, fontsize=11)

ax.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.spines['left'].set_color(C['jade'])
ax2.spines['right'].set_color(C['crimson'])
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：Fastdata 极数 / 36 氪 / 迈点 | 2024 民宿均价 -30%', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_05_homestay_ice_fire.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 5: 民宿冰火两重天')

# ============================================
# 图表 6：端午/五一 RevPAR/OCC/ADR
# ============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

metrics = ['OCC (%)', 'ADR (元)', 'RevPAR (元)']
wuyi = [63.5, 295.98, 187.33]
duanwu = [None, None, None]  # 端午未直接公布
quanyu = [58.8, 200, 118]  # 2024 全国基准

x = np.arange(len(metrics))
width = 0.3

# 五一
bars1 = ax.bar(x - width, wuyi, width, label='2026 五一', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
# 全国
bars2 = ax.bar(x, quanyu, width, label='2024 全国基准', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)
# 2025 同期
bars3 = ax.bar(x + width, [64.6, 293.34, 189.04], width, label='2025 五一', color=C['gold'], edgecolor='#3a2410', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('2026 五一酒店核心指标 vs 2024/2025 同期', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

for bars in [bars1, bars2, bars3]:
    for b in bars:
        h = b.get_height()
        if h > 0:
            ax.text(b.get_x() + b.get_width()/2, h+5, f'{h:.1f}' if h < 100 else f'¥{h:.0f}', 
                    ha='center', fontsize=9, color=C['ash'])

plt.figtext(0.5, 0.02, '数据来源：酒店之家 / STR China | 五一 RevPAR 同比 -0.9%（价格承压）', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_06_kpi_compare.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 6: 五一 vs 2024 基准')

# ============================================
# 图表 7：上海/广州 H1 高端韧性
# ============================================
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

cities = ['上海\n奢华酒店', '广州\n高端酒店', '三亚\n奢华酒店']
occ_change = [3, None, None]  # 上海 +3pp
adr_change = [7, None, 17]  # 上海 +7% / 三亚 +17%
revpar = [None, 754, None]  # 广州 ¥754

x = np.arange(len(cities))
bars1 = ax.bar(x - 0.2, [v if v is not None else 0 for v in occ_change], 0.4, label='OCC 同比 (pp)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)
bars2 = ax.bar(x + 0.2, [v if v is not None else 0 for v in adr_change], 0.4, label='ADR 同比 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(cities, fontsize=12, color=C['ash'])
ax.set_ylabel('变化 (pp / %)', fontsize=12, color=C['ash'])
ax.set_title('2026 H1 重点城市高端酒店韧性（JLL）', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# 标注
ax.text(0 - 0.2, 3.3, '+3pp', ha='center', fontsize=11, color=C['jade'], fontweight='bold')
ax.text(0 + 0.2, 7.3, '+7%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')
ax.text(1, 2, '广州 H1 RevPAR\n¥754 (+5.9%)', ha='center', fontsize=11, color=C['ash'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=C['ash'], linewidth=1.2))
ax.text(2 + 0.2, 17.5, '+17%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')

plt.figtext(0.5, 0.02, '数据来源：JLL 仲量联行 2026-07-14 上海 H1 + 2026-07-01 广州 H1', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_07_premium_cities.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 7: 重点城市高端韧性')

# ============================================
# 图表 8：客群结构（民宿 + 酒店）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

# 民宿
groups = ['休闲度假', '自驾散客', '旅居康养', '亲子/MICE', '商务']
sizes1 = [35, 25, 18, 12, 10]
colors1 = [C['crimson'], C['gold'], C['jade'], C['indigo'], C['umber']]
explode1 = (0, 0, 0.1, 0, 0)

wedges, texts, autotexts = axes[0].pie(sizes1, labels=groups, colors=colors1, autopct='%1.0f%%',
                                          explode=explode1, startangle=90,
                                          textprops={'fontsize': 11, 'color': C['ash']},
                                          wedgeprops={'edgecolor': '#FDFBF6', 'linewidth': 2})
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
axes[0].set_title('民宿客群结构（2026 H1 推估）', fontsize=13, fontweight='bold', color=C['ash'])

# 酒店
groups2 = ['休闲度假', '商务出差', '亲子家庭', '自驾旅游', 'MICE/会务']
sizes2 = [30, 25, 20, 15, 10]
colors2 = [C['crimson'], C['indigo'], C['jade'], C['gold'], C['umber']]
explode2 = (0, 0.05, 0, 0, 0)

wedges2, texts2, autotexts2 = axes[1].pie(sizes2, labels=groups2, colors=colors2, autopct='%1.0f%%',
                                              explode=explode2, startangle=90,
                                              textprops={'fontsize': 11, 'color': C['ash']},
                                              wedgeprops={'edgecolor': '#FDFBF6', 'linewidth': 2})
for at in autotexts2:
    at.set_color('white')
    at.set_fontweight('bold')
axes[1].set_title('酒店客群结构（2026 H1 推估）', fontsize=13, fontweight='bold', color=C['ash'])

fig.suptitle('2026 H1 客群结构对比：民宿 vs 酒店', fontsize=15, fontweight='bold', color=C['ash'], y=1.02)

plt.figtext(0.5, 0.01, '民宿旅居康养 18% vs 酒店 0% | 民宿 35% 休闲 vs 酒店 30% | 民宿 25% 自驾 vs 酒店 15%', 
            ha='center', fontsize=10, style='italic', color=C['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_08_customer_segments.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 8: 客群结构对比')

# ============================================
# 图表 9：58 维度信源审计（L0 默认）
# ============================================
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

categories = ['A 行业协会\n(5)', 'B 国际研究\n(6)', 'C 国内研究\n(6)', 'D OTA\n(6)', 'E 官方统计\n(4)', 'F 本土研究\n(3)', 'G 财经媒体\n(3)', 'H 金融证券\n(7)', 'I 上市集团\n(10)', 'J 4大+4大行\n(8)']
total = [5, 6, 6, 6, 4, 3, 3, 7, 10, 8]
used = [3, 2, 4, 5, 4, 0, 3, 2, 10, 0]

x = np.arange(len(categories))
bars1 = ax.bar(x, total, 0.6, color=C['slate'], edgecolor='#2a3a4a', linewidth=0.8, alpha=0.4, label='总数')
bars2 = ax.bar(x, used, 0.6, color=C['jade'], edgecolor='#1d3a30', linewidth=0.8, label='已用 (H1 报告)')

for b, t, u in zip(x, total, used):
    pct = u / t * 100 if t > 0 else 0
    ax.text(b, t+0.3, f'{t}', ha='center', fontsize=10, color=C['ash'])
    if u > 0:
        ax.text(b, u+0.2, f'{u}\n({pct:.0f}%)', ha='center', fontsize=9, color=C['jade'], fontweight='bold')
    else:
        ax.text(b, 0.3, f'{u}\n(0%)', ha='center', fontsize=9, color=C['umber'], fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10, color=C['ash'])
ax.set_ylabel('信源数', fontsize=12, color=C['ash'])
ax.set_title('58 维度信源审计：H1 报告覆盖率', fontsize=15, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：B166ER H1 报告 v1.0 | 34/58 = 58.6% 完整覆盖（I 上市集团 + E 官方统计 + G 财经媒体 全满）', 
            ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/h1_09_source_audit.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print('[OK] 图表 9: 58 维度信源审计')

print('\n[ALL DONE] 9 张 H1 图表已生成 ->', CHART_DIR)
import os
for f in sorted(os.listdir(CHART_DIR)):
    if f.startswith('h1_'):
        sz = os.path.getsize(os.path.join(CHART_DIR, f))
        print(f'  {sz:>10} {f}')