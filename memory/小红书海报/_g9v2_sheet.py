import os, sys, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image, ImageDraw

D = r"C:\Users\ericz\Desktop\小红书_酒店分级分类_9图v2_2026-10-31"
PREV = r"D:\B166ER-openclaw\workspace\memory\小红书海报\头像预览"
os.makedirs(PREV, exist_ok=True)

files = sorted(f for f in os.listdir(D) if f.endswith(".png"))
CW, PAD, LBL = 336, 14, 24
cols = 3
rows = (len(files) + cols - 1) // cols
thumbs = []
for f in files:
    im = Image.open(os.path.join(D, f)).convert("RGB")
    h = int(im.size[1] * CW / im.size[0])
    thumbs.append((f, im.resize((CW, h), Image.LANCZOS)))
rowh = [max(t[1].size[1] for t in thumbs[r*cols:(r+1)*cols]) for r in range(rows)]
W = cols*CW + (cols+1)*PAD
H = sum(rowh) + rows*(LBL+PAD) + PAD
sheet = Image.new("RGB", (W, H), "#e8e4da")
d = ImageDraw.Draw(sheet)
y = PAD
for r in range(rows):
    x = PAD
    for name, t in thumbs[r*cols:(r+1)*cols]:
        d.text((x+2, y), name, fill="#6b6259")
        sheet.paste(t, (x, y+LBL))
        x += CW + PAD
    y += rowh[r] + LBL + PAD
out = os.path.join(PREV, "_g9v2_sheet.png")
sheet.save(out)
print("sheet:", sheet.size, os.path.getsize(out), "bytes")

# 源文件同步到桌面
src = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
for f in ("_g9_lib.py", "_g9_data.py", "_g9_page.py", "_g9_main.py"):
    shutil.copy(os.path.join(src, f), os.path.join(D, f))
print("sources copied")
print("files:", len(os.listdir(D)))