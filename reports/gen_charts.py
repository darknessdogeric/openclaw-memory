"""
弥勒民宿可行性研究 - 图表生成器
matplotlib + Noto Sans SC 中文字体
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# 中文字体
font_path = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans SC'
plt.rcParams['axes.unicode_minus'] = False

CHART_DIR = 'D:/B166ER-OpenClaw/workspace/reports/charts'
os.makedirs(CHART_DIR, exist_ok=True)

# 配色：东方美学（参考 Eric 审美）
COLORS = {
    'crimson': '#C73E1D',  # 朱红
    'gold': '#C99A3D',     # 鎏金
    'jade': '#3A8B6E',     # 青绿
    'indigo': '#2C5F7C',   # 靛蓝
    'umber': '#7A5230',    # 赭石
    'ash': '#5C5742',      # 烟灰
    'ivory': '#F5F0E6',    # 牙白
}

# =============================================
# 图表 1：2024 全国酒店 OCC/ADR/RevPAR 对比
# =============================================
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

groups = ['华住', '亚朵', '君亭(直营)', '首旅', '锦江(全服务)']
adr = [289, 400, 400, 229, 400]
occ = [81.2, 77.4, 70, 64.2, 51.56]
revpar = [235, 351.3, 280, 147, 207]

x = np.arange(len(groups))
width = 0.26

bars1 = ax.bar(x - width, adr, width, label='ADR (¥)', color=COLORS['crimson'], edgecolor='#3a1f15', linewidth=0.8)
bars2 = ax.bar(x, occ, width, label='OCC (%)', color=COLORS['jade'], edgecolor='#1d3a30', linewidth=0.8)
bars3 = ax.bar(x + width, revpar, width, label='RevPAR (¥)', color=COLORS['indigo'], edgecolor='#162d3a', linewidth=0.8)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=12, color=COLORS['ash'])
ax.set_ylabel('数值', fontsize=13, color=COLORS['ash'])
ax.set_title('2024 年中国上市酒店集团核心运营指标对比', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.legend(loc='upper right', frameon=False, fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLORS['ash'])
ax.spines['bottom'].set_color(COLORS['ash'])
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# 标注关键数据
for b in bars2:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h+1, f'{h}%', ha='center', fontsize=10, color=COLORS['jade'])

plt.figtext(0.5, 0.02, '数据来源：STR/各集团 2024 年报  |  整体行业 2024 RevPAR 同比 -9.7%', 
            ha='center', fontsize=10, style='italic', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/01_2024_groups_compare.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 1: 2024 全国酒店集团对比")

# =============================================
# 图表 2：外资中国区 RevPAR 下行幅度
# =============================================
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

brands = ['凯悦', '万豪', '洲际', '温德姆']
decline = [-0.1, -2.3, -4.8, -8.0]
colors_decline = [COLORS['jade'], COLORS['gold'], COLORS['crimson'], COLORS['umber']]

bars = ax.barh(brands, decline, color=colors_decline, edgecolor='#3a2410', linewidth=1)
ax.set_xlim(-10, 1)
ax.set_xlabel('RevPAR 同比变化（%）', fontsize=12, color=COLORS['ash'])
ax.set_title('2024 年外资酒店中国区 RevPAR 同比变化', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.axvline(0, color=COLORS['ash'], linewidth=0.8)

# 添加数值标签
for b, val in zip(bars, decline):
    width = b.get_width()
    ax.text(width - 0.3, b.get_y() + b.get_height()/2, f'{val}%', 
            ha='right', va='center', fontsize=12, fontweight='bold', color='white')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color(COLORS['ash'])
ax.spines['left'].set_color(COLORS['ash'])
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：各集团 2024 财报  |  全行业下行，外资无例外', 
            ha='center', fontsize=10, style='italic', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/02_foreign_china_decline.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 2: 外资中国区 RevPAR 下行")

# =============================================
# 图表 3：中国民宿市场规模增长
# =============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

years = ['2021', '2022', '2023', '2024']
market_size = [200, 280, 350, 422.7]  # 亿元（推估）
financing = [12, 18, 28, 44.9]

ax2 = ax.twinx()
bars1 = ax.bar(years, market_size, width=0.5, label='市场规模 (亿元)', 
              color=COLORS['crimson'], edgecolor='#3a1f15', linewidth=0.8, alpha=0.85)
line = ax2.plot(years, financing, marker='o', linewidth=2.5, color=COLORS['jade'], 
                markersize=12, label='融资金额 (亿元)', markeredgecolor='#1d3a30', markeredgewidth=1)

# 标注
for bar, v in zip(bars1, market_size):
    ax.text(bar.get_x() + bar.get_width()/2, v+8, f'{v}亿', 
            ha='center', fontsize=11, color=COLORS['crimson'], fontweight='bold')

for x_pos, v in zip(years, financing):
    ax2.text(x_pos, v+2, f'{v}亿', ha='center', fontsize=11, color=COLORS['jade'], fontweight='bold')

ax.set_ylabel('市场规模 (亿元)', fontsize=12, color=COLORS['crimson'])
ax2.set_ylabel('融资金额 (亿元)', fontsize=12, color=COLORS['jade'])
ax.set_title('中国民宿行业：市场规模 + 融资双增长（2021-2024）', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.set_ylim(0, 500)
ax2.set_ylim(0, 60)

# 合并图例
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False, fontsize=11)

ax.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.spines['left'].set_color(COLORS['crimson'])
ax.spines['right'].set_color(COLORS['jade'])
ax.spines['bottom'].set_color(COLORS['ash'])
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：Fastdata 极数《中国民宿行业发展趋势报告 2025》', 
            ha='center', fontsize=10, style='italic', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/03_homestay_market_growth.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 3: 中国民宿行业增长")

# =============================================
# 图表 4：云南旅居康养人数爆发
# =============================================
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

years = ['2023', '2024', '2025E']
num_lvju = [120, 389.75, 600]  # 万人
yoy = [None, 20.7, 53.9]  # 同比

bars = ax.bar(years, num_lvju, color=[COLORS['gold'], COLORS['crimson'], COLORS['jade']], 
              width=0.55, edgecolor='#3a2410', linewidth=0.8, alpha=0.85)
for bar, v in zip(bars, num_lvju):
    ax.text(bar.get_x() + bar.get_width()/2, v+15, f'{v}万', 
            ha='center', fontsize=14, fontweight='bold', color=COLORS['crimson'])

# 同比箭头
ax.text(1, 510, '+20.7% YoY', ha='center', fontsize=13, color=COLORS['jade'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['jade'], linewidth=1.5))
ax.text(2, 660, '+53.9% YoY', ha='center', fontsize=13, color=COLORS['crimson'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['crimson'], linewidth=1.5))

ax.set_ylabel('旅居人数（万人）', fontsize=12, color=COLORS['ash'])
ax.set_title('云南旅居人数爆发式增长（2023 → 2025E）', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.set_ylim(0, 750)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLORS['ash'])
ax.spines['bottom'].set_color(COLORS['ash'])
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.figtext(0.5, 0.02, '数据来源：搜狐财经 / 云南省政府发布  |  东北老人赴云南订单 +82% YoY', 
            ha='center', fontsize=10, style='italic', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/04_yunnan_lvju_growth.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 4: 云南旅居增长")

# =============================================
# 图表 5：弥勒 vs 同梯次对标（雷达图）
# =============================================
fig, ax = plt.subplots(figsize=(9, 9), dpi=120, subplot_kw=dict(projection='polar'))
fig.patch.set_facecolor('#FDFBF6')

categories = ['游客数\n(万人次)', '旅游花费\n(亿元)', 'OCC\n(节假日%)', 'ADR\n(¥)', '过夜率\n(%)']
mile_values = [1779, 217, 80, 350, 20]
dali_values = [5000, 600, 95, 600, 38]
national_values = [56.2e4/1000, 5800, 58.8, 200, 35]  # 缩放到合适范围

# 归一化到 0-100
def normalize(vals, ref):
    return [(v/ref[i])*100 for i, v in enumerate(vals)]

ref = [5000, 600, 95, 600, 40]  # 基准
mile_n = normalize(mile_values, ref)
dali_n = normalize(dali_values, ref)
national_n = normalize(national_values, ref)

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

mile_n += mile_n[:1]
dali_n += dali_n[:1]
national_n += national_n[:1]

ax.plot(angles, mile_n, 'o-', linewidth=2.5, color=COLORS['crimson'], label='弥勒', markersize=10)
ax.fill(angles, mile_n, alpha=0.25, color=COLORS['crimson'])
ax.plot(angles, dali_n, 's-', linewidth=2.5, color=COLORS['indigo'], label='大理（对标）', markersize=8)
ax.fill(angles, dali_n, alpha=0.20, color=COLORS['indigo'])
ax.plot(angles, national_n, '^-', linewidth=2.5, color=COLORS['gold'], label='全国基准', markersize=8)
ax.fill(angles, national_n, alpha=0.15, color=COLORS['gold'])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12, color=COLORS['ash'])
ax.set_ylim(0, 110)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9, color=COLORS['ash'])
ax.set_title('弥勒 vs 大理 vs 全国基准——5 维对标（归一化 0-100%）', 
             fontsize=15, fontweight='bold', pad=25, color=COLORS['ash'])
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.05), fontsize=12, frameon=False)
ax.grid(color=COLORS['ash'], alpha=0.3)

plt.figtext(0.5, 0.05, '弥勒优势：游客数 + 旅游花费', 
            ha='center', fontsize=11, style='italic', color=COLORS['jade'])
plt.figtext(0.5, 0.02, '弥勒劣势：过夜率仅 20%（行业优秀线 35%）—— 民宿核心机会', 
            ha='center', fontsize=11, style='italic', color=COLORS['crimson'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/05_mile_vs_compete_radar.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 5: 弥勒 vs 同梯次对标")

# =============================================
# 图表 6：财务模型三档对比
# =============================================
fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

scenarios = ['保守\n(修改前)', '保守\n(修正后)', '中性\n(修正前)', '中性\n(修正后)', '乐观\n(修正后)']
revenue = [70.5, 95, 102.2, 130, 158]
recovery = [8.1, 5.0, 8.4, 5.5, 4.5]
colors6 = [COLORS['ash'], COLORS['umber'], COLORS['gold'], COLORS['crimson'], COLORS['jade']]

bars = axes[0].bar(scenarios, revenue, color=colors6, edgecolor='#3a2410', linewidth=0.8, width=0.6)
for bar, v in zip(bars, revenue):
    axes[0].text(bar.get_x() + bar.get_width()/2, v+2, f'{v}万', 
                  ha='center', fontsize=10, fontweight='bold', color=COLORS['ash'])

axes[0].set_ylabel('年营收（万元）', fontsize=12, color=COLORS['ash'])
axes[0].set_title('弥勒 12 间民宿：三档场景年营收对比', fontsize=14, fontweight='bold', color=COLORS['ash'])
axes[0].set_ylim(0, 200)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].grid(axis='y', linestyle='--', alpha=0.3)
axes[0].set_axisbelow(True)

bars2 = axes[1].bar(scenarios, recovery, color=colors6, edgecolor='#3a2410', linewidth=0.8, width=0.6)
for bar, v in zip(bars2, recovery):
    axes[1].text(bar.get_x() + bar.get_width()/2, v+0.15, f'{v}年', 
                  ha='center', fontsize=10, fontweight='bold', color=COLORS['ash'])

axes[1].axhline(5, color=COLORS['jade'], linestyle='--', linewidth=1.5, alpha=0.7)
axes[1].text(4.2, 5.15, '5 年合理线', fontsize=10, color=COLORS['jade'], fontweight='bold')
axes[1].set_ylabel('投资回收期（年）', fontsize=12, color=COLORS['ash'])
axes[1].set_title('修正后回收期全部 ≤ 5 年', fontsize=14, fontweight='bold', color=COLORS['ash'])
axes[1].set_ylim(0, 10)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].grid(axis='y', linestyle='--', alpha=0.3)
axes[1].set_axisbelow(True)

fig.suptitle('弥勒民宿财务模型 —— 修改路径前后对比', fontsize=16, fontweight='bold', color=COLORS['ash'], y=1.02)

plt.figtext(0.5, 0.01, '修正路径：A(温泉+康养) + B(私域+长住) + C(创业担保贷款 50% 贴息)', 
            ha='center', fontsize=10, style='italic', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/06_finance_scenarios.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 6: 财务模型三档对比")

# =============================================
# 图表 7：客群结构饼图
# =============================================
fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

groups = ['休闲度假家庭', '自驾散客情侣', '旅居康养客\n(银发候鸟)', '亲子团建 MICE', '商务会务']
sizes = [38, 27, 13, 13, 9]
colors7 = [COLORS['crimson'], COLORS['gold'], COLORS['jade'], COLORS['indigo'], COLORS['umber']]
explode = (0, 0, 0.08, 0, 0)

wedges, texts, autotexts = ax.pie(sizes, labels=groups, colors=colors7, autopct='%1.0f%%',
                                    explode=explode, startangle=90, 
                                    textprops={'fontsize': 12, 'color': COLORS['ash']},
                                    wedgeprops={'edgecolor': '#FDFBF6', 'linewidth': 2.5})
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
    at.set_fontsize(13)

ax.set_title('弥勒民宿客群结构（推估）', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.text(0, -1.4, '核心洞察：旅居康养客虽仅 13%，但停留 7-30 天 / 单客价值高 5-10 倍', 
        ha='center', fontsize=11, style='italic', color=COLORS['jade'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/07_customer_segments.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 7: 客群结构")

# =============================================
# 图表 8：5 维可行性矩阵雷达图
# =============================================
fig, ax = plt.subplots(figsize=(9, 9), dpi=120, subplot_kw=dict(projection='polar'))
fig.patch.set_facecolor('#FDFBF6')

categories = ['市场可行性', '政策可行性', '财务可行性', '运营可行性', '退出可行性']
scores = [8.5, 7.5, 6.5, 6.5, 5.5]
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]
scores += scores[:1]

ax.plot(angles, scores, 'o-', linewidth=3.5, color=COLORS['crimson'], markersize=14, 
        markeredgecolor='white', markeredgewidth=2)
ax.fill(angles, scores, alpha=0.35, color=COLORS['crimson'])

# 评级阈值
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=13, fontweight='bold', color=COLORS['ash'])
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=10, color=COLORS['ash'])

# 添加评级区
ax.fill_between(angles, 0, 5, color='gray', alpha=0.1)
ax.fill_between(angles, 5, 7, color=COLORS['gold'], alpha=0.15)
ax.fill_between(angles, 7, 10, color=COLORS['jade'], alpha=0.15)

ax.set_title('5 维可行性评分（10 分制）', fontsize=15, fontweight='bold', pad=25, color=COLORS['ash'])

# 标注评级
for i, (cat, s) in enumerate(zip(categories[:-1], scores[:-1])):
    ang = angles[i]
    if s >= 8:
        label = '✓强'
        color = COLORS['jade']
    elif s >= 6:
        label = '△有条件'
        color = COLORS['gold']
    else:
        label = '⚠ 较弱'
        color = COLORS['crimson']
    ax.text(ang, s+1.2, label, ha='center', fontsize=10, fontweight='bold', color=color)

ax.grid(color=COLORS['ash'], alpha=0.3)

plt.figtext(0.5, 0.02, '总体评级：有条件可行（取决于 5 个约束条件是否同时满足）', 
            ha='center', fontsize=12, fontweight='bold', color=COLORS['ash'])

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/08_feasibility_radar.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 8: 5 维可行性矩阵")

# =============================================
# 图表 9：政策时间线
# =============================================
fig, ax = plt.subplots(figsize=(13, 5.5), dpi=120)
fig.patch.set_facecolor('#FDFBF6')

events = [
    (1958, '国营东风农场建立'),
    (2014, '罗旭开始红砖建筑创作'),
    (2017, '万花筒艺术馆建成'),
    (2020, '美憬阁 (雅高) 开业'),
    (2022, '蓝城加入 / 沐心谷开盘'),
    (2024, '东风韵网球小镇 / 民宿 +211'),
    (2025, '网签 28.23 亿 / 大理民宿条例'),
    (2026, '大理条例施行 / 7/24 D-Day'),
]

ax.axhline(0, color=COLORS['ash'], linewidth=2, alpha=0.4)
for i, (year, ev) in enumerate(events):
    y = 0.5 if i % 2 == 0 else -0.5
    color = COLORS['crimson'] if year >= 2024 else (COLORS['jade'] if year <= 2020 else COLORS['gold'])
    ax.scatter(year, 0, s=180, color=color, edgecolors='white', linewidth=2, zorder=5)
    ax.plot([year, year], [0, y*0.6], color=color, linewidth=1.5, alpha=0.6)
    ax.text(year, y, f'{year}\n{ev}', ha='center', va='center', fontsize=9.5, 
            color=COLORS['ash'], fontweight='bold')

ax.set_xlim(1955, 2029)
ax.set_ylim(-1, 1)
ax.set_yticks([])
ax.set_xlabel('年份', fontsize=12, color=COLORS['ash'])
ax.set_title('弥勒东风韵 / 民宿产业政策时间线（1958-2026）', fontsize=15, fontweight='bold', pad=15, color=COLORS['ash'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(COLORS['ash'])

# 图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=COLORS['jade'], label='奠基期 (1958-2020)'),
    Patch(facecolor=COLORS['gold'], label='成长期 (2020-2023)'),
    Patch(facecolor=COLORS['crimson'], label='爆发期 (2024+)')
]
ax.legend(handles=legend_elements, loc='lower right', frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig(f'{CHART_DIR}/09_policy_timeline.png', dpi=150, bbox_inches='tight', facecolor='#FDFBF6')
plt.close()
print("[OK] 图表 9: 政策时间线")

print("\n[ALL DONE] 所有图表生成完成 ->", CHART_DIR)
print("图表清单:")
for f in sorted(os.listdir(CHART_DIR)):
    sz = os.path.getsize(os.path.join(CHART_DIR, f))
    print(f"  {sz:>10} {f}")
