# -*- coding: utf-8 -*-
"""近24个月真实月度曲线 → 季节性剖面 + 按起停月份的精确停业期损失（替代均摊 815 万/月）"""
import io, os, sys, re, json
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xlrd

P = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件\4. 经营基线数据 财务部 2026. 11.2\近24个月总府皇冠假日酒店主要经营指标.xls"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"

bk = xlrd.open_workbook(P)
sh = bk.sheet_by_index(0)


def rowvals(label):
    for r in range(sh.nrows):
        v = str(sh.cell_value(r, 0)).strip()
        if v == label:
            return [sh.cell_value(r, c) for c in range(1, sh.ncols)]
    return None


months = []
for r in range(sh.nrows):
    if str(sh.cell_value(r, 0)).strip() == "From":
        months = [str(sh.cell_value(r, c)).strip() for c in range(1, sh.ncols)]
        break

rev = rowvals("营业总收入")
gop = rowvals("经营毛利润")
gopr = rowvals("经营毛利率%")
adr = rowvals("平均房价")
occ = rowvals("出租率")
trev = rowvals("每间可售房收入")
roomrev = rowvals("客房收入")
fnbrev = rowvals("餐饮收入")
banqrev = rowvals("会议收入")
misc = rowvals("其它收入")
labor = rowvals("人工成本")
energy = rowvals("能耗成本")
maint = rowvals("维保成本")
avail = rowvals("可售间夜")
sold = rowvals("已售房间")
internal = rowvals("内部用房/免费房")

n = len(months)
print(f"月份数: {n}  区间: {months[0]} → {months[-1]}")

M = []
for i in range(n):
    M.append({
        "ym": months[i], "mon": int(months[i].split("/")[1]),
        "rev": rev[i] or 0, "gop": gop[i] or 0, "gopr": gopr[i] or 0,
        "adr": adr[i] or 0, "occ": occ[i] or 0, "trevpar": trev[i] or 0,
        "room": roomrev[i] or 0, "fnb": fnbrev[i] or 0, "banq": banqrev[i] or 0, "misc": misc[i] or 0,
        "labor": labor[i] or 0, "energy": energy[i] or 0, "maint": maint[i] or 0,
        "avail": avail[i] or 0, "sold": sold[i] or 0, "internal": internal[i] or 0,
    })

print("\n" + "=" * 108)
print("逐月明细（万元 / 元）")
print("=" * 108)
print(f"{'月份':<10}{'营业总收入':>11}{'毛利率':>8}{'ADR':>9}{'出租率':>8}{'RevPAR':>9}{'客房':>10}{'餐饮':>9}{'会议':>9}{'人工':>9}{'能耗':>8}{'维保':>8}{'内部房':>8}")
for m in M:
    print(f"{m['ym']:<10}{m['rev']/1e4:>11.1f}{m['gopr']*100:>8.1f}{m['adr']:>9.0f}{m['occ']*100:>8.1f}"
          f"{m['trevpar']:>9.0f}{m['room']/1e4:>10.1f}{m['fnb']/1e4:>9.1f}{m['banq']/1e4:>9.1f}"
          f"{m['labor']/1e4:>9.1f}{m['energy']/1e4:>8.1f}{m['maint']/1e4:>8.1f}{m['internal']:>8.0f}")

# 季节性
cal = defaultdict(list)
for m in M:
    cal[m["mon"]].append(m)
print("\n" + "=" * 108)
print("同历月均值（2 个年度：2024/10–2025/09 与 2025/10–2026/09）")
print("=" * 108)
print(f"{'历月':<6}{'月均营收(万)':>14}{'月均毛利率':>12}{'月均ADR':>10}{'月均出租率':>13}{'月均RevPAR':>13}{'餐饮占比':>10}{'会议占比':>10}")
season = {}
for k in sorted(cal):
    g = cal[k]
    am = lambda f: sum(x[f] for x in g) / len(g)
    season[k] = {"rev": am("rev"), "gopr": am("gopr"), "adr": am("adr"), "occ": am("occ"),
                 "trevpar": am("trevpar"), "fnb_ratio": am("fnb") / am("rev"), "banq_ratio": am("banq") / am("rev")}
    s = season[k]
    print(f"{k}月{'':<3}{s['rev']/1e4:>14.1f}{s['gopr']*100:>12.1f}{s['adr']:>10.0f}{s['occ']*100:>13.1f}"
          f"{s['trevpar']:>13.0f}{s['fnb_ratio']*100:>10.1f}{s['banq_ratio']*100:>10.1f}")

avg_rev = sum(x["rev"] for x in M) / n
print(f"\n24 个月月均营业总收入 = {avg_rev/1e4:.1f} 万  （均摊停业损失口径：{avg_rev/1e4:.1f} 万/月）")
lo = min(season.items(), key=lambda kv: kv[1]["rev"])
hi = max(season.items(), key=lambda kv: kv[1]["rev"])
print(f"季节低谷 = {lo[0]}月 {lo[1]['rev']/1e4:.1f} 万（{lo[1]['adr']:.0f}元, OCC {lo[1]['occ']*100:.1f}%）")
print(f"季节高峰 = {hi[0]}月 {hi[1]['rev']/1e4:.1f} 万（{hi[1]['adr']:.0f}元, OCC {hi[1]['occ']*100:.1f}%）")
print(f"峰谷差 = {(hi[1]['rev']-lo[1]['rev'])/1e4:.1f} 万/月（{(hi[1]['rev']/lo[1]['rev']-1)*100:.0f}%）")

# 停业期损失：按起始月 + 停业月数
FIX = 284.0  # 万/月 固定成本
print("\n" + "=" * 108)
print("⭐ 停业期总损失精确测算（收入损失按真实历月曲线 + 固定成本 284 万/月）")
print("=" * 108)
print(f"{'起始月':<8}" + "".join(f"{x:>10}月" for x in range(12, 24)) + "   ← 停业月数下的停业期损失（万元）")
print("-" * 108)
for start in range(1, 13):
    row = []
    for dur in range(12, 24):
        loss = 0.0
        for k in range(dur):
            mo = ((start - 1 + k) % 12) + 1
            loss += season[mo]["rev"] / 1e4 + FIX
        row.append(loss)
    print(f"  {start:>2}月    " + "".join(f"{v:>11,.0f}" for v in row))

best = min(((s, d, sum(season[((s - 1 + k) % 12) + 1]["rev"] / 1e4 + FIX for k in range(d)))
            for s in range(1, 13) for d in range(12, 24)), key=lambda t: t[2])
worst = max(((s, d, sum(season[((s - 1 + k) % 12) + 1]["rev"] / 1e4 + FIX for k in range(d)))
             for s in range(1, 13) for d in range(12, 24)), key=lambda t: t[2])
print(f"\n最省：{best[0]}月开工、停业 {best[1]}月 → 停业期损失 {best[2]:,.0f} 万")
print(f"最贵：{worst[0]}月开工、停业 {worst[1]}月 → 停业期损失 {worst[2]:,.0f} 万")
print(f"⭐ 季节性造成的停业期成本差 = {worst[2]-best[2]:,.0f} 万（等效 {(worst[2]-best[2])/815:.1f} 个停业月）")

json.dump({"months": M, "season": {str(k): v for k, v in season.items()},
           "avg_rev": avg_rev, "fix_monthly": FIX},
          open(os.path.join(OUT, "seasonal_24m.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n输出:", os.path.join(OUT, "seasonal_24m.json"))
