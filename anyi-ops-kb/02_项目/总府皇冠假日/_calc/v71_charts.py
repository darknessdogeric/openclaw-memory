# -*- coding: utf-8 -*-
"""v71：图表生成 + PIP 前期策划模板抽取
   图表：① 五年曲线 ② 品牌面积要求→可行房量 ③ 核心商圈实测房价带 ④ 净现值路径 ⑤ 停业方案对比"""
import io, os, sys, re, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
T = r"D:\B166ER-openclaw\workspace\.tmp"
FIG = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_figs"
os.makedirs(FIG, exist_ok=True)
LOG = open(os.path.join(T, "v71.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# 中文字体
CAND = ["Microsoft YaHei", "SimHei", "DengXian", "KaiTi", "Microsoft JhengHei", "SimSun"]
HAVE = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((c for c in CAND if c in HAVE), None)
if FONT:
    plt.rcParams["font.sans-serif"] = [FONT]
plt.rcParams["axes.unicode_minus"] = False
L("字体:", FONT)
J = json.load(open(os.path.join(T, "v70.json"), encoding="utf-8"))
BR = J["brands"]
C1, C2, C3, C4 = "#1F4E79", "#C00000", "#2E7D32", "#ED7D31"

def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    L("  →", name, "%.0f KB" % (os.path.getsize(p) / 1024))
    return p

# ══ 图1 2021—2026 五年曲线 ══
yrs = ["2021", "2022", "2023", "2024", "2025", "2026"]
revpar = [None, 217, None, 834, None, 215.5]
adr = [None, 534, None, 834, None, 292]
occ = [None, 40.7, None, None, 67.5, 73.8]
fig, ax = plt.subplots(figsize=(9, 4.6))
xs = list(range(6))
ax.plot(xs, [v if v else float("nan") for v in revpar], "o-", color=C1, lw=2.2, ms=7, label="成都五星级每间可售房收入（元）")
for i, v in enumerate(revpar):
    if v: ax.annotate(str(v), (i, v), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, color=C1)
ax.set_xticks(xs); ax.set_xticklabels(yrs, fontsize=11)
ax.set_ylabel("每间可售房收入（元）", fontsize=10)
ax.set_title("图1  成都五星级酒店每间可售房收入五年走势（2021—2026）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(alpha=.28, ls="--")
ax2 = ax.twinx()
ax2.bar(xs, [v if v else 0 for v in occ], color="#9DC3E6", alpha=.55, width=.45, zorder=0, label="平均出租率（%，全国口径）")
ax2.set_ylabel("出租率（%）", fontsize=10); ax2.set_ylim(0, 100)
for i, v in enumerate(occ):
    if v: ax2.annotate("%.1f%%" % v, (i, v), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8, color="#31708F")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9, framealpha=.9)
ax.set_ylim(0, 1050)
L("图1 注：2022 为十年最低；2024/2026 为不同口径（成都高端／全国），已在正文标注")
save(fig, "fig01_五年曲线.png")

# ══ 图2 品牌客房面积要求 → 可行房量 ══
items = [r for r in BR if r["key"] != "B01"]
items = sorted(items, key=lambda r: r["area_th"])
fig, ax = plt.subplots(figsize=(10, 5.2))
names = [r["name"].split("（")[0][:10] for r in items]
rooms = [r["n"] for r in items]
areas = [r["area_th"] for r in items]
bars = ax.bar(names, rooms, color=[C4 if r["key"] == "B12" else C1 for r in items], alpha=.88)
ax.axhline(402, color=C3, ls="--", lw=1.8)
ax.annotate("现状 402 间（单间套内 25.35 ㎡）", (len(names) - .4, 402), textcoords="offset points",
            xytext=(0, 6), ha="right", fontsize=10, color=C3, weight="bold")
for r, b in zip(items, bars):
    ax.annotate("%d 间\n%.0f㎡" % (r["n"], r["area_th"]), (r["name"].split("（")[0][:10], r["n"]),
                textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8)
ax.set_ylabel("按品牌面积要求可实现的房量（间）", fontsize=10)
ax.set_title("图2  品牌客房面积要求 → 总府可行房量（客房套内 10,192 ㎡，移卫耦合折损 8%）",
             fontsize=13, color=C1, pad=12, weight="bold")
plt.setp(ax.get_xticklabels(), rotation=32, ha="right", fontsize=9)
ax.grid(axis="y", alpha=.28, ls="--")
save(fig, "fig02_品牌面积与房量.png")

# ══ 图3 核心商圈实测房价带 ══
band = [("成都院子（古建）", 1500, 2500, "#8C8C8C"), ("成都居舍", 2000, 3000, C4),
        ("成都丽思卡尔顿", 1000, 2800, C1), ("成都瑞吉", 1291, 1393, C1),
        ("成都尼依格罗", 1180, 1400, C1), ("成都洲至奢选（棕榈泉）", 900, 1500, C1),
        ("成都华侨城/君悦", 1200, 2000, C1), ("成都华尔道夫", 1265, 3500, C1),
        ("总府现状（24个月均值）", 363.99, 427.4, C2)]
fig, ax = plt.subplots(figsize=(9.6, 5))
yl = list(range(len(band)))[::-1]
for i, (nm, lo, hi, c) in enumerate(band):
    ax.barh(yl[i], hi - lo, left=lo, color=c, alpha=.82, height=.55)
    ax.text(hi + 45, yl[i], "%d—%d" % (lo, hi), va="center", fontsize=9, color=c, weight="bold")
ax.set_yticks(yl); ax.set_yticklabels([b[0] for b in band], fontsize=10)
ax.set_xlabel("平均房价（元/间/晚）", fontsize=10)
ax.set_xlim(0, 4000)
ax.set_title("图3  春熙路核心商圈五星级及奢华酒店实测房价带（含总府现状对照）",
             fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="x", alpha=.28, ls="--")
save(fig, "fig03_实测房价带.png")

# ══ 图4 净现值路径 ══
labels = ["基准\n（12月全停+分区滚动+20年）", "①经营期\n20→30年", "②品牌方承担\n30%改造投入",
          "③锦江区补贴\n50万元", "④①+②", "⑤①+②+③"]
import importlib.util
spec = importlib.util.spec_from_file_location("v10", r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\v10_econ.py")
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
vals = [-3422.6, 254.7, 6451.0, 302.8, 6451.0, 6499.1]
fig, ax = plt.subplots(figsize=(9.6, 4.6))
bars = ax.bar(labels, vals, color=[C2 if v < 0 else C3 for v in vals], alpha=.88, width=.55)
for b, v in zip(bars, vals):
    ax.annotate("%+.0f" % v, (b.get_x() + b.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 6 if v >= 0 else -16), ha="center",
                fontsize=10, weight="bold", color=C3 if v >= 0 else C2)
ax.axhline(0, color="#555", lw=1)
ax.set_ylabel("净现值（万元，8% 折现，30 年口径）", fontsize=10)
ax.set_title("图4  净现值转正路径分解（皇冠假日现状续约基准情景）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="y", alpha=.28, ls="--")
plt.setp(ax.get_xticklabels(), fontsize=8.5)
save(fig, "fig04_净现值路径.png")

# ══ 图5 停业方案 ══
sl = ["全停业 4 月\n（原设想，不可行）", "全停业 12 月\n一次复业", "全停业 12 月\n分区滚动开业",
      "全停业 16 月\n分区滚动开业", "全停业 20 月\n分区滚动开业"]
sv = [None, -710.5, 254.7, -1608.3, -3444.8]
fig, ax = plt.subplots(figsize=(9, 4.4))
xs = range(len(sl))
bars = ax.bar(list(xs)[:1], [0], color="#BFBFBF", alpha=.8)
bars = ax.bar(list(xs)[1:], sv[1:], color=[C2 if v < 0 else C3 for v in sv[1:]], alpha=.88, width=.55)
for i, v in enumerate(sv):
    if v is None:
        ax.annotate("消防+机电工程\n12 个月不可压缩", (0, 120), ha="center", fontsize=9, color="#8C8C8C", weight="bold")
    else:
        ax.annotate("%+.0f" % v, (i, v), textcoords="offset points", xytext=(0, 6 if v >= 0 else -16),
                    ha="center", fontsize=10, weight="bold", color=C3 if v >= 0 else C2)
ax.set_xticks(list(xs)); ax.set_xticklabels(sl, fontsize=8.8)
ax.set_ylabel("净现值（万元，30 年口径）", fontsize=10)
ax.set_title("图5  停业方案与净现值（停业月数是最大的单一变量）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="y", alpha=.28, ls="--")
save(fig, "fig05_停业方案.png")

L("图表完成")
L("DONE")
