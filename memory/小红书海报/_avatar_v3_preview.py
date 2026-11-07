"""头像 v3 对照预览: 大图网格 + 40px + 圆形裁切 + 微信列表模拟"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\ericz\Desktop\微信头像_v3_2026-10-24"
PREV = r"D:\B166ER-openclaw\workspace\memory\小红书海报\头像预览"
os.makedirs(PREV, exist_ok=True)

SETS = [
    ("A_墨与朱印", ["dunhuang"]),
    ("B_定位十字", ["dunhuang", "indigo", "mint"]),
    ("C_双点弧线", ["dunhuang", "indigo", "mint"]),
    ("D_纯印极简", ["gold"]),
]
THEME_CN = {"dunhuang": "宣纸·墨·朱砂", "indigo": "米白·靛蓝·金", "mint": "淡青·松绿·金", "gold": "深墨·米白·金"}


def font(sz, bold=False):
    paths = ([r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc"]
              if bold else [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"])
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def load(name):
    p = os.path.join(OUT, name)
    return Image.open(p).convert("RGB") if os.path.exists(p) else None


def grid():
    CELL, PAD, LBL = 290, 24, 34
    rows = []
    for s, themes in SETS:
        rows.append((s, themes))
    W = PAD + 3 * (CELL + PAD)
    H = PAD + 70 + len(rows) * (CELL + LBL + PAD)
    g = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(g)
    d.text((PAD, 16), "微信头像 v3  —  4 方案对比", font=font(26, True), fill="#141414")
    d.text((PAD, 48), "设计规则: 中性色 70-90% / 单一强调色 / 留白优先 / 40px 可辨",
           font=font(14), fill="#888888")
    for ri, (s, themes) in enumerate(rows):
        y = PAD + 70 + ri * (CELL + LBL + PAD)
        d.text((PAD, y), s, font=font(18, True), fill="#222222")
        for ci, t in enumerate(themes):
            im = load(f"头像v3_{s}_{t}.png")
            if not im:
                continue
            im = im.resize((CELL, CELL), Image.LANCZOS)
            x = PAD + ci * (CELL + PAD)
            g.paste(im, (x, y + 26))
            d.text((x, y + 26 + CELL + 5), THEME_CN[t], font=font(13), fill="#666666")
    g.save(os.path.join(PREV, "v3_对照.png"), quality=95)
    return g.size


def small40():
    S = 40
    cells = []
    for s, themes in SETS:
        for t in themes:
            im = load(f"头像v3_{s}_{t}.png")
            if im:
                cells.append((f"{s.split('_')[0]}·{t}", im))
    W = 4 * (S + 46) + 40
    H = ((len(cells) + 3) // 4) * (S + 26) + 60
    g = Image.new("RGB", (W, H), "#EDEDED")
    d = ImageDraw.Draw(g)
    d.text((20, 14), "40px 实测 — 微信通讯录列表真实尺寸", font=font(15, True), fill="#555555")
    for i, (label, im) in enumerate(cells):
        x = 20 + (i % 4) * (S + 46)
        y = 44 + (i // 4) * (S + 26)
        g.paste(im.resize((S, S), Image.LANCZOS), (x, y))
        d.text((x + S + 4, y + 13), label, font=font(11), fill="#777777")
    g = g.resize((W * 2, H * 2), Image.LANCZOS)
    g.save(os.path.join(PREV, "v3_40px.png"), quality=95)
    return g.size


def circle():
    C = 190
    cells = []
    for s, themes in SETS:
        for t in themes:
            im = load(f"头像v3_{s}_{t}.png")
            if im:
                cells.append(im)
    cols = 4
    W = cols * (C + 34) + 34
    H = ((len(cells) + cols - 1) // cols) * (C + 34) + 34
    g = Image.new("RGB", (W, H), "#FFFFFF")
    for i, im in enumerate(cells):
        im = im.resize((C, C), Image.LANCZOS)
        mask = Image.new("L", (C, C), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, C - 1, C - 1), fill=255)
        x = 34 + (i % cols) * (C + 34)
        y = 34 + (i // cols) * (C + 34)
        g.paste(im, (x, y), mask)
    g.save(os.path.join(PREV, "v3_圆形裁切.png"), quality=95)
    return g.size


def wechat_mock():
    """模拟微信聊天列表: 圆头像 + 联系人名 + 最后消息"""
    rows = [("张实", "客人是冲目的地来的", "dunhuang", "A"),
            ("酒店选址理论", "跟着基建走、政策走、商业走", "indigo", "B"),
            ("AHL 匹配式", "从货架式到匹配式", "mint", "C"),
            ("B166ER", "看清大势 · 提前布局", "gold", "D")]
    W, H = 460, 96 * len(rows) + 30
    g = Image.new("RGB", (W, H), "#F7F7F7")
    d = ImageDraw.Draw(g)
    d.text((18, 8), "微信聊天列表模拟 (圆角头像 + 列表)", font=font(13), fill="#999999")
    for i, (name, msg, theme, tag) in enumerate(rows):
        y = 30 + i * 96
        d.rectangle([0, y, W, y + 95], fill="#FFFFFF")
        im = load(f"头像v3_{tag}_{'墨与朱印' if tag=='A' else ('定位十字' if tag=='B' else ('双点弧线' if tag=='C' else '纯印极简'))}_{theme}.png")
        if im:
            S = 64
            im = im.resize((S, S), Image.LANCZOS)
            mask = Image.new("L", (S, S), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, S - 1, S - 1), radius=10, fill=255)
            g.paste(im, (18, y + 16), mask)
        d.text((96, y + 22), name, font=font(17, True), fill="#111111")
        d.text((96, y + 50), msg, font=font(13), fill="#999999")
        d.text((W - 60, y + 22), "14:32", font=font(11), fill="#BBBBBB")
    g.save(os.path.join(PREV, "v3_微信列表模拟.png"), quality=95)
    return g.size


for fn in (grid, small40, circle, wechat_mock):
    try:
        print(fn.__name__, fn())
    except Exception as e:
        print(fn.__name__, "FAIL", e)
print("PREV:", PREV)
