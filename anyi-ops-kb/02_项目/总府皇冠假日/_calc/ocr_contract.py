# -*- coding: utf-8 -*-
"""OCR the 49-page scanned 管理合同 (no text layer). Renders at 260 DPI, tesseract chi_sim."""
import io, sys, os, glob, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIR = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\contract_ocr.txt"

pdf = [f for f in glob.glob(os.path.join(DIR, "*.pdf"))
       if "延期" in f or "转让协议" in f or "六洲" in f]
if not pdf:
    print("NOT FOUND"); sys.exit(1)
pdf = pdf[0]
print("target:", os.path.basename(pdf)[:90], flush=True)

try:
    import pytesseract
    from PIL import Image
    langs = pytesseract.get_languages(config="")
    print("tesseract langs:", langs, flush=True)
    if "chi_sim" not in langs:
        print("!!! chi_sim NOT installed -> OCR 不可用", flush=True)
        sys.exit(3)
except Exception as e:
    print("tesseract check failed:", type(e).__name__, e, flush=True)
    sys.exit(2)

import fitz
d = fitz.open(pdf)
out = []
t0 = time.time()
for i, pg in enumerate(d):
    pix = pg.get_pixmap(dpi=260)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    try:
        t = pytesseract.image_to_string(img, lang="chi_sim", config="--psm 6")
    except Exception as e:
        t = f"[OCR FAIL p{i+1}: {e}]"
    out.append(f"\n===== PAGE {i+1} =====\n{t}")
    print(f"  p{i+1}/{d.page_count}  {len(t)} chars  {time.time()-t0:.0f}s", flush=True)

open(OUT, "w", encoding="utf-8").write("".join(out))
print("DONE", os.path.getsize(OUT), "chars ->", OUT, flush=True)
