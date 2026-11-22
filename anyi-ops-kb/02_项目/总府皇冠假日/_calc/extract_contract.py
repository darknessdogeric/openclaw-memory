# -*- coding: utf-8 -*-
"""Extract text from the 49-page 管理合同延期协议及转让协议 PDF (check for text layer)."""
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIR = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\contract_text.txt"

cands = [f for f in glob.glob(os.path.join(DIR, "*.pdf")) if "总府实业" in f or "合同" in f or "延期" in f]
for c in cands:
    print("cand:", os.path.basename(c)[:110])
if not cands:
    print("NOT FOUND in", DIR)
    sys.exit(1)

pdf = cands[0]
txt = ""
try:
    import fitz
    d = fitz.open(pdf)
    print("pages:", d.page_count)
    parts = []
    for i, pg in enumerate(d):
        t = pg.get_text().strip()
        if t:
            parts.append(f"\n===== PAGE {i+1} =====\n{t}")
    txt = "".join(parts)
    # 统计有文本的页
    ntext = sum(1 for p in d if p.get_text().strip())
    print(f"pages with text layer: {ntext}/{d.page_count}")
    # 图像页
    nimg = sum(1 for p in d if p.get_images())
    print(f"pages with images: {nimg}")
except Exception as e:
    print("fitz failed:", type(e).__name__, e)

open(OUT, "w", encoding="utf-8").write(txt)
print("extracted chars:", len(txt), "->", OUT)
if len(txt) < 500:
    print("*** 无文本层 —— 系扫描件，需 OCR ***")
else:
    print(txt[:3000])
