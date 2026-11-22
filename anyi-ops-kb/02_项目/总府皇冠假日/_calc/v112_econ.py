# -*- coding: utf-8 -*-
"""v112：以 v111 重建造价与工期为准，重算四路径经济性"""
import json, os, io, math, sys

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v112.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# ── 先修 v111 的两处显示 bug ──
vp = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\v111_capex.py"
s = io.open(vp, encoding="utf-8").read()
s = s.replace('"per_room": round((sub + cont + interest) * 10000 / ROOMS, 1),',
              '"per_room": round((sub + cont + interest) / ROOMS, 1),')
s = s.replace('(sum(i["amount"] for i in COMMON), sum(i["amount"] for i in COMMON) * 10000 / GFA))',
              '(sum(c[3] for c in COMMON), sum(c[3] for c in COMMON) * 10000 / GFA))')
s = s.replace('% sum(i["amount"] for i in COMMON),', '% sum(c[3] for c in COMMON),')
io.open(vp, "w", encoding="utf-8").write(s)
import subprocess
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
r = subprocess.run([PY, vp], capture_output=True, text=True, encoding="utf-8", errors="replace",
                   env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
L("v111 rc=%d" % r.returncode)
V = json.load(open(os.path.join(T, "v111.json"), encoding="utf-8"))
CAPEX, DUR = V["capex"], V["duration"]
L("造价： " + "｜".join("%s %.0f 万 (%.0f 元/㎡, %.1f 万/间)" %
    (k, CAPEX[k]["total"], CAPEX[k]["per_sqm"], CAPEX[k]["per_room"]) for k in ("P1","P2","P3","P4")))
L("停业： " + "｜".join("%s %d 月 (区间 %d—%d)" % (k, DUR[k]["m"], DUR[k]["lo"], DUR[k]["hi"])
    for k in ("P1","P2","P3","P4")))

# ── 沿用 v98 的经营模型内核（已与台账对账） ──
D = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
B = D["base"]
PATHS = D["paths"]

def npv(rate, cfs): return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cfs))
def irr(cfs, lo=-0.90, hi=2.0, tol=1e-9):
    try: f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    except ZeroDivisionError: return None
    if f_lo * f_hi > 0: return None
    for _ in range(400):
        mid = (lo + hi) / 2
        try: f_mid = npv(mid, cfs)
        except ZeroDivisionError: return None
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2
def payback(cfs):
    cum = 0.0
    for i, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0: return i - 1 + (-prev / cf)
    return None

def annual_op(p, adr=None, occ=None, nonroom_cap=None):
    adr = p["adr_excl_svc"] if adr is None else adr
    occ = p["occ"] if occ is None else occ
    nc = p["nonroom_capability"] if nonroom_cap is None else nonroom_cap
    rn = p["rooms"] * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * B["svc_pct_of_room_B"]
    occ_ratio = occ / B["occ_ttm"]
    nonroom_B = B["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * nc
    rev_B = room_B + nonroom_B
    gop = room_B * B["dept_margin"]["房务部"] + nonroom_B * B["nonroom_margin_blend"]
    scale_room = p["rooms"] / B["rooms"]
    ANN = B["annualize_10m"]
    undist = {
        "A&G（行政及总办）": B["cost_10m"]["A&G"] * ANN * (0.75 + 0.25 * scale_room),
        "POM（工程部维保）": B["cost_10m"]["POM"] * ANN * (0.70 + 0.30 * scale_room),
        "IT & Telecom": B["cost_10m"]["IT"] * ANN,
        "S&M（市场销售，含渠道佣金）": B["cost_10m"]["S&M"] * ANN * occ_ratio,
        "Energy（未分摊能源）": B["cost_10m"]["能源"] * ANN * (0.55 + 0.45 * scale_room),
    }
    undist_total = sum(undist.values())
    ihg_gop = gop - undist_total
    mode = p["fee_mode"]
    if mode == "delegate":
        license = rev_B * B["license_pct_rev_B"]
        imf = max(0.0, ihg_gop - license) * B["imf_pct"]
    elif mode in ("franchise_ihg", "franchise_ext"):
        license = room_B * 0.05; imf = 0.0
    else:
        license = 0.0; imf = 0.0
    fee = license + imf
    adj_gop = ihg_gop - fee
    return {"room_B": room_B, "svc": svc, "room_A": room_B + svc, "nonroom_B": nonroom_B,
            "rev_B": rev_B, "rev_A": rev_B + svc, "gop": gop, "undist": undist,
            "undist_total": undist_total, "ihg_gop": ihg_gop, "license": license, "imf": imf,
            "fee": fee, "adj_gop": adj_gop, "adr": adr, "occ": occ}

def project_cf(p, capex, life=20, rate=0.08, ramp=6, sustain_pct=0.02,
               adr=None, occ=None, nonroom_cap=None, brand_share=0.0, subsidy=0.0,
               downtime=None, fee_mult=1.0):
    dt = p["downtime"] if downtime is None else downtime
    st = annual_op(p, adr, occ, nonroom_cap)
    owner_capex = capex * (1 - brand_share) - subsidy
    dt_monthly = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * 0.6
                  + B["cost_10m"]["能源"] / 10 * 0.25)
    cfs = [-owner_capex]
    for _ in range(dt): cfs.append(-dt_monthly)
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p, adr, occ, nonroom_cap)
        rev_B = r["rev_B"] * k
        gop = r["gop"] * k
        undist = r["undist_total"] * (0.85 + 0.15 * k)
        ihg = gop - undist
        fee = r["fee"] * k * fee_mult
        adj = ihg - fee
        sustain = rev_B * sustain_pct / 12
        cfs.append(adj - sustain)
    for y in range(life):
        r = annual_op(p, adr, occ, nonroom_cap)
        sustain = r["rev_B"] * sustain_pct
        cfs.append(r["adj_gop"] * fee_mult - sustain)
    return {"npv": npv(rate, cfs), "irr": irr(cfs), "payback": payback(cfs),
            "owner_capex": owner_capex, "cfs": cfs, "shutdown_cf_total": -dt_monthly * dt,
            "stable": st}

KS = ["P1", "P2", "P3", "P4"]
results = {}
for k in KS:
    p = dict(PATHS[k]); p["downtime"] = DUR[k]["m"]
    capex = CAPEX[k]["total"]
    r = project_cf(p, capex)
    st = r["stable"]
    op_cf = st["adj_gop"] - st["rev_B"] * 0.02
    results[k] = {
        "name": p["name"], "rooms": p["rooms"], "downtime": DUR[k]["m"],
        "downtime_lo": DUR[k]["lo"], "downtime_hi": DUR[k]["hi"],
        "capex": capex, "per_sqm": CAPEX[k]["per_sqm"], "per_room": CAPEX[k]["per_room"],
        "capex_items": CAPEX[k]["items"],
        "owner_capex": round(r["owner_capex"], 2),
        "adr": st["adr"], "occ": st["occ"],
        "room_rev_A": round(st["room_A"], 2), "nonroom_rev_B": round(st["nonroom_B"], 2),
        "rev_A_stable": round(st["rev_A"], 2),
        "vs_base_rev_A": round(st["rev_A"] - B["rev_A_fy2025"], 2),
        "adj_gop": round(st["adj_gop"], 2), "fee": round(st["fee"], 2),
        "op_cf_stable": round(op_cf, 2),
        "op_cf_margin": round(op_cf / st["rev_A"], 4),
        "shutdown_cf_total": round(r["shutdown_cf_total"], 2),
        "npv": round(r["npv"], 2),
        "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
        "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
        "simple_payback": round(capex / op_cf, 2) if op_cf > 0 else None,
    }
    L("%s capex=%.0f 停业=%d月 营收A=%.0f 经营现金流=%.0f NPV=%.0f IRR=%s 回收=%s 简单回收=%.1f年" % (
        k, capex, DUR[k]["m"], st["rev_A"], op_cf, r["npv"], results[k]["irr_pct"],
        results[k]["payback_yr"], results[k]["simple_payback"] or -1))

# 盈亏平衡
be = {}
for k in KS:
    rn = PATHS[k]["rooms"] * 365
    req = B["room_A_fy2025"] * 10000 / rn
    assumed = results[k]["rev_A_stable"] / PATHS[k]["rooms"] * 10000 / 365
    be[k] = {"required_revpar": round(req, 0), "assumed_revpar": round(assumed, 0),
             "gap": round(assumed - req, 0), "pass": assumed >= req}

# 敏感性（含造价 ±30%，因造价不确定性显著放大）
sens = {}
for k in KS:
    p = dict(PATHS[k]); p["downtime"] = DUR[k]["m"]
    capex = CAPEX[k]["total"]; s = {}
    for lbl, kw in (("ADR -10%", dict(adr=PATHS[k]["adr_excl_svc"] * 0.9)), ("ADR 基准", dict()),
                    ("ADR +10%", dict(adr=PATHS[k]["adr_excl_svc"] * 1.1)),
                    ("OCC -5pp", dict(occ=PATHS[k]["occ"] - 0.05)), ("OCC 基准", dict()),
                    ("OCC +5pp", dict(occ=PATHS[k]["occ"] + 0.05)),
                    ("停业下限", dict(downtime=DUR[k]["lo"])), ("停业基准", dict()),
                    ("停业上限", dict(downtime=DUR[k]["hi"]))):
        s[lbl] = round(project_cf(p, capex, **kw)["npv"], 0)
    for lbl, cp in (("CAPEX -30%", capex * 0.70), ("CAPEX -15%", capex * 0.85),
                    ("CAPEX 基准", capex), ("CAPEX +15%", capex * 1.15), ("CAPEX +30%", capex * 1.30)):
        s[lbl] = round(project_cf(p, cp)["npv"], 0)
    for lbl, rt in (("折现率 6%", 0.06), ("折现率 8%", 0.08), ("折现率 10%", 0.10)):
        s[lbl] = round(project_cf(p, capex, rate=rt)["npv"], 0)
    for lbl, lf in (("评价期 10 年", 10), ("评价期 20 年", 20), ("评价期 30 年", 30)):
        s[lbl] = round(project_cf(p, capex, life=lf)["npv"], 0)
    for lbl, bs in (("品牌方承担 0%", 0.0), ("品牌方承担 20%", 0.20), ("品牌方承担 30%", 0.30)):
        s[lbl] = round(project_cf(p, capex, brand_share=bs)["npv"], 0)
    s["房价不提升（ADR维持现状）"] = round(project_cf(
        p, capex, adr=B["adr_A_24m"] / (1 + B["svc_pct_of_room_B"]), occ=B["occ_24m"])["npv"], 0)
    sens[k] = s
    L("敏感性 %s：%s" % (k, json.dumps(s, ensure_ascii=False)))

OUT = {"meta": {"title": "v112 四路径经济性（依 v111 重建造价与工期）", "date": "2026-11-15",
                "纠正": "P1 造价 11,066 → 24,517 万元；P1 停业 8 → 12 个月",
                "评价": "项目口径 NPV/IRR（不含存量债务利息）；评价期 20 年；折现率 8%",
                "capex_note": V["reconciliation"]["note"], "capex_action": V["reconciliation"]["action"]},
       "base": B, "results": results, "breakeven": be, "sensitivity": sens,
       "duration": DUR, "capex": CAPEX}
io.open(os.path.join(T, "v112.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("")
L("写出 v112.json")
L("DONE")
