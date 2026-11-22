# -*- coding: utf-8 -*-
"""房间分布表：提取每格的底色/字色 + 房态标签 → 还原可售房量与逐层排布底数"""
import io, os, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xlrd

P = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件\1. 物业基础档案 工程部 2026. 11.2\② 客房总数与房型构成（标准间、大床房、套房、无障碍房）及各房型净面积 OK\房间分布表.xls"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"

bk = xlrd.open_workbook(P, formatting_info=True)
sh = bk.sheet_by_index(0)
cmap = bk.colour_map
print(f"sheet: {sh.name}  {sh.nrows}x{sh.ncols}")

# xf -> (fill_rgb, font_rgb)
def xf_colors(xf_idx):
    try:
        xf = bk.xf_list[xf_idx]
        fill = None; font = None
        try:
            bg = xf.background
            if bg is not None and bg.fill_pattern:
                ci = bg.pattern_colour_index
                if ci in cmap:
                    rgb = cmap[ci]
                    if rgb != (0, 0, 0):
                        fill = rgb
        except Exception:
            pass
        try:
            fi = xf.font_index
            if fi is not None and fi < len(bk.font_list):
                f = bk.font_list[fi]
                ci = f.colour_index
                if ci in cmap:
                    rgb = cmap[ci]
                    if rgb != (0, 0, 0):
                        font = rgb
        except Exception:
            pass
        return fill, font
    except Exception:
        return None, None

def name_rgb(rgb):
    if rgb is None:
        return "-"
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"

TAG = re.compile(r"(HU|障碍房|状态差|不见阳光|落地窗热|窗外有风机|味道臭|联通门|尾房|厨房|可变床|小套房|套房|大床|小床|办公室|噪音)")

rows = []
for r in range(sh.nrows):
    for c in range(sh.ncols):
        v = sh.cell_value(r, c)
        if not isinstance(v, str):
            v = str(v).strip()
        if not v:
            continue
        fill, font = xf_colors(sh.cell_xf_index(r, c))
        room = v.split()[0] if v.split() else v
        tags = TAG.findall(v)
        rows.append({"r": r, "c": c, "raw": v, "room": room,
                     "fill": name_rgb(fill), "font": name_rgb(font), "tags": tags})

# 统计每种底色
from collections import Counter
fills = Counter(x["fill"] for x in rows)
print("\n=== 底色分布 ===")
for k, n in fills.most_common():
    print(f"  {k}: {n}")

# 每格：房号 + 标签 + 颜色
with open(os.path.join(OUT, "room_map_colored.txt"), "w", encoding="utf-8") as f:
    f.write("# 房间分布表 · 单元格颜色版\n")
    for x in rows:
        f.write(f"{x['raw']:<34} fill={x['fill']}  font={x['font']}  tags={'/'.join(x['tags'])}\n")

# 分层：表头行识别楼层
floors = {}
cur = None
for r in range(sh.nrows):
    vals = [str(sh.cell_value(r, c)).strip() for c in range(sh.ncols)]
    joined = " ".join(v for v in vals if v)
    m = re.search(r"(\d+)\s*楼", joined)
    if m and ("平面" not in joined) and len(joined) < 20:
        cur = m.group(1) + "楼"
        floors.setdefault(cur, [])
        continue
    if cur:
        for c, v in enumerate(vals):
            if v:
                fill, font = xf_colors(sh.cell_xf_index(r, c))
                tags = TAG.findall(v)
                floors[cur].append({"room": v.split()[0], "raw": v, "fill": name_rgb(fill),
                                     "font": name_rgb(font), "tags": tags})

print("\n=== 分层房量 ===")
total = 0
for k in sorted(floors, key=lambda x: int(re.sub(r"\D", "", x) or 0)):
    n = len(floors[k])
    total += n
    print(f"  {k}: {n} 间")
print(f"  合计（表内）: {total}")

# 状态标签统计
print("\n=== 房态标签统计（表内全部）===")
tc = Counter()
for x in rows:
    for t in x["tags"]:
        tc[t] += 1
for k, n in tc.most_common():
    print(f"  {k}: {n}")

json.dump({"rows": rows, "floors": floors},
          open(os.path.join(OUT, "room_map_colored.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n输出:", os.path.join(OUT, "room_map_colored.txt"))
