# -*- coding: utf-8 -*-
"""OCR the 49-page scanned 管理合同 via rapidocr_onnxruntime (local, zh support)."""
import io, sys, os, glob, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIR = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\contract_ocr.txt"

pdf = [f for f in glob.glob(os.path.join(DIR, "*.pdf"))
       if "延期" in f or "转让协议" in f or "六洲" in f]
if not pdf:
    print("NOT FOUND"); sys.exit(1)
pdf = pdf[0]
print("target:", os.path.basename(pdf)[:80], flush=True)

from rapidocr_onnxruntime import RapidOCR
import fitz
import numpy as np
from PIL import Image

engine = RapidOCR()
d = fitz.open(pdf)
print("pages:", d.page_count, flush=True)
out, t0 = [], time.time()
for i, pg in enumerate(d):
    pix = pg.get_pixmap(dpi=200)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    arr = np.array(img)
    try:
        res, _ = engine(arr)
        txt = "\n".join([r[1] for r in res]) if res else ""
    except Exception as e:
        txt = f"[FAIL {type(e).__name__}: {e}]"
    out.append(f"\n===== PAGE {i+1} =====\n{txt}")
    print(f"  p{i+1}/{d.page_count} chars={len(txt)} {time.time()-t0:.0f}s", flush=True)

open(OUT, "w", encoding="utf-8").write("".join(out))
print("DONE", os.path.getsize(OUT), "->", OUT, flush=True)
