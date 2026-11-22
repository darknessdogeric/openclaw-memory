# -*- coding: utf-8 -*-
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
        f.write(str(t) + "\n")
print("OK", len(lines))
