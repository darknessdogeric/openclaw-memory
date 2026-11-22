# -*- coding: utf-8 -*-
"""修正：房间分布表含两个楼层表头块（5-14F / 15-24F）→ 分层可售房量真值"""
import io, os, sys, re, json
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xlrd

P = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件\1. 物业基础档案 工程部 2026. 11.2\② 客房总数与房型构成（标准间、大床房、套房、无障碍房）及各房型净面积 OK\房间分布表.xls"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"

bk = xlrd.open_workbook(P, formatting_info=True)
sh = bk.sheet_by_index(0)
cmap = bk.colour_map


def fill(r, c):
    try:
        xf = bk.xf_list[sh.cell_xf_index(r, c)]
        bg = xf.background
        if bg is not None and bg.fill_pattern:
            ci = bg.pattern_colour_index
            if ci in cmap and cmap[ci] != (0, 0, 0):
                return "#%02X%02X%02X" % cmap[ci]
    except Exception:
        pass
    return None


TAG = re.compile(r"(HU|障碍房|状态差|不见阳光|落地窗热|窗外有风机|味道臭|联通门|尾房|厨房|可变床|小套房|套房|大床|小床|办公室|噪音)")

# 找所有楼层表头行
hdrs = []
for r in range(sh.nrows):
    cols = {}
    for c in range(sh.ncols):
        v = str(sh.cell_value(r, c)).strip()
        m = re.match(r"^(\d+)\s*楼", v)
        if m:
            cols[c] = int(m.group(1))
    if len(cols) >= 5:
        hdrs.append((r, cols))
print("楼层表头行:", [(r + 1, sorted(cols.values())) for r, cols in hdrs])

per = defaultdict(list)
for bi, (hr, cols) in enumerate(hdrs):
    end = hdrs[bi + 1][0] if bi + 1 < len(hdrs) else sh.nrows
    for r in range(hr + 1, end):
        for c, fl in cols.items():
            v = str(sh.cell_value(r, c)).strip()
            if not v or v.startswith("备注") or "绿色正常售卖" in v:
                continue
            room = v.split()[0]
            if not re.match(r"^\d{3,4}", room) and "办公室" not in v:
                continue
            per[fl].append({"room": room, "raw": v, "fill": fill(r, c), "tags": TAG.findall(v)})

print("\n" + "=" * 86)
print("分层房量与颜色构成  ★绿=正常售卖  红=尽量不卖  灰=有噪音  蓝=状态差  黄=旁有工作间")
print("=" * 86)
print(f"{'楼层':<6}{'名义':>6}{'★正常售卖':>10}{'尽量不卖':>9}{'有噪音':>8}{'状态差':>8}{'旁有工作间':>11}{'其他':>6}")
tot = Counter()
rows = []
for fl in sorted(per):
    it = per[fl]
    c = Counter(i["fill"] for i in it)
    n = len(it)
    ng, nr, ns, nb, ny = c.get("#339966", 0), c.get("#FF0000", 0), c.get("#C0C0C0", 0), c.get("#00CCFF", 0), c.get("#FFFF00", 0)
    no = n - ng - nr - ns - nb - ny
    rows.append({"floor": fl, "total": n, "normal": ng, "red": nr, "gray": ns, "blue": nb, "yellow": ny, "other": no})
    for k, v in (("total", n), ("normal", ng), ("red", nr), ("gray", ns), ("blue", nb), ("yellow", ny), ("other", no)):
        tot[k] += v
    print(f"{fl:<6}{n:>6}{ng:>10}{nr:>9}{ns:>8}{nb:>8}{ny:>11}{no:>6}")
print("-" * 86)
print(f"{'合计':<6}{tot['total']:>6}{tot['normal']:>10}{tot['red']:>9}{tot['gray']:>8}{tot['blue']:>8}{tot['yellow']:>11}{tot['other']:>6}")

print("\n=== 与工程部《楼层房间数量表》交叉核对 ===")
official = {5: 18, 6: 10, 7: 20, 8: 23, 9: 23, 10: 23, 11: 23, 12: 23, 13: 23, 14: 23, 15: 23, 16: 23,
            17: 23, 18: 23, 19: 23, 20: 21, 21: 19, 22: 21, 23: 17, 24: 13}
off_tot = sum(official.values())
print(f"工程部官方合计: {off_tot} 间（中区 255 + 高区 160）；分布表实测: {tot['total']} 间")
diff = [(r["floor"], r["total"], official.get(r["floor"])) for r in rows if r["total"] != official.get(r["floor"])]
if diff:
    print("差异层:", diff)
else:
    print("⭐ 各层完全一致")

print("\n=== 3 改 2（402→268 / 415→268）测算 ===")
print(f"名义房数 {tot['total']}  ★正常售卖 {tot['normal']}  问题房(红+灰+蓝) {tot['red']+tot['gray']+tot['blue']}")
print(f"口径A（名义 415→268）: 需减 {tot['total']-268} 间，其中问题房仅 {tot['red']+tot['gray']+tot['blue']} 间 → 另需减 {tot['total']-268-(tot['red']+tot['gray']+tot['blue'])} 间正常房")
print(f"口径B（正常售卖 351→268）: 需减 {tot['normal']-268} 间")
print("→ ⭐ 两口径差额须工程部/财务部确认（是否含 25–26F 行政层、27F 皇冠层；表内仅覆盖 5–24F）")

json.dump({"floor_rows": rows, "totals": dict(tot), "official": official},
          open(os.path.join(OUT, "room_map_by_floor.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n输出 room_map_by_floor.json")
