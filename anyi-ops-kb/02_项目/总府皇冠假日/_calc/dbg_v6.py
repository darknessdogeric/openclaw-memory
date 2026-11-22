# -*- coding: utf-8 -*-
import sys, io, os
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc")
import v6_launch as V
import v6_run_export as E
out = open(r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\dbg.txt", "w", encoding="utf-8")
r = E.run_monthly("D2", "中性", 20, 284.0, 12)
for y in r["years"][:6]:
    out.write("Y%d rev=%s rooms=%s fnb=%s banq=%s gop=%s rate=%s open=%s closed=%s\n" % (
        y["year"], y["revenue"], y["rooms_rev"], y["fnb"], y["banq"], y["gop"],
        y["gop_rate"], y["open_months"], y["closed_months"]))
out.write("--- 单月 ---\n")
for t in r["timeline"]:
    if t["m"] in (1, 18, 19, 24, 25, 30, 31):
        out.write("m=%s %s mon=%s adr=%s occ=%s sold=%s rev=%s gop=%s rate=%s\n" % (
            t["m"], t["state"], t["mon"], round(t["adr"], 1), round(t["occ"], 3),
            round(t["rooms_sold"]), round(t["revenue"], 1), round(t["gop"], 1),
            round(t["gop"] / t["revenue"], 3) if t["revenue"] else 0))
out.write("--- 直接调 month_revenue ---\n")
dk = dict(V.DIRECTIONS["D2"])
m = E.month_revenue(dk, "中性", 3, 6)
for k, v in m.items():
    out.write("  %s = %s\n" % (k, round(v, 3) if isinstance(v, float) else v))
out.write("mix=%s dept_gop=%s\n" % (V.TIER["D2" and "intl_upper_upscale"]["mix"], V.TIER["intl_upper_upscale"]["dept_gop"]))
out.close()
