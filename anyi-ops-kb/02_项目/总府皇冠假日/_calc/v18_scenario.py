# -*- coding: utf-8 -*-
"""v18：三方安全评估结论 → 三情景方案空间与财务结果
   情景 A 认定须整体改造（现行基准）
   情景 B 认定部分系统可延寿、须分段实施
   情景 C 认定可通过维修改造维持经营条件 → 整体改造不成立，仅必要局部整改
"""
import io, os, sys, re, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
LOG = open(os.path.join(T, "v18.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(V10)
except Exception as e: L("v10 note:", str(e)[:160])
ECON = {x["dk"]: x for x in json.load(open(os.path.join(T, "v10_econ.json"), encoding="utf-8"))}

def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v*100)) if v is not None else "无可解内部收益率"

OUT = {}

# ══ 情景 A：认定须整体改造（现行基准）══
a = {}
for k in ("S1", "S4", "S5", "S3", "S2", "S6", "S7"):
    x = RES[k]; e = ECON[k]
    a[k] = dict(loss=x["loss"], mep=x["mep"], fit=x["fitout"], months=x["months"],
                 capex=x["mep"]+x["fitout"], total=x["mep"]+x["fitout"]+x["loss"],
                 irr20=e["irr20"], npv20=e["npv20"], pb=e["pb"],
                 irr_grp=e["irr_grp"], pb_grp=e["pb_grp"], irr_inc=e["irr_inc"])
OUT["A"] = a

# ══ 情景 B：认定部分系统可延寿、须分段实施 ══
# 段二按可压缩 30% 计（依据：2024 底稿中部分系统为整体更换口径，而第二批次台账显示
# 1#-8# 电梯已于 2022-2026 更换、部分给排水与配电设备服役状态优于预期）；
# 停业月数由 12 个月压缩至 8 个月（分段实施、局部不停业）
MEP_KEEP = 0.70
b = {}
for k in ("S1", "S4", "S5", "S3", "S2", "S6", "S7"):
    x = RES[k]
    mep = x["mep"] * MEP_KEEP
    months = 8 if x["months"] >= 12 else max(6, x["months"] - 4)
    e = V10.econ(x, mep_override=mep, months_override=months)
    b[k] = dict(loss=815.0*months, mep=mep, fit=x["fitout"], months=months,
                capex=mep+x["fitout"], total=mep+x["fitout"]+815.0*months,
                irr20=e["irr20"], npv20=e["npv20"], pb=e["pb"],
                irr_grp=e["irr_grp"], pb_grp=e["pb_grp"], irr_inc=e["irr_inc"])
OUT["B"] = b
L("=== 情景对比 ===")
for k in ("S1", "S4", "S5", "S3", "S2", "S6", "S7"):
    L("%s  A: 段二%.1f 停业%d月 改造%.1f 总%.1f IRR%s | B: 段二%.1f 停业%d月 改造%.1f 总%.1f IRR%s" % (
        k, a[k]["mep"], a[k]["months"], a[k]["capex"], a[k]["total"], P(a[k]["irr20"]),
        b[k]["mep"], b[k]["months"], b[k]["capex"], b[k]["total"], P(b[k]["irr20"])))

# ══ 情景 C：认定可通过维修改造维持经营条件 ══
# 整体改造不成立，仅保留必要局部整改（安全合规必需项）
LOCAL_ITEMS = [
    ("消防现代化修正（报警主机更换、喷淋与联动更新、气体灭火补齐、消防水炮新增）", 420),
    ("电梯 6 台大修或更换（9#—11#、14#—16#）", 360),
    ("发电机组 2 台更换与油箱恢复、储油罐重建", 320),
    ("给排水隐蔽与末端更新（14 台排污泵、锈蚀管段、中水回用）", 260),
    ("竖井与隐蔽工程分层重排", 320),
    ("客房周期性更新改造（沿用皇冠标准，保留石材）", 2904),
]
LOCAL_TOTAL = sum(v for _, v in LOCAL_ITEMS)
# 局部整改可分区不停业实施（客房可逐层滚动，机电可分系统切换）
LOCAL_MONTHS = 0
# 现状持续：年经营现金流 −1,924 万元
BASE_CF = -1924.0
def npv5(annual_cf, invest_year0):
    return round(invest_year0 + sum(annual_cf/(1.08**(i+1)) for i in range(5)), 1)
c_keep = npv5(BASE_CF, 0)                 # 完全不改造
c_local = npv5(BASE_CF, -LOCAL_TOTAL)     # 局部整改
OUT["C"] = dict(items=LOCAL_ITEMS, local_total=LOCAL_TOTAL, local_months=LOCAL_MONTHS,
                base_cf=BASE_CF, npv_keep_5y=c_keep, npv_local_5y=c_local,
                note="局部整改不改变盈利能力，5 年窗口净现值劣于不改造；其价值在于消除安全合规隐患")
L("情景C: 局部整改 %.1f 万 | 5年NPV 不改造 %.1f / 局部整改 %.1f" % (LOCAL_TOTAL, c_keep, c_local))

# ══ 三情景汇总（以基准方案 S1 为主，另列 S4）══
summ = []
for k in ("S1", "S4"):
    summ.append(dict(scheme=k, A=a[k], B=b[k]))
OUT["summary"] = summ
json.dump(OUT, open(os.path.join(T, "v18.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
