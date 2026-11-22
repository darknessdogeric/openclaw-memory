# -*- coding: utf-8 -*-
"""房间分布表：按列归属楼层 → 分层房量与颜色构成 → 3改2 减房可行性测算"""
import io, os, sys, re, json
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xlrd

SRC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件"
P = os.path.join(SRC, r"1. 物业基础档案 工程部 2026. 11.2\② 客房总数与房型构成（标准间、大床房、套房、无障碍房）及各房型净面积 OK\房间分布表.xls")
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"

bk = xlrd.open_workbook(P, formatting_info=True)
sh = bk.sheet_by_index(0)
cmap = bk.colour_map


def cell_rgb(r, c):
    try:
        xf = bk.xf_list[sh.cell_xf_index(r, c)]
        bg = xf.background
        if bg is not None and bg.fill_pattern:
            ci = bg.pattern_colour_index
            if ci in cmap:
                rgb = cmap[ci]
                if rgb != (0, 0, 0):
                    return "#%02X%02X%02X" % rgb
    except Exception:
        pass
    return None


TAG = re.compile(r"(HU|障碍房|状态差|不见阳光|落地窗热|窗外有风机|味道臭|联通门|尾房|厨房|可变床|小套房|套房|大床|小床|办公室|噪音)")

# 找楼层表头行：同行内出现多个 "N楼"
hdr_r = None
col_floor = {}
for r in range(sh.nrows):
    cols = {}
    for c in range(sh.ncols):
        v = str(sh.cell_value(r, c)).strip()
        m = re.match(r"^(\d+)\s*楼", v)
        if m:
            cols[c] = int(m.group(1))
    if len(cols) >= 5:
        hdr_r = r
        col_floor = cols
        break

print(f"楼层表头行 = 第 {hdr_r+1} 行，列映射 {len(col_floor)} 列")
print("列→楼层:", {c: f for c, f in sorted(col_floor.items())})

LEG = {"#339966": "正常售卖", "#FF0000": "尽量不卖", "#C0C0C0": "有噪音",
       "#00CCFF": "状态差", "#0066CC": "深蓝(未定义)", "#FFFF00": "旁有工作间",
       "#FFFFFF": "无填充"}

per_floor = defaultdict(list)
for r in range(hdr_r + 1, sh.nrows):
    for c, fl in col_floor.items():
        v = str(sh.cell_value(r, c)).strip()
        if not v:
            continue
        if v.startswith("备注") or "绿色正常售卖" in v:
            continue
        room = v.split()[0]
        tags = TAG.findall(v)
        if not re.match(r"^\d{3,4}", room) and "办公室" not in v:
            continue
        per_floor[fl].append({"room": room, "raw": v, "fill": cell_rgb(r, c), "tags": tags})

print("\n" + "=" * 92)
print("分层房量与颜色构成（★ 绿色=正常售卖）")
print("=" * 92)
print(f"{'楼层':<6}{'名义房数':>9}{'★正常售卖':>11}{'尽量不卖':>9}{'有噪音':>8}{'状态差':>8}{'旁有工作间':>11}{'办公室/其他':>11}")
tot = Counter()
floor_rows = []
for fl in sorted(per_floor):
    items = per_floor[fl]
    cnt = Counter(i["fill"] for i in items)
    n_norm = cnt.get("#339966", 0)
    n_red = cnt.get("#FF0000", 0)
    n_gray = cnt.get("#C0C0C0", 0)
    n_blue = cnt.get("#00CCFF", 0)
    n_yel = cnt.get("#FFFF00", 0)
    other = len(items) - n_norm - n_red - n_gray - n_blue - n_yel
    floor_rows.append({"floor": fl, "total": len(items), "normal": n_norm, "red": n_red,
                       "gray": n_gray, "blue": n_blue, "yellow": n_yel, "other": other})
    for k, v in (("total", len(items)), ("normal", n_norm), ("red", n_red), ("gray", n_gray),
                 ("blue", n_blue), ("yellow", n_yel), ("other", other)):
        tot[k] += v
    print(f"{fl:<6}{len(items):>9}{n_norm:>11}{n_red:>9}{n_gray:>8}{n_blue:>8}{n_yel:>11}{other:>11}")
print("-" * 92)
print(f"{'合计':<6}{tot['total']:>9}{tot['normal']:>11}{tot['red']:>9}{tot['gray']:>8}"
      f"{tot['blue']:>8}{tot['yellow']:>11}{tot['other']:>11}")

print("\n=== 3 改 2 测算：名义 402 → 268 ===")
print(f"名义房数（表内）: {tot['total']}   ★正常售卖: {tot['normal']}   问题房(红+灰+蓝+深蓝): "
      f"{tot['red']+tot['gray']+tot['blue']+1}")
print(f"若 268 间全部为『正常售卖』口径 → 需从 {tot['normal']} 间正常房中减 {tot['normal']-268} 间")
print(f"若按名义口径 402→268 → 需减 134 间，而表内『问题房』仅 {tot['red']+tot['gray']+tot['blue']+1} 间")
print("→ ⭐ 两种口径的差额需工程部/财务部确认：是否含 25–26 层行政层与 27 层皇冠层（表内未覆盖）")

json.dump({"floor_rows": floor_rows, "totals": dict(tot),
           "header_row": hdr_r, "col_floor": {str(k): v for k, v in col_floor.items()}},
          open(os.path.join(OUT, "room_map_by_floor.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n输出:", os.path.join(OUT, "room_map_by_floor.json"))
