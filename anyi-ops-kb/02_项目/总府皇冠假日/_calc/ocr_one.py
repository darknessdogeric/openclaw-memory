# -*- coding: utf-8 -*-
"""OCR one page of the scanned contract (isolated subprocess -> crash-proof)."""
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIR = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
OUTDIR = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\ocr_pages"
os.makedirs(OUTDIR, exist_ok=True)

pdfs = [f for f in glob.glob(os.path.join(DIR, "*.pdf"))
        if "延期" in f or "转让协议" in f or "六洲" in f]
if not pdfs:
    print("NOT FOUND"); sys.exit(1)
pdf = pdfs[0]

pno = int(sys.argv[1])
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 200

import fitz
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

d = fitz.open(pdf)
pg = d[d.page_count and (pno - 1)]
pix = pg.get_pixmap(dpi=dpi)
img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
arr = np.array(img)

engine = RapidOCR()
res, _ = engine(arr)
txt = "\n".join([r[1] for r in res]) if res else ""
out = os.path.join(OUTDIR, f"p{pno:02d}.txt")
open(out, "w", encoding="utf-8").write(txt)
print(f"P{pno} chars={len(txt)}")
