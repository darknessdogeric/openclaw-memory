"""2026 H1 报告 v2.0 - 9 张图表（同比基准 = 2025 同期）"""
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

C = {
    'crimson': '#C73E1D', 'gold': '#C99A3D', 'jade': '#3A8B6E',
    'indigo': '#2C5F7C', 'umber': '#7A5230', 'ash': '#5C5742',
    'slate': '#4A5A6A'
}

# 1: 内资前 5
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
groups = ['锦江酒店', '华住集团', '首旅酒店', '亚朵集团', '格林酒店']
revpar_yoy = [35, 33, 32, 28, 28]
adr = [298, 312, 285, 571, 228]
x = np.arange(len(groups))
b1 = ax.bar(x-0.2, revpar_yoy, 0.4, label='2026 春节 RevPAR 同比 2025 春节 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
b2 = ax.bar(x+0.2, [a/10 for a in adr], 0.4, label='2026 春节 ADR/10 (元)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('内资前 5 上市酒店集团 2026 春节业绩（同比 2025 春节）', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
for b in b1:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f'+{int(b.get_height())}%', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
for b, a in zip(b2, adr):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+1, f'¥{a}', ha='center', fontsize=10, color=C['jade'], fontweight='bold')
plt.figtext(0.5, 0.02, '数据：2026-Spring-Festival 报告 4.4 节 | 亚朵替换东呈', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_01_internal_top5.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 1')

# 2: 外资前 5
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
groups = ['万豪国际', '洲际酒店', '希尔顿', '雅高集团', '凯悦酒店']
revpar_yoy = [28, 26, 27, 24, 22]
revpar = [493, 419, 446, 375, 938]
x = np.arange(len(groups))
b1 = ax.bar(x-0.2, revpar_yoy, 0.4, label='2026 春节 RevPAR 同比 2025 (%)', color=C['indigo'], edgecolor='#162d3a', linewidth=0.8)
b2 = ax.bar(x+0.2, [r/15 for r in revpar], 0.4, label='2026 春节 RevPAR/15 (元)', color=C['gold'], edgecolor='#3a2410', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('外资前 5 上市酒店集团 2026 春节业绩（同比 2025 春节）', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
for b in b1:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f'+{int(b.get_height())}%', ha='center', fontsize=10, color=C['indigo'], fontweight='bold')
for b, r in zip(b2, revpar):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+1, f'¥{r}', ha='center', fontsize=10, color=C['gold'], fontweight='bold')
plt.figtext(0.5, 0.02, '数据：2026-Spring-Festival 报告 4.4 节', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_02_foreign_top5.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 2')

# 3: 连锁化率
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
years = ['2022', '2023', '2024', '2025 末']
chain = [35, 38, 40.09, 41.80]
top10 = [50, 54, 57, 59.38]
ax2 = ax.twinx()
bars = ax.bar(years, chain, 0.5, label='连锁化率 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8, alpha=0.85)
line = ax2.plot(years, top10, marker='o', linewidth=2.5, color=C['jade'], markersize=12, label='TOP10 占连锁 (%)', markeredgecolor='#1d3a30', markeredgewidth=1.5)
for bar, v in zip(bars, chain):
    ax.text(bar.get_x()+bar.get_width()/2, v+0.5, f'{v}%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')
for x_pos, v in zip(years, top10):
    ax2.text(x_pos, v+1, f'{v}%', ha='center', fontsize=11, color=C['jade'], fontweight='bold')
ax.set_ylabel('连锁化率 (%)', fontsize=12, color=C['crimson'])
ax2.set_ylabel('TOP10 集中度 (%)', fontsize=12, color=C['jade'])
ax.set_title('中国酒店连锁化率与 TOP10 集中度演进（2022-2025）', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.set_ylim(0, 50); ax2.set_ylim(0, 70)
L1, l1 = ax.get_legend_handles_labels(); L2, l2 = ax2.get_legend_handles_labels()
ax.legend(L1+L2, l1+l2, loc='upper left', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False); ax2.spines['top'].set_visible(False)
ax.spines['left'].set_color(C['crimson']); ax2.spines['right'].set_color(C['jade'])
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
plt.figtext(0.5, 0.02, '数据：2026-04 月度报告 / 迈点 | 历年同期', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_03_chain_rate.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 3')

# 4: 节假日对比
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
fest = ['2026 春节', '2026 清明', '2026 五一', '2026 端午']
t26 = [5.29, 1.35, 3.25, 1.24]
t25 = [5.0, 1.27, 3.14, 1.1]
r26 = [708.98, 613.67, 1854.92, 444.56]
r25 = [680, 580, 1802, 403.5]
x = np.arange(len(fest)); w = 0.18
ax.bar(x-0.21, t25, w, label='2025 同期游客(亿)', color=C['slate'], alpha=0.5, edgecolor='#2a3a4a', linewidth=0.8)
ax.bar(x, t26, w, label='2026 游客(亿)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
ax.bar(x+0.21, [r/100 for r in r25], w, label='2025 同期收入/100(亿)', color=C['umber'], alpha=0.5, edgecolor='#3a1f15', linewidth=0.8)
ax.bar(x+0.42, [r/100 for r in r26], w, label='2026 收入/100(亿)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)
ax.set_xticks(x+0.1); ax.set_xticklabels(fest, fontsize=11, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('2026 H1 节假日文旅数据 vs 2025 同期', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper left', frameon=False, fontsize=9, ncol=2)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
plt.figtext(0.5, 0.02, '数据：文旅部 | 端午 +4.4%/+4.0% (2025/2026)', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_04_festivals.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 4')

# 5: 2026 五一 vs 2025 五一
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
metrics = ['酒店 OCC (%)', '酒店 ADR (元)', '酒店 RevPAR (元)']
y25 = [71.42, 448.58, 320.0]
y26 = [63.5, 295.98, 187.33]
x = np.arange(len(metrics)); w = 0.35
b1 = ax.bar(x-0.2, y25, w, label='2025 五一(订单来了)', color=C['gold'], edgecolor='#3a2410', linewidth=0.8, alpha=0.85)
b2 = ax.bar(x+0.2, y26, w, label='2026 五一(酒店之家)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('2026 五一酒店指标 vs 2025 五一：高基数效应', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
for i, (b1_, b2_, v1, v2) in enumerate(zip(b1, b2, y25, y26)):
    h1 = b1_.get_height(); h2 = b2_.get_height()
    if i == 0:
        ax.text(b1_.get_x()+b1_.get_width()/2, h1+1.5, f'{v1}%', ha='center', fontsize=10, color=C['gold'], fontweight='bold')
        ax.text(b2_.get_x()+b2_.get_width()/2, h2+1.5, f'{v2}%\n-7.92pp', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
    else:
        ax.text(b1_.get_x()+b1_.get_width()/2, h1+10, f'¥{v1:.0f}', ha='center', fontsize=10, color=C['gold'], fontweight='bold')
        delta = (v2-v1)/v1*100
        ax.text(b2_.get_x()+b2_.get_width()/2, h2+10, f'¥{v2:.0f}\n{delta:+.0f}%', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
plt.figtext(0.5, 0.02, '2025 五一历史高位 → 2026 高基数效应', ha='center', fontsize=10, style='italic', color=C['crimson'], fontweight='bold')
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_05_wuyi.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 5')

# 6: 端午对比
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
m = ['客流(亿)', '收入(亿)']
v25 = [1.1, 403.5]; v26 = [1.24, 444.56]
x = np.arange(len(m)); w = 0.35
ax.bar(x-0.2, v25, w, label='2025 端午', color=C['slate'], edgecolor='#2a3a4a', linewidth=0.8, alpha=0.7)
ax.bar(x+0.2, v26, w, label='2026 端午', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(m, fontsize=12, color=C['ash'])
ax.set_ylabel('数值', fontsize=12, color=C['ash'])
ax.set_title('2026 端午 vs 2025 端午：温和增长', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper left', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
for i, (v1, v2) in enumerate(zip(v25, v26)):
    delta = (v2-v1)/v1*100
    ax.text(i-0.2, v1*1.05, f'{v1}', ha='center', fontsize=10, color=C['slate'], fontweight='bold')
    ax.text(i+0.2, v2*1.05, f'{v2}\n+{delta:.1f}%', ha='center', fontsize=10, color=C['crimson'], fontweight='bold')
plt.figtext(0.5, 0.02, '同比基准 = 2025 端午', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_06_duanwu.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 6')

# 7: 重点城市高端韧性
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
cities = ['上海\n奢华酒店', '广州\n高端酒店', '三亚\n奢华酒店']
occ = [3, 0, 0]; adr = [7, 0, 17]
x = np.arange(len(cities))
ax.bar(x-0.2, occ, 0.4, label='OCC 同比 2025 H1 (pp)', color=C['jade'], edgecolor='#1d3a30', linewidth=0.8)
ax.bar(x+0.2, adr, 0.4, label='ADR 同比 2025 H1 (%)', color=C['crimson'], edgecolor='#3a1f15', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(cities, fontsize=12, color=C['ash'])
ax.set_ylabel('变化 (pp / %)', fontsize=12, color=C['ash'])
ax.set_title('2026 H1 重点城市高端酒店韧性（同比 2025 H1）', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
ax.text(0-0.2, 3.3, '+3pp', ha='center', fontsize=11, color=C['jade'], fontweight='bold')
ax.text(0+0.2, 7.3, '+7%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')
ax.text(1, 2, '广州 H1 RevPAR\n¥754 (+5.9%)', ha='center', fontsize=11, color=C['ash'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=C['ash'], linewidth=1.2))
ax.text(2+0.2, 17.5, '+17%', ha='center', fontsize=11, color=C['crimson'], fontweight='bold')
plt.figtext(0.5, 0.02, 'JLL 仲量联行 2026-07-14 上海 + 2026-07-01 广州', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_07_premium.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 7')

# 8: 客群结构
fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
g1 = ['休闲度假', '自驾散客', '旅居康养', '亲子/MICE', '商务']
s1 = [35, 25, 18, 12, 10]
c1 = [C['crimson'], C['gold'], C['jade'], C['indigo'], C['umber']]
w1, t1, a1 = axes[0].pie(s1, labels=g1, colors=c1, autopct='%1.0f%%', startangle=90, textprops={'fontsize': 11, 'color': C['ash']}, wedgeprops={'edgecolor': '#FDFBF6', 'linewidth': 2})
for at in a1: at.set_color('white'); at.set_fontweight('bold')
axes[0].set_title('民宿客群结构 (2026 H1)', fontsize=13, fontweight='bold', color=C['ash'])
g2 = ['休闲度假', '商务出差', '亲子家庭', '自驾旅游', 'MICE/会务']
s2 = [30, 25, 20, 15, 10]
c2 = [C['crimson'], C['indigo'], C['jade'], C['gold'], C['umber']]
w2, t2, a2 = axes[1].pie(s2, labels=g2, colors=c2, autopct='%1.0f%%', startangle=90, textprops={'fontsize': 11, 'color': C['ash']}, wedgeprops={'edgecolor': '#FDFBF6', 'linewidth': 2})
for at in a2: at.set_color('white'); at.set_fontweight('bold')
axes[1].set_title('酒店客群结构 (2026 H1)', fontsize=13, fontweight='bold', color=C['ash'])
fig.suptitle('2026 H1 客群结构对比：民宿 vs 酒店', fontsize=15, fontweight='bold', color=C['ash'], y=1.02)
plt.figtext(0.5, 0.01, '民宿旅居康养 18% vs 酒店 0%', ha='center', fontsize=10, style='italic', color=C['ash'])
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_08_segments.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 8')

# 9: 信源审计
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')
cats = ['A\n(5)', 'B\n(6)', 'C\n(6)', 'D\n(6)', 'E\n(4)', 'F\n(3)', 'G\n(3)', 'H\n(7)', 'I\n(10)', 'J\n(8)']
total = [5, 6, 6, 6, 4, 3, 3, 7, 10, 8]
used = [3, 2, 4, 5, 4, 0, 3, 2, 10, 0]
x = np.arange(len(cats))
ax.bar(x, total, 0.6, color=C['slate'], edgecolor='#2a3a4a', linewidth=0.8, alpha=0.4, label='总数')
ax.bar(x, used, 0.6, color=C['jade'], edgecolor='#1d3a30', linewidth=0.8, label='已用 (v2.0)')
for b, t, u in zip(x, total, used):
    pct = u/t*100 if t > 0 else 0
    ax.text(b, t+0.3, f'{t}', ha='center', fontsize=10, color=C['ash'])
    if u > 0:
        ax.text(b, u+0.2, f'{u}\n({pct:.0f}%)', ha='center', fontsize=9, color=C['jade'], fontweight='bold')
    else:
        ax.text(b, 0.3, f'{u}\n(0%)', ha='center', fontsize=9, color=C['umber'], fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=10, color=C['ash'])
ax.set_ylabel('信源数', fontsize=12, color=C['ash'])
ax.set_title('58 维度信源审计：v2.0 H1 报告覆盖率', fontsize=14, fontweight='bold', pad=15, color=C['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.3); ax.set_axisbelow(True)
plt.figtext(0.5, 0.02, '34/58 = 58.6% | v2.0 所有同比基于 2025 同期', ha='center', fontsize=10, style='italic', color=C['crimson'], fontweight='bold')
plt.tight_layout(); plt.savefig(f'{CHART_DIR}/h1v2_09_audit.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6'); plt.close()
print('[OK] 9')

print('\n[DONE] 9 张 v2.0 H1 图表已生成')
for f in sorted(os.listdir(CHART_DIR)):
    if f.startswith('h1v2_'):
        print(f'  {os.path.getsize(os.path.join(CHART_DIR, f)):>8} {f}')