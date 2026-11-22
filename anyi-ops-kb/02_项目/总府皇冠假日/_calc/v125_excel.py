# -*- coding: utf-8 -*-
"""v125：图表（按四方案）+ Excel 测算附表（含说明）+ Word 重建 + 终检"""
import json, os, io, re, sys, shutil, subprocess, glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

sys.stdout.reconfigure(encoding="utf-8")
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FIG = os.path.join(KB, "_calc", "fig")
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
V = json.load(open(os.path.join(T, "v120.json"), encoding="utf-8"))
R, SENS, TIERS, RC = V["results"], V["sensitivity"], V["tiers"], V["roomcount"]
K = ("S1", "S2", "S3", "S4")
NAMES = {"S1": "路径一 轻改", "S2": "路径二 停业改造", "S3": "路径三 换品牌动格局", "S4": "路径四 自建品牌"}
def f0(x): return "{:,.0f}".format(x) if isinstance(x, (int, float)) else str(x)
def nz(x): return ("\u2212" if x < 0 else "\uff0b") + f0(abs(x))

# ══════════ 字体 ══════════
cands = ["Microsoft YaHei", "SimHei", "Microsoft JhengHei", "DengXian"]
have = {f.name for f in fm.fontManager.ttflist}
font = next((c for c in cands if c in have), None)
plt.rcParams["font.sans-serif"] = [font] if font else ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#1F2933"; MUT = "#7B8794"; C = ["#2E6E8E", "#C96A2E", "#7A5C8C", "#3F7D58"]
GRID = {"color": "#E4E7EB", "lw": .8}
def save(fig, name):
    p = os.path.join(FIG, name); fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("  ", name, round(os.path.getsize(p) / 1024), "KB")

# ══════════ 图3：房量口径（三改二）══════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.3))
items = [("皇冠现状", 25.35, 402, "实测"), ("皇冠 2026 标准", 35, 291, "品牌标准"),
         ("洲至奢选（洲际条件）", 40, 254, "F2-29"), ("洲至奢选（实测）", 45, 226, "本地实测"),
         ("康莱德", 46, 205, "异地样本"), ("尼依格罗", 50, 188, "本地实测"),
         ("丽晶／LXR", 60, 157, "品牌标准"), ("瑞吉", 65, 145, "本地实测")]
xs = np.arange(len(items))
ax1.bar(xs, [i[2] for i in items], color=[C[0]] + ["#6E93A8"] * 7, width=.62)
for x, it in zip(xs, items):
    ax1.text(x, it[2] + 6, "%d\n%.0f㎡" % (it[2], it[1]), ha="center", fontsize=8.4, color=INK, weight="bold")
ax1.set_xticks(xs); ax1.set_xticklabels([i[0] for i in items], fontsize=8, color=INK, rotation=30, ha="right")
ax1.set_ylabel("可行房量（间）", fontsize=10, color=MUT); ax1.set_ylim(0, 460)
ax1.set_title("按品牌基础房面积要求反推的可行房量", fontsize=11.5, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9)
ax2.plot([i[1] for i in items], [i[2] for i in items], "-o", color=C[1], lw=2, ms=7)
for i in items:
    ax2.annotate("%d" % i[2], (i[1], i[2]), textcoords="offset points", xytext=(0, 11), ha="center", fontsize=8.6, color=INK)
ax2.axhline(402, color="#A03A2E", ls="--", lw=1.5); ax2.text(30, 410, "现状 402 间", color="#A03A2E", fontsize=9, weight="bold")
ax2.axhline(268, color=C[2], ls=":", lw=1.6); ax2.text(30, 276, "三改二 268 间（套内 38.0㎡）", color=C[2], fontsize=9, weight="bold")
ax2.set_xlabel("品牌基础房面积要求（㎡/间）", fontsize=10, color=MUT)
ax2.set_ylabel("可行房量（间）", fontsize=10, color=MUT)
ax2.set_title("面积要求是房量的唯一决定因素", fontsize=11.5, color=INK, weight="bold")
ax2.grid(**GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig03_面积刚性与房量反推.png")

# ══════════ 图4：四方案净现值与结构 ═════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.3))
npvs = [R[k]["npv"] for k in K]
bars = ax1.bar([NAMES[k] for k in K], npvs, color=[C[3], C[1], "#A03A2E", "#7A5C8C"], width=.55)
for r, v in zip(bars, npvs):
    ax1.text(r.get_x() + r.get_width() / 2, v + (900 if v > 0 else -2200), nz(v),
             ha="center", fontsize=10.5, weight="bold", color=INK)
ax1.axhline(0, color=INK, lw=1.2)
ax1.set_ylabel("项目口径净现值（万元）", fontsize=10, color=MUT); ax1.set_ylim(-34000, 12000)
ax1.set_title("四方案净现值对比（评价期 20 年、折现率 8%）", fontsize=11.5, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=8.6)
ax1.text(.02, .93, "不含存量债务利息（各方案共同项）", transform=ax1.transAxes, fontsize=8.6, color=MUT)
comp = {"投资额": [R[k]["capex"] for k in K], "停业期净流出": [R[k]["shutdown_loss"] for k in K],
        "达产年经营现金流": [R[k]["op_cf_peak"] for k in K]}
bot = np.zeros(4); xx = np.arange(4)
for i, (lb, vs) in enumerate(comp.items()):
    ax2.bar(xx, vs, bottom=bot, label=lb, color=[C[0], C[1], C[3]][i], width=.55)
    bot += np.array(vs, dtype=float)
ax2.set_xticks(xx); ax2.set_xticklabels([NAMES[k] for k in K], fontsize=8.6, color=INK, rotation=18, ha="right")
ax2.set_ylabel("万元", fontsize=10, color=MUT)
ax2.set_title("投资额、停业损失与达产现金流的结构对比", fontsize=11.5, color=INK, weight="bold")
ax2.legend(fontsize=8.8, frameon=False, loc="upper left")
ax2.grid(axis="y", **GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig04_四路径净现值与构成.png")

# ══════════ 图5：累计折现现金流 ═════════
import copy
fig, ax = plt.subplots(figsize=(9.6, 4.4))
for i, k in enumerate(K):
    # 简化重建月度现金流
    adr = R[k]["adr_peak"]; occ = R[k]["occ_peak"]; rooms = R[k]["rooms"]
    tier = R[k]["tier"]; T_ = TIERS[tier]
    B98 = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))["base"]
    def op_year(year):
        price = {1: .65, 2: .80, 3: .90, 4: 1.0}.get(year, max(.55, 1 - .012 * (year - 4)))
        od = {1: -.05, 2: -.02}.get(year, 0.0)
        a = adr * price; o = min(.95, max(.30, B98["occ_ttm"] + od))
        rn = rooms * 365
        room_B = rn * o * a / 10000.0
        svc = room_B * B98["svc_pct_of_room_B"]
        oratio = o / B98["occ_ttm"]
        nonroom_B = B98["nonroom_B_fy2025"] * (oratio ** .8) * ((rooms / 402) ** .5)
        rev_A = room_B + svc + nonroom_B
        gop = room_B * B98["dept_margin"]["房务部"] + nonroom_B * B98["nonroom_margin_blend"]
        sc = rooms / 402; AN = B98["annualize_10m"]
        undist = (B98["cost_10m"]["A&G"] * AN * (.75 + .25 * sc) + B98["cost_10m"]["POM"] * AN * (.70 + .30 * sc)
                  + B98["cost_10m"]["IT"] * AN + B98["cost_10m"]["S&M"] * AN * oratio
                  + B98["cost_10m"]["能源"] * AN * (.55 + .45 * sc))
        ihg = gop - undist
        if rooms == 402:
            lic = (room_B + svc + nonroom_B) * B98["license_pct_rev_B"]; imf = max(0, ihg - lic) * B98["imf_pct"]
        else:
            lic = room_B * .05; imf = 0
        adj = ihg - lic - imf
        return {"rev_A": rev_A, "op": adj - rev_A * .02}
    dtm = (B98["shutdown_labor_monthly"] + B98["cost_10m"]["POM"] / 10 * .6 + B98["cost_10m"]["能源"] / 10 * .25)
    cfs = [-R[k]["capex"]]
    for _ in range(R[k]["dur"]): cfs.append(-dtm)
    for m in range(6):
        kk = .45 + (.85 - .45) * (m / 5)
        o = op_year(1); cfs.append((o["op"] * kk - o["rev_A"] * .02 / 12))
    for y in range(1, 21):
        o = op_year(y)
        for _ in range(12): cfs.append(o["op"] / 12)
    rm = (1.08) ** (1 / 12) - 1
    cum = np.cumsum([cf / ((1 + rm) ** m) for m, cf in enumerate(cfs)])
    ax.plot(range(len(cum)), cum, lw=2, color=C[i], label="%s  NPV %s" % (NAMES[k], nz(R[k]["npv"])))
ax.axhline(0, color=INK, lw=1.2)
ax.set_xlabel("自决策时点起的月序", fontsize=10, color=MUT)
ax.set_ylabel("累计折现现金流（万元，8% 折现）", fontsize=10, color=MUT)
ax.set_title("四方案累计折现现金流曲线（负值＝项目口径不成立）", fontsize=11.8, color=INK, weight="bold")
ax.legend(fontsize=9, frameon=False, loc="lower right")
ax.grid(**GRID); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.tick_params(colors=MUT, labelsize=9)
save(fig, "fig05_累计折现现金流曲线.png")

# ══════════ 图6：敏感性龙卷风（路径一 vs 路径三）══════════
fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.3))
picks = [("造价 −30%", "造价 −30%"), ("造价 +30%", "造价 +30%"), ("房价 −10%", "房价 −10%"),
         ("房价不提升（412 元）", "房价不提升"), ("停业下限", "停业下限"), ("停业上限", "停业上限"),
         ("评价期 10 年", "评价期 10 年"), ("折现率 10%", "折现率 10%"),
         ("房价上探（奢华档 2200 元）", "房价上探 2200 元")]
for ax, k in zip(axes, ("S1", "S3")):
    base = R[k]["npv"]; names = []; deltas = []
    for src, lb in picks:
        v = SENS[k].get(src)
        if v is None: continue
        names.append(lb); deltas.append(v - base)
    order = sorted(range(len(deltas)), key=lambda i: abs(deltas[i]))
    names = [names[i] for i in order]; deltas = [deltas[i] for i in order]
    cl = ["#A03A2E" if d < 0 else C[3] for d in deltas]
    ax.barh(range(len(deltas)), deltas, color=cl, height=.62)
    lo, hi = min(deltas + [0]), max(deltas + [0]); span = (hi - lo) or 1
    ax.set_xlim(lo - span * .34, hi + span * .34)
    for i, d in enumerate(deltas):
        frac = abs(d) / span
        if frac > .28:
            ax.text(d - (150 if d > 0 else -150), i, ("%+" + f0(d)), va="center",
                    ha="right" if d > 0 else "left", fontsize=8.2, color="white", weight="bold")
        else:
            ax.text(d + (240 if d > 0 else -240), i, ("%+" + f0(d)), va="center",
                    ha="left" if d > 0 else "right", fontsize=8.2, color=INK)
    ax.axvline(0, color=INK, lw=1.1)
    ax.set_yticks(range(len(deltas))); ax.set_yticklabels(names, fontsize=8.6, color=INK)
    ax.set_title("%s 敏感性（基准净现值 %s 万元）" % (NAMES[k], nz(base)), fontsize=11, color=INK, weight="bold")
    ax.grid(axis="x", **GRID); [ax.spines[s].set_visible(False) for s in ("top", "right", "left")]
    ax.tick_params(colors=MUT, labelsize=9)
    ax.set_xlabel("净现值变动（万元）", fontsize=9.5, color=MUT)
save(fig, "fig06_敏感性龙卷风图.png")

# ══════════ 图7：三档收入结构 ═════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.2))
tiers = list(TIERS.keys())
for i, t in enumerate(tiers):
    d = TIERS[t]
    bottom = 0
    for kk, lb, col in (("客房", "客房", C[0]), ("餐饮", "餐饮", C[1]), ("会议", "会议", C[3]), ("其他", "其他", "#B07A3C")):
        v = d["mix"][kk]
        ax1.bar(i, v, bottom=bottom, label=lb if i == 0 else None, color=col, width=.55)
        if v > .07: ax1.text(i, bottom + v / 2, "%s\n%.1f%%" % (lb, v * 100), ha="center", va="center", fontsize=8, color="white", weight="bold")
        bottom += v
ax1.set_xticks(range(len(tiers)))
ax1.set_xticklabels([t.replace(" Upper Scale", "\nUpper Scale") for t in tiers], fontsize=8.6, color=INK)
ax1.set_ylabel("收入结构占比", fontsize=10, color=MUT); ax1.set_ylim(0, 1)
ax1.set_title("三档价格带的收入结构模型", fontsize=11.5, color=INK, weight="bold")
ax1.legend(fontsize=8.6, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(.5, -.08))
ax1.grid(axis="y", **GRID); [ax1.spines[s].set_visible(False) for s in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9)
y = [r["price_factor"] for r in V["ramp"][:20]]
xs2 = list(range(1, 21))
ax2.plot(xs2, y, "-o", color=C[0], lw=2, ms=4.5)
ax2.axhline(1.0, color=MUT, ls="--", lw=1)
ax2.axvline(4, color=C[1], ls=":", lw=1.4)
ax2.text(4.25, 0.62, "第 4 年达峰", color=C[1], fontsize=9, weight="bold")
ax2.text(13.5, 0.72, "其后每年 −1.2% 回落", color=MUT, fontsize=8.8)
ax2.set_xlabel("复业后第几年", fontsize=10, color=MUT); ax2.set_ylabel("价格回归系数", fontsize=10, color=MUT)
ax2.set_ylim(.5, 1.1)
ax2.set_title("复业爬坡曲线（20 年口径）", fontsize=11.5, color=INK, weight="bold")
ax2.grid(**GRID); [ax2.spines[s].set_visible(False) for s in ("top", "right")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig07_停业期损失与收入结构.png")

# ══════════ 图8：盈亏平衡 RevPAR ═════════
fig, ax = plt.subplots(figsize=(9.4, 4.0))
req = [323, 323, 621, 621]; asm = [R[k]["rev_A_peak"] * 10000 / (R[k]["rooms"] * 365) for k in K]
xx = np.arange(4); w = .34
ax.bar(xx - w / 2, req, w, label="守住现状客房收入所需 RevPAR", color="#9DB4C0")
ax.bar(xx + w / 2, asm, w, label="本方案达产 RevPAR（口径 A）", color=C[0])
for i, (q, a) in enumerate(zip(req, asm)):
    ax.text(i - w / 2, q + 12, "%d" % q, ha="center", fontsize=9, color=INK, weight="bold")
    ax.text(i + w / 2, a + 12, "%d" % a, ha="center", fontsize=9, color=INK, weight="bold")
ax.set_xticks(xx); ax.set_xticklabels([NAMES[k] for k in K], fontsize=8.8, color=INK, rotation=14, ha="right")
ax.set_ylabel("元/间夜", fontsize=10, color=MUT); ax.set_ylim(0, 1000)
ax.set_title("减房后的盈亏平衡 RevPAR 约束", fontsize=11.5, color=INK, weight="bold")
ax.legend(fontsize=9, frameon=False, loc="upper left")
ax.grid(axis="y", **GRID); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.tick_params(colors=MUT, labelsize=9)
save(fig, "fig08_盈亏平衡RevPAR约束.png")

# ══════════════════ Excel 测算附表 ══════════════════
wb = Workbook(); wb.remove(wb.active)
HD = PatternFill("solid", fgColor="1F4E5F"); HF = Font(color="FFFFFF", bold=True, size=10)
SUB = PatternFill("solid", fgColor="DCE6EC"); TOT = PatternFill("solid", fgColor="F3E6C8")
THIN = Side(style="thin", color="B0BEC5"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
def sh(name, headers, rows, widths=None, note=None):
    ws = wb.create_sheet(name); r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(size=9, italic=True, color="555555")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(3, len(headers)))
        r0 = 2
    for j, h in enumerate(headers, 1):
        c = ws.cell(r0, j, h); c.fill = HD; c.font = HF
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BD
    for i, row in enumerate(rows, r0 + 1):
        tot = str(row[0]).startswith(("合计", "小计", "合计（"))
        for j, v in enumerate(row, 1):
            c = ws.cell(i, j, v); c.font = Font(bold=tot, size=10); c.border = BD
            if isinstance(v, (int, float)):
                c.number_format = '#,##0.00'; c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            if tot: c.fill = TOT
    for j, w in enumerate(widths or [26] * len(headers), 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 1); ws.row_dimensions[r0].height = 30
    return ws
from openpyxl.utils import get_column_letter

# 00 说明
sh("00 说明与使用指引", ["项目", "内容"], [
 ["报告名称", "总府皇冠假日酒店重大安全隐患改造项目可行性研究报告暨执行路径请示（v7.0）"],
 ["编制单位", "安逸酒店集团产业发展部"],
 ["编制日期", "2026-11-15"],
 ["授权依据", "《关于总府皇冠假日酒店重大安全隐患专题会纪要》（2026-10-16）第三条"],
 ["报告性质", "按会议纪要要求形成的确定性方案意见，提出四条执行路径请集团选择"],
 ["价格口径", "不含服务费；服务费按口径 A 客房收入 10.06% 计"],
 ["时间轴口径", "统一月度网格；折现率 (1+8%)^(1/12)-1；评价期 20 年"],
 ["NPV 口径", "项目口径，不含存量债务利息（各方案共同项，另列于表 08 说明）"],
 ["关键提醒一", "全部造价为产业发展部按数量基数自下而上编制，未经第三方工程量清单核定，不得作为投资承诺依据"],
 ["关键提醒二", "客房轻改单间造价为框算区间（软装级 3.5—5.5／中度级 6—10／深度级 10—15 万元每间），基准取中度级中值 8.0 万元"],
 ["关键提醒三", "路径三的成立性取决于 268 间能否进入 2,000 元以上价格带，须由市场验证"],
 ["表目录", "01 改造前基线；02 三档价格带与收入结构；03 房量口径；04 公共必选工程；05—08 四方案测算；09 敏感性；10 爬坡曲线；11 存量改造工作步骤；12 全生命周期分工；13 数据来源"],
], [16, 96], note="使用说明：本表册全部数据与研究报告 v7.0 同源；请先读本表，再读正文。")

# 01 基线
B98 = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))["base"]
sh("01 改造前基线", ["指标", "2023年", "2024年", "2025年", "滚动12个月", "2026年1-10月", "口径与来源"], [
 ["营业收入（万元，口径A含服务费）", 7948, 7937, 7099.54, 6442.73, 5403.53, "业主资料(2)；近24个月经营指标；2026年10月利润表"],
 ["营业收入同比", None, -0.0014, -0.1055, None, -0.1173, "2026年1-10月同比 −11.73%"],
 ["平均房价（元，含服务费）", None, None, 435.95, 412.09, 428.50, "近24个月经营指标"],
 ["出租率", None, None, 0.7410, 0.7253, 0.8245, "同上"],
 ["每间可售房收入（元）", None, None, 323.04, 298.70, 353.30, "同上"],
 ["经营毛利润（万元）", 1504, 1506, 1580.64, None, 1393.90, "台账加总；口径B调整后营业毛利润"],
 ["净营业利润（万元）", None, None, None, None, -416.51, "2026年1-10月，扣奖励管理费与非经营性费用后"],
 ["客房收入占比", None, None, 0.6677, 0.6810, None, "口径A"],
 ["餐饮收入占比", None, None, 0.1239, 0.1400, None, "口径A"],
 ["会议收入占比", None, None, 0.1416, 0.1280, None, "口径A"],
 ["其它收入占比", None, None, 0.0669, 0.0510, None, "口径A"],
 ["非房收入合计占比", None, None, 0.3323, 0.3190, None, "口径A"],
 ["人工成本（万元，年化）", None, None, 2530.0, 2269.4, 2184.1, "2026年1-10月1820.08万×1.2"],
 ["能耗成本（万元，年化）", None, None, 572.3, 548.6, 525.2, "P&L Energy"],
 ["维保成本（万元）", None, None, 183.81, 145.70, None, "口径A全口径；合同类2026年43.72万"],
 ["年利息支出（万元）", None, None, 2088.85, 2088.85, 1740.71, "P&L Summary Other Non-Operating(Interest)；月均174.07万"],
 ["折旧摊销（万元）", 722, 711, 387.0, None, None, "业主口径；2025年降幅45.6%原因无台账"],
 ["客房数（间）", None, None, 402, 402, 402, "面积台账415间；在售402间三方一致"],
 ["营业总收入（万元，口径B不含服务费）", None, None, 6666.0, None, 5065.06, "P&L TOTAL REVENUE"],
 ["服务费（万元）", None, None, 433.5, None, 338.47, "P&L Service Charge"],
], [26, 11, 11, 13, 13, 14, 44], note="改造前经营基线：口径A（含服务费）与口径B（利润表）通过1.1006倍服务费系数桥接")

# 02 三档价格带与收入结构
rows = []
for t, d in TIERS.items():
    rows.append([t, d["adr_lo"], d["adr_hi"], d["mix"]["客房"], d["mix"]["餐饮"], d["mix"]["会议"], d["mix"]["其他"], d["nonroom_ratio"], d["ref"]])
sh("02 三档价格带与收入结构", ["档次", "价格带下限(元/间晚,不含服务费)", "价格带上限", "客房占比", "餐饮占比", "会议占比", "其他占比", "非房合计占比", "实证依据"], rows,
   [16, 14, 12, 10, 10, 10, 10, 13, 56], note="三档价格带的收入结构不同，测算中不可相互套用；实证依据见末列")

# 03 房量口径
rows = [["现状", 402, 25.35, 10192, "10,192 ÷ 402 恰整除，现存建筑无移卫耦合折损", "实测"],
        ["三改二（每3间并为2间）", 268, 38.0, 10192, "名义含卫生间约42.6平方米，满足洲至奢选等品牌常规房型", "工程推算"],
        ["三改二＋洲际方套内≥40平方米约束", 254, 40.1, 10192, "若品牌方坚持40平方米套内下限，房量再减14间", "合同条件"],
        ["皇冠 2026 标准≥35平方米", 291, 35.0, 10192, "品牌建造设计标准 [958140]/[958148]", "品牌标准"],
        ["洲至奢选 洲际方条件≥40平方米", 254, 40.0, 10192, "F2-29 沟通纪要", "合同条件"],
        ["洲至奢选 实测基础房45平方米", 226, 45.0, 10192, "成都棕榈泉房型实测与酒店官方口径", "本地实测"],
        ["康莱德 46平方米", 205, 46.0, 10192, "异地代理样本（北京）", "异地样本"],
        ["尼依格罗 50平方米", 188, 50.0, 10192, "本地实测", "本地实测"],
        ["丽晶/LXR 60平方米", 157, 60.0, 10192, "品牌标准", "品牌标准"],
        ["瑞吉 65平方米", 145, 65.0, 10192, "本地实测", "本地实测"]]
sh("03 房量口径", ["口径", "房量(间)", "单间套内面积(㎡)", "客房套内总面积(㎡)", "说明", "依据性质"], rows,
   [30, 11, 15, 18, 44, 14], note="★ 三改二的工程前提：框架结构、无结构安全鉴定报告（工程部2026-11-10答复「未见」）；3改2须先完成结构鉴定与可行性核定")

# 04 公共必选工程
rows = [[it["name"], it.get("unit") or "", it["amount"], it.get("why", "")] for it in V["common_engineering"]]
rows.append(["合计", "", sum(it["amount"] for it in V["common_engineering"]), "四条路径共有，不可裁量；折合313元/平方米（客用建筑面积69,026.08平方米）"])
sh("04 公共必选工程", ["工程项", "数量基数与单价口径", "金额(万元)", "依据"], rows, [40, 34, 14, 56],
   note="公共必选工程 21,610 万元：按1996年实际投用、现已全面到期或带病运行的系统逐项列示，不按整包给数")

# 05-08 四方案测算
for idx, k in enumerate(K):
    p = V["schemes"][k]; r = R[k]
    rows = [["房量（间）", r["rooms"], "", "目标房量"],
            ["档次", r["tier"], "", ""],
            ["停业期（月）", r["dur"], "", r["dur_range"] + "；一次性整体停业、整体验收、整体复业"],
            ["公共必选工程（万元）", 21610, "", "四条路径共有"],
            ["路径增量工程（万元）", p["subtotal"] - 21610, "", ""]]
    for it in p["items"]:
        rows.append(["　" + it["name"], it["amount"], it.get("basis") or "", ""])
    rows += [["工程费小计（万元）", p["subtotal"], "", ""],
             ["基本预备费（8%）", p["contingency"], "", ""],
             ["建设期利息与资金占用成本", p["interest"], "", "存量债务利率区间3.1%—6%取中值4.5%"],
             ["合计 投资额（万元）", r["capex"], "", "折合单方投资 %s 元/平方米" % f0(r["per_sqm"])],
             ["峰值平均房价（元，不含服务费）", r["adr_peak"], "", "第4年达峰"],
             ["峰值出租率", r["occ_peak"], "", ""],
             ["峰值营业收入（万元，口径A）", r["rev_A_peak"], "", ""],
             ["峰值调整后营业毛利润（万元）", r["adj_gop_peak"], "", ""],
             ["峰值年经营现金流（万元）", r["op_cf_peak"], "", "经营现金流占收入比 %.1f%%" % (r["op_cf_margin"] * 100)],
             ["停业期净现金流出（万元）", r["shutdown_loss"], "", ""],
             ["合计 项目口径净现值（万元）", r["npv"], "", "不含存量债务利息；评价期20年，折现率8%"],
             ["内部收益率", r["irr_pct"], "", "20年评价期"],
             ["动态回收期（年）", r["payback_yr"] if r["payback_yr"] is not None else "不回本", "", ""],
             ["静态回收期（年）", round(r["capex"] / r["op_cf_peak"], 2), "", ""],
             ["评价期30年净现值（万元）", r["npv_30y"], "", ""],
             ["评价期30年内部收益率(%)", r["irr_30y_pct"], "", ""]]
    sh("0%d %s测算" % (5 + idx, NAMES[k].split(" ")[1]), ["项目", "数值", "计算基数／口径", "说明"], rows, [34, 15, 30, 50],
       note="%s 完整测算表；数值与研究报告 v7.0 同源" % NAMES[k])

# 09 敏感性
labels = ["造价 −30%", "造价 −15%", "造价 基准", "造价 +15%", "造价 +30%",
          "评价期 10 年", "评价期 20 年", "评价期 30 年", "折现率 6%", "折现率 8%", "折现率 10%",
          "停业下限", "停业基准", "停业上限", "房价 −10%", "房价不提升（412 元）", "房价上探（奢华档 2200 元）"]
rows = [[lbl] + [SENS[k].get(lbl) for k in K] for lbl in labels]
sh("09 敏感性分析", ["情景（项目口径净现值，万元）"] + [NAMES[k] for k in K], rows, [30, 16, 16, 16, 16],
   note="★「房价不提升」为最关键情景；「房价上探」为路径三的第三档上行情景")

# 10 爬坡曲线
rows = [[r["year"], r["price_factor"], r["occ_delta"], ""] for r in V["ramp"]]
rows.append(["第9年起", "每年 −1.2%", 0, "硬件折旧与同档次供给增加"])
sh("10 爬坡曲线", ["复业后第几年", "价格回归系数", "出租率相对现状变化", "说明"], rows, [16, 16, 20, 40],
   note="复业爬坡曲线：第4年达峰后按每年−1.2%回落；评价期20年与30年口径的净现值差异见方案测算表")

# 11 存量改造工作步骤
rows = [["阶段〇 立项与合规前置", "第0—6月", "请示事项呈报；资料调取；抵押与产权状态梳理；员工安置方案",
         "第三方安全检测评估；机电消防结构专项鉴定；造价复核；管理合同条款确认", "评估报告、投资复核意见、合同确认函", "确认必须整改且投资经复核"],
        ["阶段一 设计定位与方案", "第4—12月", "品牌定位与房量决策；投资上限控制",
         "咨询顾问全程评审；品牌设计方、产品设计方、机电设计方、消防设计方出图；样板间", "设计任务书四册、样板间、施工图、概算与清单", "概算不超上限且样板间获认可"],
        ["阶段二 报建与招采", "第10—16月", "八部门报建；人防与特种设备资料补齐",
         "施工总承包招标；长交期设备采购；监理与检测进场", "批复文件、检验报告、合同包", "全部审批取得"],
        ["阶段三 停业与实施", "第16—28月", "员工安置执行；资产移交；舆情预案",
         "拆除与竖向管网改造；冷源空调末端给排水配电电梯锅炉智能化安装；消防系统整体重做；客房复原", "分部验收记录、隐蔽工程影像、签证台账", "分部验收合格且投资不超上限"],
        ["阶段四 验收与复业", "第28—31月", "渠道与协议客户重签；再培训",
         "消防整体验收与营业前检查；1998年意见书重新审核；品牌方开业前检查与书面授权；特种设备登记变更", "验收合格文件、检查许可、书面授权", "证照与授权齐备"],
        ["阶段五 运营提升", "第31—36月", "价格与渠道治理；会员与协议客户重建；在地文化落地；资产重整与债务优化",
         "OTA评分与内容运营；MICE与协议客户开发；品牌方收益管理支持；客史数据迁移打通", "价格与渠道月报、评分趋势、资产重整方案", "达产经营现金流达测算值"]]
sh("11 存量改造工作步骤", ["阶段", "起止", "对内工作", "对外工作", "交付物", "放行闸口"], rows, [20, 12, 40, 48, 34, 30],
   note="★ 对外合作第一顺位为设计方与咨询顾问团队，非工程总承包与设备供应商；阶段性改造与阶段性开业不成立")

# 12 全生命周期分工
rows = [["第一顺位", "咨询顾问团队", "阶段〇起全程", "投资可行性复核、造价审价、方案比选、市场与品牌定位复核"],
        ["第二顺位", "品牌设计方", "阶段〇末至阶段一", "视觉识别体系、品牌标准落地规范"],
        ["第三顺位", "产品设计方", "阶段一", "客房产品定义、房型标准化、样板间"],
        ["第四顺位", "机电设计方、消防设计方", "阶段一", "隐蔽工程与消防系统施工图、报建文件"],
        ["第五顺位", "施工总承包、主要设备供应商", "阶段二", "按设计成果实施与供货"]]
sh("12 全生命周期分工", ["顺位", "合作方类别", "介入时点", "核心交付"], rows, [12, 30, 22, 56],
   note="全服务式酒店重大改造的权重分配：前期由设计方与咨询顾问决定，中期由施工与设备决定，末期由运营与资产重组决定")

# 13 数据来源
sh("13 数据来源", ["级别", "来源", "用途", "可信度"], [
 ["一级 业主一手", "业主资料(2).xlsx 近三年数据；近24个月经营指标；2026年10月利润表（37张部门表）；客源结构与客户反馈；人力数据统计；管网与渗漏状况；消防管网爆裂与维修记录；2026皇冠品牌标准建造篇与运营篇；三次品牌审计非合规报告；2019洲际总部PIP报告；F2-29换牌沟通纪要；各类设备台账；专项限制条件；关于能否消防分批验收的回复；证照与经营资质", "现状基线、隐患事实、合同条款、工程约束", "高（可溯源至表行）"],
 ["一级 第三方评估", "川同力达成房预估函（2025）第0915号（收益法，基准日2025-09-04）", "资产与抵押现状", "高（专业机构出具，预评估函）"],
 ["二级 公开可核验", "携程（酒店编号19857058等）、Agoda、Booking、Trip.com 房型页与评分；wherebest、yourwayholiday 竞对汇总；品牌官网与米其林指南", "竞对房量、面积、价格带、评分", "中高（注明平台与抓取日期）"],
 ["三级 内部研究", "成都UPSCALE/UPPER SCALE/LUXURY市场分析与预测；高星级全服式品牌分级分类；安逸集团十五五规划系列建议（2026-08至2026-11）；新川生产力方法论交叉研判", "定位方法、档次划分、战略对标", "中（须核验锚点）"],
 ["禁用", "「春熙路1,280元/76.3%/977元」；「成都高于全国37%」", "—", "★ 无法溯源的合成数，本报告一律不引用"],
], [16, 74, 26, 24], note="数据来源分级；每条关键数字均标注平台或文件出处")


# 14 奢华档临界房价反解
sh("14 奢华档临界房价", ["口径", "房量(间)", "单间套内(㎡)", "客房单间造价(万元)", "投资(万元)", "临界平均房价(元,不含服务费)", "对应RevPAR(元)", "峰值营收(万元)"], [
 ["三改二（按现有套内38㎡）", 268, 38.03, 21.0, 37105, 1238, 898, 11588],
 ["两改一（满足洲际40㎡条件）", 201, 50.71, 21.0, 37105, 1647, 1194, 11310],
 ["两改一·奢华高配", 201, 50.71, 30.0, 37105, 1647, 1194, 11310],
 ["按奢华品牌50㎡基础房反推", 188, 54.2, 30.0, 37105, 1760, 1277, 11254],
], [30, 12, 14, 18, 12, 22, 16, 15],
   note="★ 反解方法：出租率固定72.53%（与既有测算一致），二分法求解使项目口径净现值等于零的平均房价。201间与188间口径造价未随房量等比下调，为偏高估的保守值（真实值约可再低80元）")

# 14b 价格-净现值曲线
sh("14b 房价与净现值曲线", ["平均房价(元)", "项目口径净现值(万元)", "说明"], [
 [800, -20218, ""], [1000, -10978, ""], [1100, -6358, ""], [1200, -1739, ""],
 [1238, 0, "★ 临界点：268间口径奢华档打平所需房价"],
 [1300, 2881, ""], [1400, 7501, ""], [1500, 12121, ""],
 [1600, 16741, ""], [1800, 25980, ""], [2000, 35220, "对应奢华档价格带下限"],
], [18, 22, 44],
   note="268间·三改二·奢华档收入结构·造价37105万元·停业26个月；出租率72.53%固定")
from openpyxl.utils import get_column_letter

XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v7.0_2026-11-15.xlsx")
wb.save(XLSX)
print("Excel:", XLSX, round(os.path.getsize(XLSX) / 1024), "KB", len(wb.sheetnames), "sheets")
for n in wb.sheetnames: print("   ", n)
