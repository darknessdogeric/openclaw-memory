# -*- coding: utf-8 -*-
"""各层平面布置 JPG → OCR 提取各层客房数与功能（逐页独立子进程 + 断点续跑）"""
import io, os, sys, subprocess, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件\1. 物业基础档案 工程部 2026. 11.2\⑥ 各层平面布置（注明各层客房数与功能）\JPG版"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\floorplan_ocr"
os.makedirs(OUT, exist_ok=True)
WORK = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
PY = sys.executable

ONE = os.path.join(WORK, "ocr_floor_one.py")
open(ONE, "w", encoding="utf-8").write('''# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from rapidocr_onnxruntime import RapidOCR
p, out = sys.argv[1], sys.argv[2]
if os.path.exists(out) and os.path.getsize(out) > 20:
    print("SKIP"); sys.exit(0)
ocr = RapidOCR()
res, _ = ocr(p)
lines = []
if res:
    for box, txt, score in res:
        try:
            cx = sum(pt[0] for pt in box) / 4.0
            cy = sum(pt[1] for pt in box) / 4.0
            lines.append((round(cy), round(cx), txt))
        except Exception:
            lines.append((0, 0, txt))
lines.sort(key=lambda t: (t[0], t[1]))
with open(out, "w", encoding="utf-8") as f:
    for _, _, t in lines:
        f.write(str(t) + "\\n")
print("OK", len(lines))
''')

files = sorted(f for f in os.listdir(SRC) if f.lower().endswith((".jpg", ".jpeg")))
prog = os.path.join(OUT, "_progress.txt")
ok = 0
for i, fn in enumerate(files, 1):
    dst = os.path.join(OUT, fn.rsplit(".", 1)[0] + ".txt")
    src = os.path.join(SRC, fn)
    try:
        r = subprocess.run([PY, ONE, src, dst], capture_output=True, timeout=300)
        st = r.stdout.decode("utf-8", "replace").strip()
    except Exception as e:
        st = f"ERR {e}"
    ok += 1
    with open(prog, "a", encoding="utf-8") as f:
        f.write(f"[{i}/{len(files)}] {fn} -> {st}\n")
print(f"DONE {ok}/{len(files)}")
