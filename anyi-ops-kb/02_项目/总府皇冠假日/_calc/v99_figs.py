# -*- coding: utf-8 -*-
"""v99：图表生成 + 测算附表（Excel）—— 数据源 v98.json"""
import json, os, io, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

T = r"D:\B166ER-openclaw\workspace\.tmp"
FIG = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\fig"
os.makedirs(FIG, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

D = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
R, S, B, BE = D["results"], D["sensitivity"], D["base"], D["breakeven"]

# ── 中文字体 ──
cands = ["Microsoft YaHei", "SimHei", "Microsoft JhengHei", "DengXian", "SimSun",
         "Noto Sans CJK SC", "Source Han Sans CN"]
have = {f.name for f in fm.fontManager.ttflist}
font = next((c for c in cands if c in have), None)
if font is None:
    for f in fm.findSystemFonts():
        if "msyh" in f.lower() or "simhei" in f.lower():
            font = fm.FontProperties(fname=f).get_name(); break
plt.rcParams["font.sans-serif"] = [font] if font else ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
print("字体:", font)

INK = "#1F2933"; MUT = "#7B8794"; C = ["#2E6E8E", "#C96A2E", "#3F7D58", "#8A5B8C"]
GRID = {"color": "#E4E7EB", "lw": .8}

def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ", name, round(os.path.getsize(p) / 1024), "KB")

# ══ 图1 安全隐患趋势：爆管次数 + 关键系统服役年限 ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))
yr = ["2024", "2025", "2026(至11月)"]; br = [6, 17, 20]
b = ax1.bar(yr, br, color=["#9DB4C0", C[1], "#A03A2E"], width=.55)
for r, v in zip(b, br):
    ax1.text(r.get_x() + r.get_width() / 2, v + .5, str(v), ha="center", fontsize=11, weight="bold", color=INK)
ax1.set_title("供水管网爆管次数（三年累计 43 次）", fontsize=11.5, color=INK, weight="bold")
ax1.set_ylabel("年爆管次数（次）", fontsize=10, color=MUT)
ax1.set_ylim(0, 24); ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9.5)
for i, v in enumerate(br):
    ax1.text(i, -1.8, "桩号 45 条记录", ha="center", fontsize=8, color=MUT) if i == 0 else None
items = [("冷水管网", 1995, 30), ("消防管网/喷淋", 1996, 29), ("空调末端 FCU 542 台", 1996, 29),
         ("干式变压器 4 台", 1996, 29), ("低压配电柜 34 面", 1996, 29),
         ("电梯 14 台", 1996, 29), ("冷源 R11 机组 4 台", 1996, 29)]
labs = [i[0] for i in items]; yrs = [i[1] for i in items]
y2 = ax2.barh(range(len(items)), yrs, color=[C[1] if y < 1996 else "#B07A3C" for y in yrs], height=.6)
for i, (n, y, d) in enumerate(items):
    ax2.text(y + .4, i, f"1996 投用 · 超期 {d-1} 年" if y == 1996 else f"1995 敷设 · 超期 {d-1} 年",
             va="center", fontsize=8.6, color=INK)
ax2.set_yticks(range(len(items))); ax2.set_yticklabels(labs, fontsize=9, color=INK)
ax2.invert_yaxis(); ax2.set_xlim(1993, 2029)
ax2.set_title("核心系统投用年份与超期年限", fontsize=11.5, color=INK, weight="bold")
ax2.grid(axis="x", **GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right", "left")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig01_安全隐患趋势.png")

# ══ 图2 市场定位：同级别国际联号对标（携程口径） ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.4))
# 左图：同属洲际体系在成都的携程挂牌价 vs 总府挂牌价 vs 总府实际成交 ADR
labs = ["温江皇冠\n39平方米", "西区皇冠\n40平方米", "天府皇冠\n邻环球中心",
        "总府皇冠\n30平方米", "总府实际\n成交 ADR"]
lo = [698, 675, 730, 728, 412.09]
hi = [1098, 710, 1080, 1268, 412.09]
cl = ["#9DB4C0", "#9DB4C0", "#9DB4C0", C[0], "#A03A2E"]
xs = np.arange(len(labs))
for k in range(len(labs)):
    if hi[k] > lo[k]:
        ax1.bar(k, hi[k] - lo[k], bottom=lo[k], color=cl[k], width=.55)
        ax1.text(k - .30, hi[k] + 30, f"{lo[k]:,}", ha="right", fontsize=8.8, color=INK)
        ax1.text(k + .30, hi[k] + 30, f"{hi[k]:,}", ha="left", fontsize=8.8, color=INK)
    else:
        ax1.bar(k, 60, color=cl[k], width=.55)
        ax1.text(k, lo[k] + 60, f"{lo[k]:,.2f}", ha="center", fontsize=9.4, color=INK, weight="bold")
ax1.set_xticks(xs); ax1.set_xticklabels(labs, fontsize=8.2, color=INK)
for _t in ax1.get_xticklabels():
    _t.set_linespacing(1.35)
ax1.set_ylim(0, 1620); ax1.set_xlim(-0.62, 5.05); ax1.set_ylabel("元/间晚", fontsize=10, color=MUT)
ax1.set_title("同品牌同城：携程挂牌价基本持平，但总府实际成交仅 412", fontsize=11.2, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[x].set_visible(False) for x in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9)
ax1.annotate("", xy=(4, 460), xytext=(4, 1150), arrowprops=dict(arrowstyle="<->", color="#A03A2E", lw=1.4))
ax1.text(4.28, 800, "缺口 768 元\n（协议价与会员价\n结构造成）", fontsize=8.4, color="#A03A2E", ha="left", weight="bold")
ax1.text(0.02, .965, "结论：价格带由品牌与商圈决定，资产老旧未被折价；改造的作用是把成交价推回挂牌带",
         transform=ax1.transAxes, fontsize=8.4, color="#A03A2E", weight="bold")
# 右图：成都高端价格带阶梯（携程口径）
seg = [("居舍 Upper House", 142, 2000, 3000), ("尼依格罗 Niccolo", 230, 1400, 2800),
       ("瑞吉 St. Regis", 282, 1300, 1700), ("洲至奢选(棕榈泉)", 336, 1588, 2088),
       ("温江皇冠(同品牌对照)", 458, 698, 1098), ("总府皇冠(携程挂牌)", 402, 728, 1268)]
for k, (n, rm, a, b) in enumerate(seg):
    ax2.barh(k, b - a, left=a, color=C[0] if "总府" in n else "#6E93A8", alpha=.9, height=.55)
    ax2.text(a - 55, k, f"{a:,}–{b:,}", va="center", ha="right", fontsize=8.6, color=INK)
    ax2.text(3180, k, f"{n}\n{rm} 间", va="center", fontsize=8.4, color=MUT)
ax2.axvline(412.09, color="#A03A2E", lw=2.0, ls="--")
ax2.text(430, -0.62, "总府实际成交 ADR 412.09（含服务费）", color="#A03A2E", fontsize=9, weight="bold")
ax2.set_yticks([]); ax2.set_xlim(0, 3400); ax2.set_ylim(5.9, -1.15); ax2.invert_yaxis()
ax2.set_xlabel("元/间晚（携程口径挂牌价）", fontsize=10, color=MUT)
ax2.set_title("成都高端价格带阶梯：900 元以上供给不少于 1,632 间", fontsize=11.2, color=INK, weight="bold")
ax2.grid(axis="x", **GRID); [ax2.spines[x].set_visible(False) for x in ("top", "right", "left")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig02_市场定位与价格带.png")

# ══ 图3 面积刚性与房量反推 ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))
brands = [("皇冠现状", 25.35, 402, "现状实测"), ("皇冠 2026 标准", 35, 291, "≥35㎡"),
          ("洲至奢选(洲际条件)", 40, 254, "≥40㎡"), ("洲至奢选(实测)", 45, 226, "45㎡实测"),
          ("康莱德", 46, 205, "异地样本"), ("尼依格罗", 50, 188, "本地实测"),
          ("丽晶/LXR", 60, 157, "异地样本"), ("瑞吉", 65, 145, "本地实测")]
ns = [b[0] for b in brands]; rms = [b[2] for b in brands]
cl = [C[0] if b[3] == "现状实测" else ("#3F7D58" if "本地" in b[3] else "#B07A3C") for b in brands]
bb = ax1.bar(ns, rms, color=cl, width=.62)
for r, b in zip(bb, brands):
    ax1.text(r.get_x() + r.get_width() / 2, r.get_height() + 6, f"{b[2]}\n{b[1]}㎡", ha="center",
             fontsize=8.4, color=INK, weight="bold")
ax1.set_ylabel("可行房量（间）", fontsize=10, color=MUT); ax1.set_ylim(0, 460)
ax1.set_title("客房套内 10,192㎡ 刚性约束下的房量反推", fontsize=11.5, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=8.2)
plt.setp(ax1.get_xticklabels(), rotation=32, ha="right")
ax2.plot([b[1] for b in brands], rms, "-o", color=C[1], lw=2, ms=7)
for b in brands:
    ax2.annotate(f"{b[2]}", (b[1], b[2]), textcoords="offset points", xytext=(0, 11),
                 ha="center", fontsize=8.6, color=INK)
ax2.axhline(402, color="#A03A2E", ls="--", lw=1.4)
ax2.text(30, 410, "现状 402 间", color="#A03A2E", fontsize=9, weight="bold")
ax2.axhline(291, color=C[2], ls=":", lw=1.4)
ax2.text(30, 299, "皇冠 2026 标准上限 291 间", color=C[2], fontsize=9, weight="bold")
ax2.set_xlabel("品牌基础房面积要求（㎡/间）", fontsize=10, color=MUT)
ax2.set_ylabel("可行房量（间）", fontsize=10, color=MUT)
ax2.set_title("面积要求是房量的唯一决定因素", fontsize=11.5, color=INK, weight="bold")
ax2.grid(**GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig03_面积刚性与房量反推.png")

# ══ 图4 四路径 NPV 与关键构成 ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ks = ["P1", "P2", "P3", "P4"]
npvs = [R[k]["npv"] for k in ks]
bars = ax1.bar([f"路径{k[1]}\n{R[k]['rooms']}间" for k in ks], npvs,
               color=[C[2], "#A03A2E", "#A03A2E", "#7A5C8E"], width=.55)
for r, v in zip(bars, npvs):
    ax1.text(r.get_x() + r.get_width() / 2, v + (900 if v > 0 else -1900),
             f"{v:,.0f}", ha="center", fontsize=10.5, weight="bold", color=INK)
ax1.axhline(0, color=INK, lw=1.2)
ax1.set_ylabel("项目口径净现值（万元）", fontsize=10, color=MUT)
ax1.set_ylim(-30000, 12000)
ax1.set_title("四路径净现值对比（评价期 20 年、折现率 8%）", fontsize=11.5, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9.5)
ax1.text(.02, .93, "项目口径，不含存量债务利息（各路径共同项）", transform=ax1.transAxes,
         fontsize=8.6, color=MUT)
comp = {"投资额（业主承担）": [R[k]["owner_capex"] for k in ks],
        "停业期净流出": [-R[k]["shutdown_cf_total"] for k in ks],
        "达产年经营现金流": [R[k]["op_cf_stable"] for k in ks]}
bottom = np.zeros(4); xs = np.arange(4)
for i, (lb, vs) in enumerate(comp.items()):
    ax2.bar(xs, vs, bottom=bottom, label=lb, color=["#2E6E8E", "#C96A2E", "#3F7D58"][i], width=.55)
    bottom += np.array(vs, dtype=float)
ax2.set_xticks(xs); ax2.set_xticklabels([f"路径{k[1]}" for k in ks], fontsize=10, color=INK)
ax2.set_ylabel("万元", fontsize=10, color=MUT)
ax2.set_title("资金占用与达产产出对比（上为投资与停业出，下为达产年经营现金流）", fontsize=10.8, color=INK, weight="bold")
ax2.legend(fontsize=8.8, frameon=False, loc="upper left")
ax2.grid(axis="y", **GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right")]
ax2.tick_params(colors=MUT, labelsize=9.5)
save(fig, "fig04_四路径净现值与构成.png")

# ══ 图5 累计折现现金流曲线 ══
fig, ax = plt.subplots(figsize=(9.2, 4.4))
for i, k in enumerate(ks):
    cfs = None
    capex = R[k]["capex"]
    # 重算现金流序列以绘制曲线
    import copy
    p = copy.deepcopy(D["paths"][k])
    from importlib import util as _u
    ax.bar(0, 0)
    cfs = None
    ax.plot([], [])
    # 用近似：从结果重建
    life = 20
    dt = p["downtime"]
    dtm = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * .6 + B["cost_10m"]["能源"] / 10 * .25)
    seq = [-capex] + [-dtm] * dt
    for m in range(6):
        seq.append(R[k]["op_cf_stable"] * (0.45 + (0.85 - .45) * (m / 5)))
    for y in range(life):
        seq.append(R[k]["op_cf_stable"])
    disc = [cf / (1.08 ** i) for i, cf in enumerate(seq)]
    cum = np.cumsum(disc)
    xs2 = list(range(len(seq)))
    ax.plot(xs2, cum, lw=2, color=C[i], label=f"路径{k[1]}  净现值 {R[k]['npv']:,.0f} 万元")
    ax.annotate(f"{cum[-1]:,.0f}", (xs2[-1], cum[-1]), textcoords="offset points", xytext=(6, 0),
                fontsize=9, color=C[i], weight="bold")
ax.axhline(0, color=INK, lw=1.2)
ax.set_xlabel("自决策时点起的月序", fontsize=10, color=MUT)
ax.set_ylabel("累计折现现金流（万元，8% 折现）", fontsize=10, color=MUT)
ax.set_title("四路径累计折现现金流曲线（负值＝项目口径不成立）", fontsize=11.8, color=INK, weight="bold")
ax.legend(fontsize=9, frameon=False, loc="lower right")
ax.grid(**GRID); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.tick_params(colors=MUT, labelsize=9.5)
save(fig, "fig05_累计折现现金流曲线.png")

# ══ 图6 敏感性龙卷风（P1 与 P2 对照） ══
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
for ax, k in zip(axes, ("P1", "P2")):
    base = R[k]["npv"]
    picks = [("ADR -10%", "ADR −10%"), ("ADR +10%", "ADR +10%"), ("OCC -5pp", "OCC −5pp"),
             ("OCC +5pp", "OCC +5pp"), ("停业下限", "停业期下限"), ("停业上限", "停业期上限"),
             ("CAPEX -15%", "投资 −15%"), ("CAPEX +15%", "投资 +15%"),
             ("折现率 10%", "折现率 10%"), ("评价期 10 年", "评价期 10 年"),
             ("品牌方承担 30%", "品牌方承担 30%"),
             ("房价不提升（ADR维持现状）", "房价不提升（关键情景）")]
    names, deltas = [], []
    for src, lb in picks:
        v = S[k].get(src)
        if v is None: continue
        names.append(lb); deltas.append(v - base)
    order = sorted(range(len(deltas)), key=lambda i: abs(deltas[i]))
    names = [names[i] for i in order]; deltas = [deltas[i] for i in order]
    cl = ["#A03A2E" if d < 0 else C[2] for d in deltas]
    ax.barh(range(len(deltas)), deltas, color=cl, height=.62)
    lo, hi = min(deltas + [0]), max(deltas + [0])
    span = (hi - lo) or 1.0
    ax.set_xlim(lo - span * .30, hi + span * .30)
    for i, d in enumerate(deltas):
        frac = abs(d) / span
        if frac > .30:
            ax.text(d - (160 if d > 0 else -160), i, f"{d:+,.0f}", va="center",
                    ha="right" if d > 0 else "left", fontsize=8.4, color="white", weight="bold")
        else:
            ax.text(d + (260 if d > 0 else -260), i, f"{d:+,.0f}", va="center",
                    ha="left" if d > 0 else "right", fontsize=8.4, color=INK)
    ax.axvline(0, color=INK, lw=1.1)
    ax.set_yticks(range(len(deltas))); ax.set_yticklabels(names, fontsize=8.8, color=INK)
    ax.set_title(f"路径{k[1]} 敏感性（基准净现值 {base:,.0f} 万元）", fontsize=11, color=INK, weight="bold")
    ax.grid(axis="x", **GRID); [ax.spines[s].set_visible(False) for s in ("top", "right", "left")]
    ax.tick_params(colors=MUT, labelsize=9)
    ax.set_xlabel("净现值变动（万元）", fontsize=9.5, color=MUT)
save(fig, "fig06_敏感性龙卷风图.png")

# ══ 图7 停业期损失与达产收入结构 ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))
dtt = [R[k]["downtime"] for k in ks]
cf = [-R[k]["shutdown_cf_total"] for k in ks]
bb = ax1.bar([f"路径{k[1]}" for k in ks], cf, color=["#3F7D58", "#C96A2E", "#A03A2E", "#7A5C8E"], width=.5)
for r, v, d in zip(bb, cf, dtt):
    ax1.text(r.get_x() + r.get_width() / 2, v + 220, f"{v:,.0f}\n({d} 个月)", ha="center",
             fontsize=9.4, color=INK, weight="bold")
ax1.set_ylabel("停业期净现金流出（万元）", fontsize=10, color=MUT)
ax1.set_title("停业期代价：整体改造路径的隐性重负", fontsize=11.5, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9.5)
mix = B["mix_A_ttm"]
ax2.pie(list(mix.values()), labels=[f"{k}\n{v*100:.1f}%" for k, v in mix.items()],
        colors=[C[0], C[1], C[2], "#8A5B8C"], autopct="", startangle=90,
        textprops={"fontsize": 9.5, "color": INK}, wedgeprops={"edgecolor": "white", "lw": 1.5})
ax2.set_title("改造前收入结构（滚动 12 个月，口径 A）", fontsize=11.5, color=INK, weight="bold")
save(fig, "fig07_停业期损失与收入结构.png")

# ══ 图8 盈亏平衡 RevPAR 约束 ══
fig, ax = plt.subplots(figsize=(9.2, 4.0))
req = [BE[k]["required_revpar"] for k in ks]; asm = [BE[k]["assumed_revpar"] for k in ks]
xs3 = np.arange(4); w = .34
ax.bar(xs3 - w / 2, req, w, label="守住现状客房收入所需 RevPAR", color="#9DB4C0")
ax.bar(xs3 + w / 2, asm, w, label="本方案达产 RevPAR（口径 A）", color=C[0])
for i, (q, a) in enumerate(zip(req, asm)):
    ax.text(i - w / 2, q + 12, f"{q:,.0f}", ha="center", fontsize=9, color=INK, weight="bold")
    ax.text(i + w / 2, a + 12, f"{a:,.0f}", ha="center", fontsize=9, color=INK, weight="bold")
ax.set_xticks(xs3); ax.set_xticklabels([f"路径{k[1]}\n{R[k]['rooms']} 间" for k in ks], fontsize=10, color=INK)
ax.set_ylabel("元/间夜", fontsize=10, color=MUT); ax.set_ylim(0, 1000)
ax.set_title("减房后的盈亏平衡约束：守住现状客房收入所需 RevPAR", fontsize=11.5, color=INK, weight="bold")
ax.legend(fontsize=9, frameon=False, loc="upper left")
ax.grid(axis="y", **GRID); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.tick_params(colors=MUT, labelsize=9.5)
save(fig, "fig08_盈亏平衡RevPAR约束.png")
print("图表完成")
