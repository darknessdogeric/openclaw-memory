"""
Take Me to Chengdu — Lyric Poster
AI-generated chengdu night background + Pillow typeset lyrics
Output: 9:16 vertical, 1024×1792, 高清
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ========== 路径 ==========
BG_PATH = r"C:\Users\ericz\.openclaw\media\tool-image-generation\image-1---627ac1e7-2e5e-4fe6-a34c-b00f69f4857e.png"
OUT_PATH = r"D:\B166ER-OpenClaw\workspace\take_me_to_chengdu_lyric_poster.png"

# 目标画布 — 9:16 竖版高清 (1080×1920, 标准手机/朋友圈高清)
TARGET_W, TARGET_H = 1080, 1920

# ========== 字体 ==========
FONT_DIR = r"C:\Windows\Fonts"
F_TITLE_ITALIC = os.path.join(FONT_DIR, "georgiai.ttf")      # Georgia Italic — 标题
F_BODY_ITALIC = os.path.join(FONT_DIR, "georgiai.ttf")       # Georgia Italic — 歌词正文
F_LABEL = os.path.join(FONT_DIR, "georgiab.ttf")             # Georgia Bold — 章节标签
F_TITLE_BIG = os.path.join(FONT_DIR, "garamond-italic.ttf") if os.path.exists(os.path.join(FONT_DIR, "garamond-italic.ttf")) else os.path.join(FONT_DIR, "georgiai.ttf")

# ========== 打开背景 → upscale 到目标尺寸 ==========
bg_src = Image.open(BG_PATH).convert("RGBA")
src_w, src_h = bg_src.size
# 按目标 9:16 裁剪源图中心,然后放大到目标尺寸
target_ratio = TARGET_W / TARGET_H
src_ratio = src_w / src_h
if src_ratio > target_ratio:
    # 源图更宽 → 裁左右
    new_w = int(src_h * target_ratio)
    x0 = (src_w - new_w) // 2
    bg_crop = bg_src.crop((x0, 0, x0 + new_w, src_h))
else:
    # 源图更高 → 裁上下
    new_h = int(src_w / target_ratio)
    y0 = (src_h - new_h) // 2
    bg_crop = bg_src.crop((0, y0, src_w, y0 + new_h))
bg = bg_crop.resize((TARGET_W, TARGET_H), Image.LANCZOS)
W, H = bg.size
print(f"背景: {src_w}x{src_h} -> {W}x{H}")

# ========== 文字色彩（适配淡雅雨巷背景）============
# 柔和雨巷背景 => 文字偏深褐/墨绿/酒红
INK_GREEN = (38, 60, 50, 255)     # 墨绿 (主标题)
INK_BROWN = (78, 60, 45, 255)     # 深褐 (歌词)
DEEP_RED = (138, 52, 50, 255)     # 酒红 (Chorus 点缀)
SOFT_RED = (180, 90, 80, 255)     # 暗红柔 (标签)
IVORY = (245, 240, 230, 255)      # 象牙白 (装饰)
CREAM_SHADOW = (255, 250, 235, 200)  # 字阴影 — 暖白
SHADOW = (0, 0, 0, 90)

# 旧变量名别 (alias for 字符点)
GOLD = INK_GREEN
GOLD_SOFT = SOFT_RED

# ========== 创建画布 ==========
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# 顶部黑色渐变(让标题更清晰)
def add_vignette(img, top_alpha=90, bot_alpha=140):
    """顶部 + 底部黑色渐变"""
    w, h = img.size
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    # 顶部
    for y in range(int(h * 0.20)):
        a = int(top_alpha * (1 - y / (h * 0.20)))
        gd.line([(0, y), (w, y)], fill=(0, 0, 0, a))
    # 底部
    for y in range(int(h * 0.25)):
        a = int(bot_alpha * (y / (h * 0.25)))
        gd.line([(0, h - 1 - y), (w, h - 1 - y)], fill=(0, 0, 0, a))
    return Image.alpha_composite(img, grad)

# ========== 字体函数 ==========
def font(path, size):
    return ImageFont.truetype(path, size)

def text_w(draw, txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def center_x(draw, txt, fnt):
    w, _ = text_w(draw, txt, fnt)
    return (W - w) // 2

def shadowed_text(draw, x, y, txt, fnt, fill, shadow=SHADOW, offset=2):
    # 阴影
    draw.text((x + offset, y + offset), txt, font=fnt, fill=shadow)
    draw.text((x, y), txt, font=fnt, fill=fill)

# ========== 排版 ==========
margin_x = int(W * 0.08)        # 左右留白
center_y_top = int(H * 0.04)    # 顶部装饰区

# --- 顶部小标签 ---
lbl = font(F_LABEL, 24)
label_txt = "E R I C ' S   L Y R I C   P O S T E R"
lw, lh = text_w(draw, label_txt, lbl)
draw.text(((W - lw)//2, center_y_top), label_txt, font=lbl, fill=SOFT_RED)

# --- 主标题 (Take Me to Chengdu) ---
title_fnt = font(F_TITLE_BIG, 64)
title_txt = "Take Me to Chengdu"
tw, th = text_w(draw, title_txt, title_fnt)
tx = (W - tw) // 2
ty = center_y_top + 32
# 暖白柔光阴影 + 墨绿主文字
draw.text((tx + 2, ty + 2), title_txt, font=title_fnt, fill=CREAM_SHADOW)
draw.text((tx, ty), title_txt, font=title_fnt, fill=INK_GREEN)

# --- 副标题 ---
sub_fnt = font(F_LABEL, 20)
sub_txt = "— a song of returning —"
sw, sh = text_w(draw, sub_txt, sub_fnt)
draw.text(((W - sw)//2, ty + th + 10), sub_txt, font=sub_fnt, fill=INK_BROWN)

# 分隔线 — 酒红柔光
def divider(y, w_ratio=0.5):
    dw = int(W * w_ratio)
    x0 = (W - dw) // 2
    for i in range(2):
        a = 180 - i * 80
        draw.line([(x0, y + i), (x0 + dw, y + i)], fill=(138, 90, 80, a), width=1)
    draw.ellipse([(W//2 - 3, y - 3), (W//2 + 3, y + 3)], fill=DEEP_RED)

divider_y = ty + th + 38
divider(divider_y, 0.55)

# ========== 歌词段落 ==========
def section_label(y, txt):
    fnt = font(F_LABEL, 16)
    w, _ = text_w(draw, txt, fnt)
    x = (W - w) // 2
    # 轻声淸色
    draw.text((x, y), txt, font=fnt, fill=SOFT_RED)
    return y + 24

def lyric_line(y, txt, italic=True, size=28, color=INK_BROWN, center=True, line_spacing=1.32):
    """绘制歌词行,自动按宽度换行"""
    fnt = font(F_BODY_ITALIC, size) if italic else font(F_LABEL, size)
    max_w = W - margin_x * 2
    words = txt.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bw, _ = text_w(draw, test, fnt)
        if bw > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)

    line_h = int(size * line_spacing)
    for ln in lines:
        lw, lh = text_w(draw, ln, fnt)
        x = (W - lw) // 2 if center else margin_x
        # 暖白柔光阴影 — 适配淡雅背景
        draw.text((x + 1, y + 1), ln, font=fnt, fill=CREAM_SHADOW)
        draw.text((x, y), ln, font=fnt, fill=color)
        y += line_h
    return y

def chorus_block(y, lines, size=32, color=DEEP_RED):
    """副歌块 — 酒红点缀"""
    y = section_label(y, "C H O R U S")
    for ln in lines:
        y = lyric_line(y, ln, italic=True, size=size, color=color, center=True)
    return y + 4

# 当前 y
y = divider_y + 22

# VERSE 1
y = section_label(y, "V E R S E   1")
y = lyric_line(y, "The rain drapes this city in silver and dew,")
y = lyric_line(y, "Like veils on the hills that we once knew.")
y = lyric_line(y, "The scent of the jasmine still clings to my view,")
y = lyric_line(y, "Where the old winding alleys remember you.")
y += 6

# CHORUS 1
y = chorus_block(y, [
    "Take me to Chengdu,",
    "Take me to Chengdu,",
    "To the home that my heart holds true.",
])
y += 8

# 分隔
divider(y, 0.30)
y += 14

# VERSE 2
y = section_label(y, "V E R S E   2")
y = lyric_line(y, "The lanterns once glowed on the streets painted new,")
y = lyric_line(y, "With fireflies adrift in a river of blue.")
y = lyric_line(y, "You stand by the bridge when I close my view,")
y = lyric_line(y, "But the dream leaves me lost – and untrue.")
y += 6

# CHORUS 2
y = chorus_block(y, [
    "Take me to Chengdu,",
    "Take me to Chengdu,",
    "To the home that my heart holds true.",
])
y += 8

# 分隔
divider(y, 0.30)
y += 14

# BRIDGE
y = section_label(y, "B R I D G E")
y = lyric_line(y, "The night was a fire I kindled for you,")
y = lyric_line(y, "With embers that sparked and burned through.")
y = lyric_line(y, "Your fingers were cold, yet your eyes held the hue")
y = lyric_line(y, "Of the moon in a sky full of dew.")
y = lyric_line(y, "My voice was a whisper, my words were but few –")
y = lyric_line(y, "All the things I could never undo.")
y = lyric_line(y, "Your gaze was the mist of the morning's debut,")
y = lyric_line(y, "And mine was a blaze that grew.")
y += 6

# CHORUS 3
y = chorus_block(y, [
    "Take me to Chengdu,",
    "Take me to Chengdu,",
    "To the home that my heart holds true.",
])
y += 8

# 分隔
divider(y, 0.30)
y += 14

# VERSE 3
y = section_label(y, "V E R S E   3")
y = lyric_line(y, "The blood in my veins and the dust on these streets")
y = lyric_line(y, "Tell tales that no dying can subdue.")
y = lyric_line(y, "Their shadows ride tides where the amber light fleets,")
y = lyric_line(y, "And the waves that keep pulling me to you.")
y += 6

# FINAL CHORUS — 酒红加大
y = section_label(y, "F I N A L   C H O R U S")
y = lyric_line(y, "Take me to Chengdu,", size=34, color=DEEP_RED)
y = lyric_line(y, "Take me to Chengdu,", size=34, color=DEEP_RED)
y = lyric_line(y, "To the home that my heart holds true.", size=34, color=DEEP_RED)

# ========== 底部 ==========
# 留出底部 80px 安全区
foot_y = H - 60
# 分隔
divider(foot_y - 22, 0.40)
foot_fnt = font(F_LABEL, 16)
foot_txt = "ERIC & B166ER  ·  20 26  ·  雨 巷  ·  灯 火"
fw, fh = text_w(draw, foot_txt, foot_fnt)
draw.text(((W - fw)//2, foot_y), foot_txt, font=foot_fnt, fill=SOFT_RED)

# ========== 合成 ==========
# 淡雅背景不需重雾边, 只轻加顶部底部 20px 软边
def add_soft_vignette(img, top_alpha=40, bot_alpha=70):
    w, h = img.size
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(int(h * 0.10)):
        a = int(top_alpha * (1 - y / (h * 0.10)))
        gd.line([(0, y), (w, y)], fill=(0, 0, 0, a))
    for y in range(int(h * 0.12)):
        a = int(bot_alpha * (y / (h * 0.12)))
        gd.line([(0, h - 1 - y), (w, h - 1 - y)], fill=(0, 0, 0, a))
    return Image.alpha_composite(img, grad)

bg_with_vignette = add_soft_vignette(bg)
final = Image.alpha_composite(bg_with_vignette, overlay)

final.convert("RGB").save(OUT_PATH, quality=95, optimize=True)
sz = os.path.getsize(OUT_PATH) / 1024
print(f"SAVED: {OUT_PATH}  size={final.size}  kb={sz:.1f}")