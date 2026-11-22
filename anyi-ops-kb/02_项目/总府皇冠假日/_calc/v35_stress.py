# -*- coding: utf-8 -*-
"""v35：外部奢牌方案（S7B）现实性压力测试
   ① 3改2 面积门槛算术自洽性检验
   ② ADR / 出租率 / 部门营业利润率 三维压力测试 + 盈亏平衡 ADR
   ③ 房量约束情景（268 / 254 / 226 / 208 间）
   ④ 概率加权期望值与决策门槛
   数据源：v9.json（造价参数）、v10_econ.py（IRR/NPV/回收期算法）、area_base.py（面积与造价结构）
"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v35.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()

RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]

L("=== 0. v9.json S7 原始参数 ===")
S7 = RES["S7"]
for kk, vv in S7.items():
    if kk not in ("acf", "cash"):
        L("   %-14s %s" % (kk, vv))

# ══════════════ ① 面积门槛算术 ══════════════
L("")
L("=== 1. 3改2 面积门槛自洽性检验 ===")
GUEST_NET = 10192.0      # 客房套内总面积 ㎡
SELLABLE = 402
STOCK_ROOM = 25.0        # 普通层大床房套内 ㎡（含卫生间）
STOCK_SUITE = 45.6
GFA_PER = 22645.47 / SELLABLE   # 客房层建面/在售房数
L("客房套内总面积 %.0f ㎡｜在售 %d 间｜单间套内 %.2f ㎡｜单间建面 %.2f ㎡" %
  (GUEST_NET, SELLABLE, GUEST_NET / SELLABLE, GFA_PER))

n32 = 268
L("")
L("【检验一】3 改 2 后每间套内面积（纯套内口径，无额外取面积）")
L("   3 间 × %.1f ㎡ = %.1f ㎡ → 拆 2 间 = %.2f ㎡/间" % (STOCK_ROOM, 3 * STOCK_ROOM, 3 * STOCK_ROOM / 2))
L("   ⇒ 3改2 纯套内面积上限 %.2f ㎡/间" % (3 * STOCK_ROOM / 2))
L("")
L("【检验二】报告称「3 改 2 达 40 ㎡ 以上」，算术是否成立")
L("   268 间 × 40 ㎡ = %.0f ㎡ ＞ 客房套内总面积 %.0f ㎡ → 差 %.0f ㎡ 缺口" %
  (n32 * 40, GUEST_NET, n32 * 40 - GUEST_NET))
L("   ⇒ 268 间在 40 ㎡ 门槛下【物理不可能】；面积全部归客房时上限间数 = %.0f 间（%.2f ㎡/间）" %
  (GUEST_NET / 40, GUEST_NET / n32))
L("   ⇒ 面积_base.py 的 ROOM_AREA_32 对大床房取 48 ㎡（3改2），需 96 ㎡ 净得，")
L("      而 3 间存量仅 75 ㎡ 套内，缺口 21 ㎡/组 —— 该值与 ROOM_AREA 口径不自洽，需注明是否含走廊分摊")
L("")
L("【检验三】候选奢牌面积门槛下的最大房量（套内口径）")
for brand, need in (("尼依格罗", 40.0), ("兰博基尼", 49.0), ("丽晶（全大户型，参照 60）", 60.0)):
    L("   %-22s 门槛 %.0f ㎡ → 最大 %3.0f 间" % (brand, need, GUEST_NET / need))
L("")
L("【检验四】建面口径下 3改2 的每间建面（含走廊分摊）")
L("   3 间 × %.2f ㎡建面 = %.1f ㎡ → 2 间 = %.1f ㎡/间建面" % (GFA_PER, 3 * GFA_PER, 3 * GFA_PER / 2))
L("   ⇒ 若品牌门槛按建面计（尼依格罗口径未明示套内/建面），268 间成立；")
L("      若按套内计，268 间只能做到 %.1f ㎡/间，低于尼依格罗 40 ㎡ 与兰博基尼 49 ㎡" % (GUEST_NET / n32))

# ══════════════ ② 经营模型（可参数化）══════════════
def model(n_rooms, adr, occ, gop, nonroom, capex, months,
          base=0.030, mkt=0.025, loy=0.020, ffe=0.040, inc=0.100):
    room_rev = n_rooms * 365 * occ * adr / 1e4
    total = room_rev * nonroom
    bb_y = total * base
    br_m = bb_y * 0.35 / 12.0
    mcf = []
    for tt in range(1, 241):
        rev = 0.0
        if tt > months:
            since = tt - months
            ramp = min(1.0, 0.62 + 0.038 * since)
            rev = (total / 12.0) * ramp
        g = rev * gop
        r_ = rev / total if total else 0
        owner = (g - bb_y * r_ - total * mkt * r_ - total * loy * r_
                 - total * ffe * r_ - g * inc)
        cash = owner
        if tt <= months:
            cash -= 284.0; cash -= br_m
        half = max(1, months // 2)
        if 1 <= tt <= half: cash -= capex * 0.6 / half
        elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
        if tt > months:
            since = tt - months
            if since < 12: cash -= total * 0.085 / 12.0
            elif since < 24: cash -= total * 0.030 / 12.0
            if since < 6: cash -= total * 0.012 / 6.0
        mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(20)]
    ann = (total * gop - total * (base + mkt + loy + ffe) - total * gop * inc)
    grp = [-capex] + [ann] * 20
    inc_cf = [acf[i] - BASE["owner_cf"] for i in range(20)]
    def pv(cf, r=0.08): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
    return dict(rev=total, npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                irr_grp=V10.irr(grp), pb_grp=(round(capex / ann, 2) if ann > 0 else None),
                irr_inc=V10.irr(inc_cf), ann=ann)

# S7 基准（S7B 的造价与停业参数与 S7 相同，仅 ADR 不同）
N0 = S7["n_rooms"]; CAPEX0 = S7["mep"] + S7["fitout"]; MONTHS = S7["months"]
MEP = S7["mep"]; FIT = S7["fitout"]
# 段三造价结构（自 area_base.py OWNER_2024_SECOND）：客房相关 6,000 万 / 公区固定 2,900 万
ROOM_SHARE = 6000.0 / 8700.0
def capex_for(n):
    """房量变化时：段二机电不变，段三客房部分随房量缩放、公区部分固定"""
    return MEP + FIT * (ROOM_SHARE * n / N0 + (1 - ROOM_SHARE))
L("")
L("=== 2. S7B 三维压力测试（房量 268、造价 %.1f 万、停业 %d 月）===" % (CAPEX0, MONTHS))
L("   改造前基线年营收 %.1f 万" % BASE["total_rev"])
L("")
L("   %-8s %-8s %-8s %12s %10s %10s %10s" % ("ADR", "出租率", "营业利润率", "年营收", "净现值", "全口径IRR", "集团回收"))
GRID = []
for adr in (2000, 2500, 3000):
    for occ in (0.65, 0.70, 0.75):
        for gop in (0.30, 0.35, 0.40):
            m = model(N0, adr, occ, gop, 1.85, CAPEX0, MONTHS)
            GRID.append((adr, occ, gop, m))
            L("   %-8d %-8.2f %-8.2f %12.1f %10.1f %10s %10s" % (
                adr, occ, gop, m["rev"], m["npv"],
                ("%.2f%%" % (m["irr"] * 100)) if m["irr"] is not None else "无解",
                m["pb_grp"] if m["pb_grp"] else "不适用"))
L("")
L("=== 3. 盈亏平衡 ADR（净现值 = 0）===")
for occ in (0.65, 0.70, 0.75):
    for gop in (0.30, 0.35, 0.40):
        lo, hi = 500.0, 8000.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if model(N0, mid, occ, gop, 1.85, CAPEX0, MONTHS)["npv"] < 0: lo = mid
            else: hi = mid
        L("   出租率 %.2f｜部门营业利润率 %.2f → 平衡 ADR = %.0f 元" % (occ, gop, (lo + hi) / 2))
L("")
L("=== 4. 房量约束情景（ADR 3,000、occ 0.70、GOP 0.40、非房 1.85）===")
L("   %-8s %-12s %12s %12s %10s %10s" % ("房量", "面积口径", "改造投资", "年营收", "净现值", "全口径IRR"))
for n, note in ((268, "套内 38.0 ㎡"), (254, "套内 40.1 ㎡"), (226, "套内 45.1 ㎡"), (208, "套内 49.0 ㎡")):
    m = model(n, 3000, 0.70, 0.40, 1.85, capex_for(n), MONTHS)
    L("   %-8d %-12s %12.1f %12.1f %10.1f %10s" % (
        n, note, capex_for(n), m["rev"], m["npv"],
        ("%.2f%%" % (m["irr"] * 100)) if m["irr"] is not None else "无解"))
L("")
L("=== 5. 概率加权期望值（诚实概率）===")
m_best = model(N0, 3000, 0.70, 0.40, 1.85, CAPEX0, MONTHS)
m_mid = model(N0, 2500, 0.70, 0.35, 1.70, CAPEX0, MONTHS)
m_low = model(N0, 2000, 0.65, 0.30, 1.60, CAPEX0, MONTHS)
L("   情景A 全兑现(3,000/0.70/0.40)：净现值 %+.1f 万" % m_best["npv"])
L("   情景B 中性(2,500/0.70/0.35)：净现值 %+.1f 万" % m_mid["npv"])
L("   情景C 低落(2,000/0.65/0.30)：净现值 %+.1f 万" % m_low["npv"])
# 概率：品牌愿意接盘（未接触、面积不达标、春熙路存量物业）12%；品牌愿意且价格带兑现 30%
P_BRAND = 0.12; P_BAND = 0.30
ev = P_BRAND * (P_BAND * m_best["npv"] + (1 - P_BAND) * m_mid["npv"]) + (1 - P_BRAND) * m_low["npv"]
L("   P(品牌方接盘)=%.0f%%｜P(价格带兑现 | 接盘)=%.0f%%" % (P_BRAND * 100, P_BAND * 100))
L("   概率加权期望净现值 = %+.1f 万" % ev)
L("")
L("=== 6. 与居舍的每间客房收入对照 ===")
for adr, occ, nm in ((2500, 0.75, "居舍 中档假设(2,500×0.75,100间客房)"),
                     (2000, 0.75, "居舍 保守(2,000×0.75)"),
                     (3000, 0.75, "居舍 上限(3,000×0.75)")):
    L("   %-34s 每间客房年收入 %.1f 万" % (nm, 100 * 365 * occ * adr / 1e4))
for n, adr, occ in ((268, 3000, 0.70), (268, 2500, 0.70), (254, 3000, 0.70)):
    L("   S7B %d 间 %.0f 元×%.2f → 每间客房年收入 %.1f 万" % (n, adr, occ, n * 365 * occ * adr / 1e4 / n))
L("")
L("DONE")
