"""拼 4x3 对照预览网格 + 小尺寸可读性测试 (40px 微信列表尺寸)"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\ericz\Desktop\微信头像_2026-10-24"
SCHEMES = ["S1_定位落点", "S2_实字", "S3_人流切口", "S4_三点汇聚"]
THEMES = ["indigo", "mint", "gold"]
THEME_CN = {"indigo": "靛蓝米白", "mint": "淡青松绿", "gold": "深底金"}

def font(sz):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()

# ── 1. 大图对照网格 ──
CELL, PAD, LBL = 300, 26, 40
W = PAD + 4 * (CELL + PAD)
H = PAD + 3 * (CELL + LBL + PAD) + 40
grid = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(grid)
d.text((PAD, 12), "微信头像 4 方案 × 3 配色", font=font(26), fill="#1A1A1A")

for ti, t in enumerate(THEMES):
    row_y = PAD + 40 + ti * (CELL + LBL + PAD)
    d.text((PAD, row_y - 4), THEME_CN[t], font=font(20), fill="#888888")
    for si, s in enumerate(SCHEMES):
        p = os.path.join(OUT, f"微信头像_{s}_{t}.png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB").resize((CELL, CELL), Image.LANCZOS)
        x = PAD + si * (CELL + PAD)
        y = row_y + 30
        grid.paste(im, (x, y))
        d.text((x, y + CELL + 6), s.split("_", 1)[1], font=font(19), fill="#333333")
grid.save(os.path.join(OUT, "_预览_4方案x3色.png"), quality=95)
print("preview grid:", grid.size)

# ── 2. 40px 微信列表可读性测试 ──
S = 40
small = Image.new("RGB", (4 * (S + 30) + 30, 3 * (S + 26) + 30), "#F2F2F2")
ds = ImageDraw.Draw(small)
ds.text((30, 8), "40px 实测 (微信通讯录列表尺寸)", font=font(15), fill="#666666")
for ti, t in enumerate(THEMES):
    for si, s in enumerate(SCHEMES):
        p = os.path.join(OUT, f"微信头像_{s}_{t}.png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB").resize((S, S), Image.LANCZOS)
        x = 30 + si * (S + 30)
        y = 34 + ti * (S + 26)
        small.paste(im, (x, y))
small = small.resize((small.width * 2, small.height * 2), Image.LANCZOS)
small.save(os.path.join(OUT, "_预览_40px实测.png"), quality=95)
print("40px test:", small.size)

# ── 3. 圆形裁切测试 ──
CIRC = 200
circ = Image.new("RGB", (4 * (CIRC + 40) + 40, 3 * (CIRC + 40) + 40), "#FFFFFF")
dc = ImageDraw.Draw(circ)
for ti, t in enumerate(THEMES):
    for si, s in enumerate(SCHEMES):
        p = os.path.join(OUT, f"微信头像_{s}_{t}.png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB").resize((CIRC, CIRC), Image.LANCZOS)
        mask = Image.new("L", (CIRC, CIRC), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, CIRC - 1, CIRC - 1), fill=255)
        x = 40 + si * (CIRC + 40)
        y = 40 + ti * (CIRC + 40)
        circ.paste(im, (x, y), mask)
circ.save(os.path.join(OUT, "_预览_圆形裁切.png"), quality=95)
print("circle test:", circ.size)
print("DONE")
