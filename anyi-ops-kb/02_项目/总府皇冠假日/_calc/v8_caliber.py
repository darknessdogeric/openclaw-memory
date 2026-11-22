# -*- coding: utf-8 -*-
"""v8 口径校准器：三重口径对照
  口径1 全口径项目 IRR（本次实测，经营现金流含存量亏损与停业损失）
  口径2 增量口径 IRR（相对"不改造"反事实，用于表达"改造的必要性"）
  口径3 集团可比口径（改造后经营现金流 20 年、初始投资改造投资、停业期支出单列不进 IRR）
  并反推集团 715 定稿 17% / 5.6 年 隐含的稳态年现金流，量化与本次测算的差额
"""
import io, os, sys, json, importlib.util
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v8.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

spec = importlib.util.spec_from_file_location("v7g", os.path.join(D, "v7g.py"))
V = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(V)
except Exception as e:
    L("import note:", str(e)[:200])
RES, DIRS, run = V.RES, V.DIRS, V.run

BASE_CF = -1924.0     # 改造前年均经营现金流（业主口径，USALI 实测，KB 出处）
BASE_DECAY = 0.05     # 反事实劣化情景：设施老化与品牌失分延续
GROUP_INV = 18000.0  # 集团 715 定稿总府改造投资
GROUP_PB = 5.6       # 集团 715 定稿总府投资回收期
GROUP_IRR = 0.17     # 集团 715 定稿总府 IRR

def irr(cf, lo=-0.99, hi=10.0):
    def f(r): return sum(c / (1 + r) ** i for i, c in enumerate(cf))
    try:
        a, b = f(lo), f(hi)
    except Exception:
        return None
    if a * b > 0:
        return None
    for _ in range(500):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def npv(cf, r=0.08):
    return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)

def payback(cf):
    c = 0.0
    for i, x in enumerate(cf):
        c += x
        if c >= 0:
            return i + 1
    return None

def level_cf_for_irr(target, inv, n=20):
    """求使 IRR=target 的等额年金（t=1..n 每年 X，t=0 出资 inv）"""
    lo, hi = 0.0, inv * 3
    for _ in range(200):
        mid = (lo + hi) / 2
        cf = [-inv] + [mid] * n
        r = irr(cf)
        if r is None:
            hi = mid
            continue
        if r < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

# ── 口径3：集团可比口径现金流（改造后经营现金流，不扣停业期损失与存量基线）──
def group_comparable(dk):
    d = DIRS[dk]
    og = RES[dk]["owner_gop_steady"]          # 稳态业主经营利润（万元/年）
    # 复业爬坡：按模型月度 ramp 的年度均值，Y1 约 0.83、Y2 起 1.0
    ramp_y1 = 0.83
    cfs = [-d["capex"]]
    for y in range(1, 21):
        cfs.append(og * (ramp_y1 if y == 1 else 1.0))
    return cfs, og

# ── 口径2：增量口径（相对不改造反事实）──
def incremental(dk, decay=False):
    x = RES[dk]
    base_cfs = x["acf"]
    cfs = []
    for y in range(1, 21):
        base = BASE_CF * ((1 - BASE_DECAY) ** (y - 1)) if decay else BASE_CF
        cfs.append(base_cfs[y - 1] - base)
    return cfs

OUT = {}
L("=== 集团 715 定稿隐含值反推 ===")
imp_irr = level_cf_for_irr(GROUP_IRR, GROUP_INV)
imp_pb = GROUP_INV / GROUP_PB
L("  由 IRR %.0f%%、%d 年、%s 万投资反推等额年现金流 = %.0f 万/年" % (GROUP_IRR * 100, 20, int(GROUP_INV), imp_irr))
L("  由回收期 %.1f 年反推年现金流 = %.0f 万/年" % (GROUP_PB, imp_pb))
L("  → 两者自洽（说明集团用的是 20 年等额年金口径）")

L("\n=== 三口径对照 ===")
for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
    x = RES[k]
    cfs_all = x["acf"]
    cfs_inc = incremental(k, decay=False)
    cfs_inc_d = incremental(k, decay=True)
    cfs_grp, og = group_comparable(k)
    OUT[k] = dict(
        name=x["name"], capex=x["capex"], per_key=x["per_key"],
        steady_rev=x["steady_rev"], owner_gop=og,
        irr_full=x["irr20"], npv_full=x["npv20"], pb_full=x["pb"],
        irr_inc=irr(cfs_inc), npv_inc=npv(cfs_inc), pb_inc=payback(cfs_inc),
        irr_inc_decay=irr(cfs_inc_d), pb_inc_decay=payback(cfs_inc_d),
        irr_grp=irr(cfs_grp), npv_grp=npv(cfs_grp), pb_grp=payback(cfs_grp),
    )
    L("--- %s  投资 %s 万 单间 %.2f 万 ---" % (k, x["capex"], x["per_key"]))
    L("  稳态年营业收入 %s 万 ｜ 稳态业主经营利润 %s 万" % (x["steady_rev"], og))
    L("  口径1 全口径      IRR %s ｜ NPV %s ｜ 静态回收 %s" %
      (("%.2f%%" % (x["irr20"] * 100)) if x["irr20"] else "无", x["npv20"], x["pb"]))
    L("  口径2 增量口径    IRR %s ｜ NPV %s ｜ 静态回收 %s" %
      (("%.2f%%" % (OUT[k]["irr_inc"] * 100)) if OUT[k]["irr_inc"] else "无",
       OUT[k]["npv_inc"], OUT[k]["pb_inc"]))
    L("  口径2b 增量(劣化) IRR %s ｜ 静态回收 %s" %
      (("%.2f%%" % (OUT[k]["irr_inc_decay"] * 100)) if OUT[k]["irr_inc_decay"] else "无", OUT[k]["pb_inc_decay"]))
    L("  口径3 集团可比    IRR %s ｜ NPV %s ｜ 静态回收 %s" %
      (("%.2f%%" % (OUT[k]["irr_grp"] * 100)) if OUT[k]["irr_grp"] else "无",
       OUT[k]["npv_grp"], OUT[k]["pb_grp"]))
    L("  → 与集团隐含 %.0f 万/年的差额 = %.0f 万元/年" % (imp_irr, og - imp_irr))

L("\n=== 达到集团口径所需的稳态年业主经营利润 ===")
need_irr = level_cf_for_irr(GROUP_IRR, GROUP_INV)
for k in ("D1", "D1X", "D3", "D3R"):
    d = DIRS[k]
    inv = d["capex"]
    need = level_cf_for_irr(GROUP_IRR, inv)
    cf = [-inv] + [need] * 20
    L("  %s：投资 %s 万 → 需稳态业主经营利润 %.0f 万/年（本次测算 %.0f 万，差 %.0f 万）→ 静态回收 %.1f 年" %
      (k, int(inv), need, RES[k]["owner_gop_steady"], RES[k]["owner_gop_steady"] - need, inv / need))

json.dump(dict(group=dict(inv=GROUP_INV, pb=GROUP_PB, irr=GROUP_IRR,
                          implied_cf_irr=round(imp_irr, 1), implied_cf_pb=round(imp_pb, 1)),
               base_cf=BASE_CF, dirs=OUT),
          open(os.path.join(T, "v8.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
