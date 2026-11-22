# -*- coding: utf-8 -*-
import sys, io, os, json
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc")
import v6_launch as V
import v6_run_export as E
f = open(r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\v6_summary.txt", "w", encoding="utf-8")
res = {}
for k in ("D1", "D2", "D3"):
    for sc in ("保守", "中性", "乐观"):
        r = E.run_monthly(k, sc, 20, 284.0, V.DIRECTIONS[k]["closure_start_month"])
        res[(k, sc)] = r
        irr = ("%.2f%%" % (r["irr"] * 100)) if r["irr"] else "无可解"
        pb = ("%.1f" % r["payback"]) if r["payback"] else "未回收"
        f.write("%s %-3s | CAPEX %6.0f | 停业 %2d月 损失 %7.1f万 | Y5营收 %7.1f万 | GOP率 %5.1f%% | 品牌费率 %4.1f%% | 业主GOP %7.1f万 | IRR %8s | NPV %8.1f | 回收 %s\n" % (
            k, sc, r["capex"], r["closure_months"], r["closure_total"], r["rev_y5"],
            r["gop_rate_y5"] * 100,
            sum(y["fee_total"] for y in r["years"][2:5]) / max(1, sum(y["revenue"] for y in r["years"][2:5])) * 100,
            r["owner_gop_y5"], irr, r["npv"], pb))
f.write("\n--- 分期开业情景（条件：消防审查机构认可分区验收）---\n")
for k in ("D2", "D3"):
    full = res[(k, "中性")]
    ph = E.run_monthly(k, "中性", 20, 284.0, V.DIRECTIONS[k]["closure_start_month"], phased=E.PHASED[k])
    f.write("%s 一次全停业: 停业%s月 损失%.0f万 IRR %s NPV %.0f 回收 %s\n" % (
        k, full["closure_months"], full["closure_total"],
        ("%.2f%%" % (full["irr"]*100)) if full["irr"] else "无", full["npv"],
        ("%.1f" % full["payback"]) if full["payback"] else "未回收"))
    f.write("%s 分期开业  : 停业%s月 损失%.0f万 IRR %s NPV %.0f 回收 %s | 损失少 %.0f 万\n" % (
        k, ph["closure_months"], ph["closure_total"],
        ("%.2f%%" % (ph["irr"]*100)) if ph["irr"] else "无", ph["npv"],
        ("%.1f" % ph["payback"]) if ph["payback"] else "未回收",
        full["closure_total"] - ph["closure_total"]))
f.write("\n--- 开工月份敏感性（D2 中性 18 个月停业，损失 万元）---\n")
for st in range(1, 13):
    _, t = V.closure_loss(st, 18, 284.0)
    f.write("  %2d月开工: %8.1f\n" % (st, t))
f.close()
