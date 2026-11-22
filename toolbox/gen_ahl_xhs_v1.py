#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHL · 小红书范式多图 (12 张)
3:4 竖屏 · 1080×1440 · 深空科技风 (与 AHL v2-v6 信息图视觉统一)
主题：从「酒店业的 AI 革命」讲透 AHL 是什么、为什么、怎么做、怎么赚钱
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 输出
OUT_DIR = r"C:\Users\ericz\Desktop\产业发展部\AHL项目\AHL_小红书12图"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1440
MARGIN = 60

# 配色（与 AHL 信息图系列完全一致）
BG_TOP = (10, 26, 58)        # 深空蓝
BG_BOT = (2, 6, 15)         # 接近黑
CARD_BG = (20, 30, 60)      # 卡片底色
CARD_BG2 = (30, 40, 80)     # 卡片高光
CYAN = (0, 212, 255)
GOLD = (255, 215, 0)
PURPLE = (139, 92, 246)
GREEN = (74, 222, 128)
WHITE = (255, 255, 255)
LIGHT_GRAY = (180, 200, 230)
DIM = (100, 120, 160)
LINE = (60, 80, 130)
RED = (255, 80, 100)
ORANGE = (255, 160, 60)

# 字体（emoji 用彩色 emoji 字体避免 seguiemj 缺字）
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_SYM = r"C:\Windows\Fonts\seguiemj.ttf"
FONT_HEAVY = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
FONT_EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"

# 符号替代 (无 emoji 也能表达)
SYMBOLS = {
    'fire': 'HOT',
    'hook': '>>>',
    'arrow_down': '▼',
    'arrow_up': '▲',
    'arrow_right': '▶',
    'star': '★',
    'check': '✓',
    'cross': '✕',
    'no': '⊘',
    'plus': '+',
    'lightning': '⚡',
    'gem': '◆',
    'money': '¥',
}

# 字号
SZ_TITLE = 110
SZ_SUB = 56
SZ_HEADING = 60
SZ_BODY = 38
SZ_TAG = 28
SZ_NUM_BIG = 220
SZ_NUM = 120
SZ_NUM_MED = 80
SZ_SMALL = 26
SZ_FOOTER = 24
SZ_HUGE = 280

def f(p, s):
    return ImageFont.truetype(p, s)

# ─────────────────────────────────
# 工具函数
# ─────────────────────────────────
def new_canvas():
    img = Image.new('RGB', (W, H), BG_BOT)
    return img

def vertical_gradient_bg(img, c1=BG_TOP, c2=BG_BOT):
    """垂直渐变背景"""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def add_stars(draw, density=80):
    """星云背景星点 — 调用前确保传入的是 draw 不是 img"""
    import random
    random.seed(42)
    for _ in range(density):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.choice([1, 1, 1, 2, 2, 3])
        c = random.choice([WHITE, CYAN, (180, 210, 255), (200, 200, 255), GOLD])
        draw.ellipse([x, y, x+s, y+s], fill=c)

def add_glow_border(draw, color=GOLD, alpha=50, r=24):
    """发光边框"""
    # 多层叠加做光晕
    for offset in range(4, 0, -1):
        draw.rounded_rectangle(
            [MARGIN - offset, MARGIN - offset,
             W - MARGIN + offset, H - MARGIN + offset],
            r + offset, outline=(*color, max(15, alpha // offset)), width=1
        )

def page_header(draw, page_no, total, label):
    """页头：编号 + 标签"""
    # 顶部品牌条
    draw.rectangle([0, 0, W, 8], fill=CYAN)
    # 编号圆
    draw.ellipse([MARGIN, MARGIN, MARGIN + 60, MARGIN + 60], outline=GOLD, width=3)
    draw.text((MARGIN + 30, MARGIN + 8), str(page_no),
              font=f(FONT_BOLD, 32), fill=GOLD, anchor='mt')
    # 标签
    bb = draw.textbbox((0, 0), label, font=f(FONT_BOLD, SZ_TAG + 2))
    tw = bb[2] - bb[0]
    draw.text((W - MARGIN, MARGIN + 14), label,
              font=f(FONT_BOLD, SZ_TAG), fill=CYAN, anchor='rt')

def page_footer(draw, page_no, total, brand="ERIC的B166ER 出品 · AHL"):
    """页脚"""
    draw.line([(MARGIN, H - 90), (W - MARGIN, H - 90)], fill=LINE, width=2)
    draw.text((MARGIN, H - 60), brand, font=f(FONT_BOLD, SZ_FOOTER), fill=LIGHT_GRAY)
    pt = f"{page_no:02d} / {total:02d}"
    draw.text((W - MARGIN, H - 60), pt, font=f(FONT_BOLD, SZ_FOOTER + 2),
              fill=GOLD, anchor='rt')

def card(draw, x, y, w, h, bg=CARD_BG, border=None, r=18, alpha=None):
    if alpha:
        # 半透明卡片（先做一层背景）
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.rounded_rectangle([x, y, x+w, y+h], r, fill=(*bg, alpha))
        # 暂不处理 alpha 复杂合成，保持不透明即可
        draw.rounded_rectangle([x, y, x+w, y+h], r, fill=bg)
    else:
        draw.rounded_rectangle([x, y, x+w, y+h], r, fill=bg)
    if border:
        draw.rounded_rectangle([x, y, x+w, y+h], r, outline=border, width=2)

def glow_circle(draw, cx, cy, r, color):
    """发光圆"""
    for off in range(8, 0, -1):
        draw.ellipse([cx - r - off, cy - r - off, cx + r + off, cy + r + off],
                     outline=color, width=1)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)

def center_text(draw, text, y, font, fill, x_center=W // 2):
    draw.text((x_center, y), text, font=font, fill=fill, anchor='mt')

# ─────────────────────────────────
# 12 张图的内容
# ─────────────────────────────────
TOTAL = 12

def page_01_hook():
    """第 1 页：封面 / 钩子"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 120)

    # 顶部红色"HOOK"标签
    bb = draw.textbbox((0, 0), "▶ 一 条 视 频 讲 透", font=f(FONT_BOLD, SZ_TAG + 4))
    tw = bb[2] - bb[0]
    x = (W - tw - 40) // 2
    draw.rounded_rectangle([x, 120, x + tw + 40, 175], 28, fill=RED)
    draw.text((x + 20, 132), "▶ 一 条 视 频 讲 透", font=f(FONT_BOLD, SZ_TAG + 4), fill=WHITE)

    # 主标题
    center_text(draw, "酒店业的", 230, f(FONT_BOLD, 90), LIGHT_GRAY)
    # 巨型标题
    center_text(draw, "AI 革命", 320, f(FONT_HEAVY, SZ_HUGE), GOLD)

    # 副标题
    center_text(draw, "AHL · 同构双矩阵范式", 620, f(FONT_BOLD, SZ_SUB), CYAN)
    center_text(draw, "小到单店 · 大到文旅 · 同一种解法", 700, f(FONT_REG, SZ_BODY), LIGHT_GRAY)

    # 底部圆形三图标
    icons_y = 950
    cx = [240, 540, 840]
    labels = ["酒 店", "集 团", "文 旅"]
    icons_text = ["H", "G", "C"]  # H=Hotel G=Group C=Culture
    colors = [CYAN, PURPLE, GOLD]
    for i in range(3):
        glow_circle(draw, cx[i], icons_y, 80, colors[i])
        draw.ellipse([cx[i]-65, icons_y-65, cx[i]+65, icons_y+65], fill=CARD_BG2, outline=colors[i], width=3)
        draw.text((cx[i], icons_y), icons_text[i], font=f(FONT_HEAVY, 80), fill=colors[i], anchor='mm')
        draw.text((cx[i], icons_y + 120), labels[i], font=f(FONT_BOLD, SZ_BODY), fill=WHITE, anchor='mt')

    # 底部标识
    center_text(draw, "▼  往下滑", 1200, f(FONT_BOLD, SZ_SMALL + 6), GOLD)

    page_footer(draw, 1, TOTAL, "ERIC的B166ER 出品 · AHL系列")
    return img

def page_02_pain():
    """第 2 页：行业痛点 / 反差钩子"""
    img = new_canvas()
    vertical_gradient_bg(img, (40, 10, 10), (5, 2, 5))
    draw = ImageDraw.Draw(img)
    add_stars(draw, 60)

    page_header(draw, 2, TOTAL, "痛 点 · PAIN")

    center_text(draw, "酒店行业", 220, f(FONT_BOLD, SZ_TITLE), LIGHT_GRAY)
    center_text(draw, "卡在哪里？", 350, f(FONT_BOLD, SZ_TITLE), RED)

    # 4 大痛点卡片
    pains = [
        ("[ 头部集团 ]", "重资产·规模大·", "但效率低·创新慢"),
        ("[ 单体酒店 ]", "缺流量·缺数据·", "缺 AI 能力"),
        ("[ AI 浪潮 ]", "DeepSeek/豆包/", "帮不了酒店本身"),
        ("[ 抽水经济 ]", "OTA 抽佣 15-25%", "价值都被中介拿走"),
    ]
    cy = 580
    for i, (title, l1, l2) in enumerate(pains):
        y = cy + i * 175
        card(draw, MARGIN, y, W - 2 * MARGIN, 150, bg=CARD_BG, border=RED)
        draw.text((MARGIN + 30, y + 18), title, font=f(FONT_BOLD, SZ_HEADING), fill=RED)
        draw.text((MARGIN + 30, y + 80), l1, font=f(FONT_REG, SZ_BODY - 4), fill=LIGHT_GRAY)
        draw.text((MARGIN + 30, y + 116), l2, font=f(FONT_REG, SZ_BODY - 4), fill=GOLD)

    page_footer(draw, 2, TOTAL)
    return img

def page_03_question():
    """第 3 页：核心问题"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 3, TOTAL, "问 题 · QUESTION")

    center_text(draw, "酒店需要怎样的", 250, f(FONT_BOLD, 80), LIGHT_GRAY)
    center_text(draw, "AI 能力？", 360, f(FONT_HEAVY, SZ_TITLE), GOLD)

    # 三个失败方案
    fails = [
        ("✕", "做一个酒店 App", "消费者不会装"),
        ("✕", "做一个酒店 SaaS", "酒店用不起 / 不会用"),
        ("✕", "做一个 AI 入口", "豆包 / 飞猪帮帮已有"),
    ]
    cx = W // 2
    cy = 620
    for i, (mark, t, sub) in enumerate(fails):
        y = cy + i * 130
        draw.line([(MARGIN + 20, y + 30), (MARGIN + 60, y + 30)], fill=RED, width=4)
        draw.text((MARGIN + 80, y), mark, font=f(FONT_SYM, 56), fill=RED)
        draw.text((MARGIN + 160, y + 10), t, font=f(FONT_BOLD, SZ_HEADING - 4), fill=WHITE)
        draw.text((MARGIN + 160, y + 65), sub, font=f(FONT_REG, SZ_BODY - 6), fill=DIM)

    # 终极问题
    center_text(draw, "∴ 真正的答案是？", 1060, f(FONT_BOLD, SZ_HEADING + 4), GOLD)
    center_text(draw, "▼  往下看", 1170, f(FONT_REG, SZ_BODY), CYAN)

    page_footer(draw, 3, TOTAL)
    return img

def page_04_answer():
    """第 4 页：核心答案 - 双 AGENT 矩阵"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 80)

    page_header(draw, 4, TOTAL, "答 案 · ANSWER")

    center_text(draw, "双 AGENT 矩阵", 180, f(FONT_BOLD, SZ_TITLE), CYAN)
    center_text(draw, "DUAL-MATRIX", 300, f(FONT_BOLD, 36), DIM)

    # 上下两个矩阵
    top_y = 420
    bot_y = 850

    # C 矩阵 (顶部)
    card(draw, MARGIN, top_y, W - 2 * MARGIN, 360, bg=(0, 60, 90), border=CYAN)
    draw.text((MARGIN + 30, top_y + 24), "C 矩阵 · 客人侧", font=f(FONT_BOLD, SZ_HEADING), fill=CYAN)
    draw.text((MARGIN + 30, top_y + 90), "商 务 客 / 背 包 客 / 亲 子 客", font=f(FONT_BOLD, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, top_y + 140), "入 境 客 / 宠 物 客 / 亚 文 化", font=f(FONT_BOLD, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, top_y + 220), "× N 个 客 人 Agent", font=f(FONT_BOLD, SZ_BODY + 4), fill=WHITE)
    draw.text((MARGIN + 30, top_y + 270), "需求侧 · 数字员工代理每位客人", font=f(FONT_REG, SZ_BODY - 6), fill=DIM)

    # 中间协议层
    card(draw, MARGIN, top_y + 380, W - 2 * MARGIN, 60, bg=PURPLE, border=GOLD)
    draw.text((W // 2, top_y + 410), "★  AHL 协议层  ·  标准化握手  ·  不抽水  ★",
              font=f(FONT_BOLD, SZ_BODY + 4), fill=WHITE, anchor='mm')

    # B 矩阵 (底部)
    card(draw, MARGIN, bot_y, W - 2 * MARGIN, 360, bg=(80, 60, 0), border=GOLD)
    draw.text((MARGIN + 30, bot_y + 24), "B 矩阵 · 商家侧", font=f(FONT_BOLD, SZ_HEADING), fill=GOLD)
    draw.text((MARGIN + 30, bot_y + 90), "酒 店 / 餐 饮 / 零 售 / 娱 乐", font=f(FONT_BOLD, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, bot_y + 140), "服 务 / 交 通 / 景 区 / ...", font=f(FONT_BOLD, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, bot_y + 220), "× N 个 商 家 Agent", font=f(FONT_BOLD, SZ_BODY + 4), fill=WHITE)
    draw.text((MARGIN + 30, bot_y + 270), "供给侧 · 数字员工武装每个商家", font=f(FONT_REG, SZ_BODY - 6), fill=DIM)

    page_footer(draw, 4, TOTAL)
    return img

def page_05_p2p():
    """第 5 页：不是 Hub，是 P2P"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 5, TOTAL, "架 构 · ARCHITECTURE")

    center_text(draw, "❌ 不是中央 Hub", 180, f(FONT_BOLD, 72), RED)
    center_text(draw, "✅ 而是 P2P 直接握手", 270, f(FONT_BOLD, 72), GREEN)

    # P2P mesh 可视化
    cx_l = 200
    cx_r = 880
    cy_top = 480
    cy_bot = 1020
    gap = 70

    # 6 个 C 节点
    draw.text((cx_l, cy_top - 100), "C 矩阵", font=f(FONT_BOLD, 32), fill=CYAN, anchor='mm')
    for i in range(6):
        y = cy_top + i * (cy_bot - cy_top) // 5
        # C 节点
        x_c = cx_l + (i % 2) * 80
        glow_circle(draw, x_c, y, 20, CYAN)
        draw.ellipse([x_c - 18, y - 18, x_c + 18, y + 18], fill=CYAN)
        # B 节点
        x_b = cx_r - (i % 2) * 80
        glow_circle(draw, x_b, y, 20, GOLD)
        draw.ellipse([x_b - 18, y - 18, x_b + 18, y + 18], fill=GOLD)
        # P2P 连线
        for j in range(6):
            yj = cy_top + j * (cy_bot - cy_top) // 5
            x_bj = cx_r - (j % 2) * 80
            if (i + j) % 2 == 0:
                draw.line([(x_c, y), (x_bj, yj)], fill=PURPLE, width=1)

    draw.text((cx_r, cy_top - 100), "B 矩阵", font=f(FONT_BOLD, 32), fill=GOLD, anchor='mm')

    # 中间空
    center_text(draw, "✕", 750, f(FONT_HEAVY, 120), GREEN)
    center_text(draw, "NO MIDDLEMAN", 850, f(FONT_BOLD, 32), GREEN)

    page_footer(draw, 5, TOTAL)
    return img

def page_06_paradigm():
    """第 6 页：范式四阶"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 6, TOTAL, "范 式 · PARADIGM")

    center_text(draw, "范式四阶", 200, f(FONT_BOLD, SZ_TITLE), LIGHT_GRAY)
    center_text(draw, "价值锚一路迁移", 290, f(FONT_REG, SZ_BODY + 6), DIM)

    # 4 阶
    steps = [
        ("1", "[ 货 架 经 济 ]", "价值锚：位置", "抽水者：房东", (130, 140, 160)),
        ("2", "[ 匹 配 经 济 ]", "价值锚：算法", "抽水者：OTA", (0, 200, 230)),
        ("3", "[ 直 接 经 济 ]", "价值锚：协议", "抽水者：无", (180, 180, 100)),
        ("4", "[ TOKEN 经 济 ]", "价值锚：算力", "AHL 在此", (255, 215, 0)),
    ]
    cy = 460
    for i, (n, t, v1, v2, c) in enumerate(steps):
        y = cy + i * 200
        is_last = (i == 3)
        bg = (40, 40, 20) if is_last else CARD_BG
        border = GOLD if is_last else c
        card(draw, MARGIN, y, W - 2 * MARGIN, 170, bg=bg, border=border)
        # 编号
        draw.ellipse([MARGIN + 20, y + 30, MARGIN + 120, y + 130], fill=(*c, 30) if is_last else c)
        draw.text((MARGIN + 70, y + 80), n, font=f(FONT_HEAVY, 60), fill=WHITE, anchor='mm')
        # 标题
        draw.text((MARGIN + 150, y + 25), t, font=f(FONT_BOLD, SZ_HEADING), fill=c)
        draw.text((MARGIN + 150, y + 95), v1, font=f(FONT_BOLD, SZ_BODY - 4), fill=LIGHT_GRAY)
        draw.text((MARGIN + 150, y + 130), v2, font=f(FONT_BOLD, SZ_BODY - 4), fill=GOLD if is_last else DIM)

    page_footer(draw, 6, TOTAL)
    return img

def page_07_token():
    """第 7 页：TOKEN = 算力电费"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 7, TOTAL, "血 脉 · TOKEN")

    center_text(draw, "TOKEN 是", 180, f(FONT_BOLD, 80), LIGHT_GRAY)
    center_text(draw, "Agent 时代的电费", 280, f(FONT_HEAVY, SZ_TITLE), GREEN)

    # 对照表
    cy = 500
    card(draw, MARGIN, cy, W - 2 * MARGIN, 600, bg=CARD_BG)

    # 左 - 工业时代
    draw.text((MARGIN + 30, cy + 20), "[ 工 业 时 代 ]", font=f(FONT_BOLD, SZ_HEADING), fill=(120, 130, 150))
    draw.text((MARGIN + 30, cy + 100), "成本单位 · 电费（度）", font=f(FONT_REG, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, cy + 145), "基础设施 · 电网", font=f(FONT_REG, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, cy + 190), "计量工具 · 电表", font=f(FONT_REG, SZ_BODY), fill=LIGHT_GRAY)
    draw.text((MARGIN + 30, cy + 235), "支撑循环 · 工业经济", font=f(FONT_REG, SZ_BODY), fill=LIGHT_GRAY)

    # 分隔
    draw.line([(W // 2, cy + 40), (W // 2, cy + 540)], fill=GOLD, width=2)
    center_text(draw, "≈", cy + 280, f(FONT_HEAVY, 120), GOLD)

    # 右 - AI 时代
    draw.text((MARGIN + 30, cy + 320), "[ AI  时  代 ]", font=f(FONT_BOLD, SZ_HEADING), fill=GREEN)
    draw.text((MARGIN + 30, cy + 400), "成本单位 · TOKEN（算力）", font=f(FONT_BOLD, SZ_BODY), fill=GREEN)
    draw.text((MARGIN + 30, cy + 445), "基础设施 · AHL 协议层", font=f(FONT_BOLD, SZ_BODY), fill=GREEN)
    draw.text((MARGIN + 30, cy + 490), "计量工具 · 握手计量器", font=f(FONT_BOLD, SZ_BODY), fill=GREEN)
    draw.text((MARGIN + 30, cy + 535), "支撑循环 · Agent 经济", font=f(FONT_BOLD, SZ_BODY), fill=GREEN)

    center_text(draw, "1 次握手 = X TOKEN · 1 TOKEN = 算力", 1180, f(FONT_BOLD, SZ_BODY + 2), GOLD)

    page_footer(draw, 7, TOTAL)
    return img

def page_08_fractal():
    """第 8 页：同构分形三层"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 8, TOTAL, "同 构 · FRACTAL")

    center_text(draw, "同构分形架构", 180, f(FONT_BOLD, SZ_TITLE), CYAN)
    center_text(draw, "三层 · 同一架构 · 各自完备", 290, f(FONT_REG, SZ_BODY + 4), LIGHT_GRAY)

    # 三层卡
    tiers = [
        ("H", "单店", "SINGLE", "1 个 B Agent\n本店 + 周边", CYAN),
        ("G", "集团", "GROUP", "N 个 B Agent\n集团 + 联盟", PURPLE),
        ("C", "文旅", "INDUSTRY", "全产业 Agent 网", GOLD),
    ]
    cy = 470
    cw = (W - 2 * MARGIN - 30) // 3
    for i, (icon_letter, name, en, desc, c) in enumerate(tiers):
        x = MARGIN + i * (cw + 15)
        card(draw, x, cy, cw, 600, bg=CARD_BG, border=c)
        # 大字母图标
        glow_circle(draw, x + cw // 2, cy + 70, 50, c)
        draw.ellipse([x + cw // 2 - 45, cy + 25, x + cw // 2 + 45, cy + 115], fill=c)
        draw.text((x + cw // 2, cy + 70), icon_letter, font=f(FONT_HEAVY, 60), fill=WHITE, anchor='mm')
        # 标题
        draw.text((x + cw // 2, cy + 150), name, font=f(FONT_HEAVY, 56), fill=c, anchor='mm')
        draw.text((x + cw // 2, cy + 220), en, font=f(FONT_BOLD, 24), fill=DIM, anchor='mm')
        # 分隔
        draw.line([(x + 30, cy + 260), (x + cw - 30, cy + 260)], fill=c, width=1)
        # 描述
        for j, line in enumerate(desc.split('\n')):
            draw.text((x + cw // 2, cy + 290 + j * 50), line,
                      font=f(FONT_REG, SZ_BODY - 6), fill=WHITE, anchor='mm')
        # 完整闭环标记
        draw.text((x + cw // 2, cy + 540), "✓ 完整闭环", font=f(FONT_BOLD, SZ_BODY - 4), fill=GREEN, anchor='mm')

    # 底部
    center_text(draw, "同  构    自  相  似    可  嵌  套", 1140, f(FONT_BOLD, SZ_BODY + 6), GOLD)

    page_footer(draw, 8, TOTAL)
    return img

def page_09_who():
    """第 9 页：谁适合"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 9, TOTAL, "客 户 · WHO")

    center_text(draw, "AHL 适合谁？", 180, f(FONT_BOLD, SZ_TITLE), CYAN)

    # 5 类客户
    targets = [
        ("01", "单体酒店", "想拿到连锁才有的流量+数据", CYAN),
        ("02", "连锁集团", "想跨店协同 + 跨品牌价值流转", PURPLE),
        ("03", "文旅集团", "想让全产业跨业态握手共生", GOLD),
        ("04", "商业地产", "想盘活空间 · 用 Agent 重新定义", GREEN),
        ("05", "政府/园区", "想掌握行业数据 · 招商赋能", ORANGE),
    ]
    cy = 380
    for i, (num, t, sub, c) in enumerate(targets):
        y = cy + i * 180
        card(draw, MARGIN, y, W - 2 * MARGIN, 150, bg=CARD_BG, border=c)
        # 编号圆
        draw.ellipse([MARGIN + 30, y + 30, MARGIN + 130, y + 130], fill=c)
        draw.text((MARGIN + 80, y + 80), num, font=f(FONT_HEAVY, 44), fill=WHITE, anchor='mm')
        # 标题
        draw.text((MARGIN + 170, y + 30), t, font=f(FONT_BOLD, SZ_HEADING), fill=c)
        draw.text((MARGIN + 170, y + 95), sub, font=f(FONT_REG, SZ_BODY - 4), fill=LIGHT_GRAY)

    page_footer(draw, 9, TOTAL)
    return img

def page_10_economics():
    """第 10 页：经济模型 / 不抽佣"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 10, TOTAL, "经 济 · ECONOMICS")

    center_text(draw, "AHL 怎么赚钱？", 180, f(FONT_BOLD, SZ_TITLE), GOLD)

    # 三大收入来源
    incomes = [
        ("$", "TOKEN 计费", "协议层不抽佣\n但每次握手消耗 TOKEN", CYAN),
        ("+", "增值服务", "Agent 编排 / 行业模板\n数据中台 / 模型微调", GREEN),
        ("@", "生态分成", "商家 Agent 间流转\n按规则收费", PURPLE),
    ]
    cy = 380
    cw = (W - 2 * MARGIN - 30) // 3
    for i, (sym, t, sub, c) in enumerate(incomes):
        x = MARGIN + i * (cw + 15)
        card(draw, x, cy, cw, 480, bg=CARD_BG, border=c)
        # 大符号圆
        draw.ellipse([x + cw // 2 - 50, cy + 30, x + cw // 2 + 50, cy + 130], outline=c, width=3)
        draw.text((x + cw // 2, cy + 80), sym, font=f(FONT_HEAVY, 70), fill=c, anchor='mm')
        draw.text((x + cw // 2, cy + 180), t, font=f(FONT_BOLD, SZ_HEADING), fill=c, anchor='mm')
        for j, line in enumerate(sub.split('\n')):
            draw.text((x + cw // 2, cy + 270 + j * 60), line,
                      font=f(FONT_REG, SZ_BODY - 6), fill=WHITE, anchor='mm')

    # 强调
    card(draw, MARGIN, 960, W - 2 * MARGIN, 220, bg=(80, 60, 0), border=GOLD)
    center_text(draw, "✕  不收佣金    ✕  不做撮合", 990, f(FONT_BOLD, SZ_HEADING), GOLD)
    center_text(draw, "✓  收 TOKEN · 收服务 · 收生态价值", 1080, f(FONT_BOLD, SZ_BODY + 2), GREEN)
    center_text(draw, "价值归创造者", 1140, f(FONT_BOLD, SZ_BODY - 2), LIGHT_GRAY)

    page_footer(draw, 10, TOTAL)
    return img

def page_11_proof():
    """第 11 页：证据 / 数据"""
    img = new_canvas()
    vertical_gradient_bg(img)
    draw = ImageDraw.Draw(img)
    add_stars(draw, 70)

    page_header(draw, 11, TOTAL, "凭 证 · PROOF")

    center_text(draw, "为什么现在能成？", 180, f(FONT_BOLD, 80), LIGHT_GRAY)

    # 5 个支撑
    proofs = [
        ("①", "MCP 协议成熟", "Linux Foundation 治理\nAHL 直接采纳，不用造轮子"),
        ("②", "国产 LLM 突破", "DeepSeek / Qwen 强大\n大幅降低 Agent 成本"),
        ("③", "酒店业供给过剩", "3,500+ 新店 + 70% 单体未连锁\nAHL 切入最佳窗口"),
        ("④", "TOKEN 范式确立", "2027 H1 头部酒店按 TOKEN\n计价管理费 = 可预测"),
        ("⑤", "国资入场", "安逸集团 56 家酒店试点\n省旅投 / 文旅集团跟进"),
    ]
    cy = 350
    for i, (num, t, sub) in enumerate(proofs):
        y = cy + i * 200
        card(draw, MARGIN, y, W - 2 * MARGIN, 175, bg=CARD_BG, border=GOLD)
        # 编号圆
        draw.ellipse([MARGIN + 30, y + 30, MARGIN + 130, y + 130], fill=GOLD)
        draw.text((MARGIN + 80, y + 80), num, font=f(FONT_HEAVY, 50), fill=WHITE, anchor='mm')
        draw.text((MARGIN + 170, y + 30), t, font=f(FONT_BOLD, SZ_HEADING - 4), fill=WHITE)
        for j, line in enumerate(sub.split('\n')):
            draw.text((MARGIN + 170, y + 100 + j * 40), line,
                      font=f(FONT_REG, SZ_BODY - 6), fill=LIGHT_GRAY)

    page_footer(draw, 11, TOTAL)
    return img

def page_12_cta():
    """第 12 页：CTA / 联系"""
    img = new_canvas()
    vertical_gradient_bg(img, (40, 30, 5), (5, 3, 1))
    draw = ImageDraw.Draw(img)
    add_stars(draw, 100)

    page_header(draw, 12, TOTAL, "联 系 · CTA")

    center_text(draw, "如果你也在思考", 250, f(FONT_BOLD, 70), LIGHT_GRAY)
    center_text(draw, "酒店业的下一个 10 年", 340, f(FONT_BOLD, 70), GOLD)

    # CTA 卡
    card(draw, MARGIN, 500, W - 2 * MARGIN, 700, bg=CARD_BG2, border=GOLD, r=24)

    # 电话符号
    draw.ellipse([W // 2 - 80, 530, W // 2 + 80, 690], outline=GOLD, width=4)
    center_text(draw, "CALL", 610, f(FONT_HEAVY, 60), GOLD)

    center_text(draw, "张实 · Eric", 750, f(FONT_BOLD, SZ_TITLE), GOLD)
    center_text(draw, "安逸酒店集团  ·  产业发展部部长", 850, f(FONT_BOLD, SZ_BODY), LIGHT_GRAY)
    center_text(draw, "17760348653 (电话/微信 同号)", 940, f(FONT_BOLD, SZ_HEADING - 4), WHITE)

    # 分隔
    draw.line([(MARGIN + 60, 1000), (W - MARGIN - 60, 1000)], fill=GOLD, width=1)

    center_text(draw, "[ 招  募 ]", 1040, f(FONT_BOLD, SZ_BODY), CYAN)
    center_text(draw, "酒店 AI Agent 早期试点客户", 1090, f(FONT_BOLD, SZ_BODY + 2), WHITE)
    center_text(draw, "（ 5-10 家 · 集团/文旅优先 ）", 1140, f(FONT_REG, SZ_BODY - 6), LIGHT_GRAY)
    center_text(draw, "★  关注我  ★", 1230, f(FONT_BOLD, SZ_BODY + 6), RED)

    page_footer(draw, 12, TOTAL, "ERIC的B166ER 出品 · AHL系列 · 完")
    return img

# ─────────────────────────────────
# 主流程
# ─────────────────────────────────
def main():
    pages = [
        page_01_hook,
        page_02_pain,
        page_03_question,
        page_04_answer,
        page_05_p2p,
        page_06_paradigm,
        page_07_token,
        page_08_fractal,
        page_09_who,
        page_10_economics,
        page_11_proof,
        page_12_cta,
    ]
    print(f"Generating {len(pages)} XHS carousel images → {OUT_DIR}")
    for i, fn in enumerate(pages, 1):
        img = fn()
        path = os.path.join(OUT_DIR, f"ahl_xhs_{i:02d}.png")
        img.save(path, "PNG", quality=95)
        size = os.path.getsize(path)
        print(f"  [{i:02d}/{len(pages)}] {os.path.basename(path)} ({size//1024} KB)")
    print(f"\nDone. {len(pages)} images saved to {OUT_DIR}")

if __name__ == "__main__":
    main()
