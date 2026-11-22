#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_2026_summer_xhs_9.py — 2026 暑期+入境议题 9 图图文 V2 (玉帝视角 · 来龙去脉版)
作者: B166ER 为 ERIC 生成
日期: 2026-07-14
设计理念:
  - 玉帝视角: 上下四方全知 (上帝之眼视角)
  - 来龙去脉: 30 年时间轴缩影
  - 信息密度: 每页 3-5 个数据卡 + 1 个核心 insight
  - 审美: 意境 · 留白 · 气韵 (东方美学)
  - 节奏: 大中小字 + 装饰元素
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path(r"C:/Users/ericz/Desktop/新媒体产品线/2026暑期对冲9图-v2.0/XHS-output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 字体
FONT_HEI_B = "C:/Windows/Fonts/msyhbd.ttc"
FONT_HEI = "C:/Windows/Fonts/msyh.ttc"
FONT_KAI = "C:/Windows/Fonts/simkai.ttf"
FONT_SONG = "C:/Windows/Fonts/simsun.ttc"

# ========== 玉帝视角配色 (深沉天文 + 红日光 + 银月 + 金光 + 雾蓝) ==========
# 主背景: 深夜太空 (近黑·微蓝·高对比)
COL_BG = (8, 11, 30)             # #080B1E 更深沉
COL_BG2 = (16, 22, 50)           # #101632 卡片底
COL_INK = (245, 247, 255)        # 主文 (近乎白)
COL_WHITE = (255, 255, 255)

# 主色: 玉帝朱红 (高对比)
COL_RED = (208, 32, 48)          # #D02030
COL_RED2 = (255, 96, 112)        # 浅红高亮
COL_GOLD = (212, 175, 95)        # #D4AF5F 真金色 (而非黄)
COL_GOLD2 = (255, 215, 100)      # 高亮金
COL_GRAY = (148, 158, 184)       # 中性灰蓝
COL_LIGHT = (190, 200, 220)      # 浅雾蓝
COL_GREEN = (90, 210, 140)       # 增长绿
COL_BLUE = (98, 145, 215)        # 雾蓝
COL_PURPLE = (170, 130, 220)     # 紫气

# 文字字号梯度
F_TINY = 26
F_SMALL = 32
F_BODY = 44
F_BODY_B = 52
F_TITLE = 80
F_T1 = 110     # 一级标题
F_T2 = 150     # 大字号
F_NUM = 130    # 数据大字
F_TINY2 = 22


# ============ 通用工具 ============

def font(size, bold=True):
    return ImageFont.truetype(FONT_HEI_B if bold else FONT_HEI, size)

def draw_corner_marks(draw, W, H, color=COL_GOLD, length=40):
    """四角装饰"""
    L = length
    # Top-left
    draw.line([(40, 40), (40 + L, 40)], fill=color, width=3)
    draw.line([(40, 40), (40, 40 + L)], fill=color, width=3)
    # Top-right
    draw.line([(W - 40 - L, 40), (W - 40, 40)], fill=color, width=3)
    draw.line([(W - 40, 40), (W - 40, 40 + L)], fill=color, width=3)
    # Bottom-left
    draw.line([(40, H - 40), (40 + L, H - 40)], fill=color, width=3)
    draw.line([(40, H - 40 - L), (40, H - 40)], fill=color, width=3)
    # Bottom-right
    draw.line([(W - 40 - L, H - 40), (W - 40, H - 40)], fill=color, width=3)
    draw.line([(W - 40, H - 40 - L), (W - 40, H - 40)], fill=color, width=3)

def draw_top_strip(draw, W, color=COL_RED, h=8):
    """顶部红色色条"""
    draw.rectangle([(0, 0), (W, h)], fill=color)

def draw_top_meta(draw, W, idx, total, label, sub=""):
    """顶部元数据 (页码 + label + 副)"""
    f_kicker = font(F_TINY2)
    f_p = font(F_TINY, bold=True)
    draw.text((60, 50), f"{idx:02d} / {total:02d}", fill=COL_GRAY, font=f_kicker)
    # 右: label + 副
    label_x = W - 60
    draw.text((label_x, 50), label, fill=COL_GOLD, font=f_p, anchor="ra")

def draw_footer(draw, W, H, text, brand="ERIC的B166ER出品"):
    """统一 footer"""
    f = font(F_TINY)
    draw.line([(60, H - 90), (W - 60, H - 90)], fill=COL_GRAY, width=1)
    draw.text((60, H - 70), brand, fill=COL_GRAY, font=f)
    # 右: 副文本
    if text:
        draw.text((W - 60, H - 70), text, fill=COL_LIGHT, font=f, anchor="ra")

def draw_kicker(draw, x, y, text, max_w=None):
    """红色小型 kicker (英文小标签)"""
    f = font(F_TINY + 4, bold=True)
    # 装饰线
    draw.line([(x, y + 18), (x + 60, y + 18)], fill=COL_RED, width=3)
    draw.text((x + 75, y), text, fill=COL_RED, font=f)
    return y + 50


# ========== 9 张图 ==========

def gen_01_cover(idx, total):
    """封面: 玉帝视角 · 来龙去脉"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    # 大气: 加微噪点 (星空感)
    import random
    random.seed(42)
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 2)
        a = random.randint(40, 100)
        draw.ellipse([(x, y), (x + s, y + s)], fill=(180, 200, 240))

    # 顶部
    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "封面 · 玉帝视角")
    draw.text((W // 2, 110), "ERIC的B166ER出品", fill=COL_GOLD, font=font(24), anchor="mm")
    draw.text((W // 2, 145), "V3 BRUTALIST · 2026.07.14", fill=COL_GRAY, font=font(20), anchor="mm")

    # 玉帝视角 (天眼)
    eye_y = 220
    # 中心圆
    draw.ellipse([(W // 2 - 100, eye_y - 100), (W // 2 + 100, eye_y + 100)], fill=COL_BG2, outline=COL_GOLD, width=4)
    draw.ellipse([(W // 2 - 60, eye_y - 60), (W // 2 + 60, eye_y + 60)], fill=COL_RED, outline=COL_GOLD, width=3)
    draw.ellipse([(W // 2 - 30, eye_y - 30), (W // 2 + 30, eye_y + 30)], fill=COL_GOLD)
    # 瞳仁
    draw.ellipse([(W // 2 - 12, eye_y - 12), (W // 2 + 12, eye_y + 12)], fill=(20, 20, 20))
    # 射线
    import math
    for i in range(12):
        ang = i * 30 * math.pi / 180
        x1 = W // 2 + 130 * math.cos(ang)
        y1 = eye_y + 130 * math.sin(ang)
        x2 = W // 2 + 180 * math.cos(ang)
        y2 = eye_y + 180 * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=COL_GOLD, width=2)

    # 副标: 玉帝之眼 · 5 年大局
    draw.text((W // 2, eye_y + 220), "上知天文 · 下知地理 · 五年生死一瞬看透", fill=COL_LIGHT, font=font(34), anchor="mm")

    # 主标题 (3 行)
    title_y = eye_y + 290
    draw.text((60, title_y), "今年暑期", fill=COL_INK, font=font(90, bold=False))
    draw.text((60, title_y + 105), "酒店最冷的一年", fill=COL_RED, font=font(95, bold=True))

    # 副 (黑底红字)
    sub_y = title_y + 230
    draw.text((60, sub_y), "但可能是未来 5 年", fill=COL_GOLD, font=font(56))
    draw.text((60, sub_y + 70), "最好的一年", fill=COL_GOLD, font=font(56, bold=True))

    # 来龙去脉时间轴 (玉帝视角 = 全景视野)
    tl_y = sub_y + 180
    draw.text((60, tl_y), "来龙去脉 · 全景", fill=COL_RED, font=font(28, bold=True))
    # 时间轴主线
    draw.line([(60, tl_y + 70), (W - 60, tl_y + 70)], fill=COL_GOLD, width=3)

    timeline_data = [
        ("30 年", "制造业立国", COL_GRAY),
        ("10 年", "服务+消费", COL_LIGHT),
        ("5 年", "旅游强国", COL_GOLD),
        ("今天", "入境起飞", COL_RED),
    ]
    step_w = (W - 120) // 4
    for i, (period, label, color) in enumerate(timeline_data):
        cx = 60 + i * step_w + step_w // 2
        draw.ellipse([(cx - 14, tl_y + 56), (cx + 14, tl_y + 84)], fill=color)
        draw.text((cx, tl_y + 25), period, fill=color, font=font(28, bold=True), anchor="mm")
        draw.text((cx, tl_y + 110), label, fill=color, font=font(24), anchor="mm")

    # 5 个看点 (排序小卡)
    cards_y = tl_y + 180
    cards = [
        "01\n冷数据",
        "02\n暖数据",
        "03\n规划",
        "04\n第一性",
        "05\n行动",
    ]
    card_w = 180
    gap = 12
    total_w = 5 * card_w + 4 * gap
    start_x = (W - total_w) // 2
    for i, label in enumerate(cards):
        x = start_x + i * (card_w + gap)
        draw.rounded_rectangle([(x, cards_y), (x + card_w, cards_y + 90)], radius=10, fill=COL_BG2, outline=COL_GOLD, width=2)
        # 2 行
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            sz = font(28) if li == 0 else font(24)
            color = COL_GOLD if li == 0 else COL_INK
            draw.text((x + card_w // 2, cards_y + 25 + li * 32), ln, fill=color, font=sz, anchor="mm")

    # 品牌
    draw.text((W // 2, H - 50), "看清全貌 · 不被噪音带节奏", fill=COL_GOLD, font=font(28), anchor="mm")
    draw_corner_marks(draw, W, H)
    return img


def gen_02_question(idx, total):
    """议题: 全网在议论什么"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    # 顶部
    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "全网议题 · 全景扫描")

    # 标题
    draw.text((60, 130), "全网在说的 3 件事", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "看似矛盾 · 实则同一格局", fill=COL_GOLD, font=font(36))

    # 3 个议题卡片
    y = 320
    h = 220
    gap = 25
    items = [
        ("01", "今年暑期生意差", "中小单体'有客流不盈利'", COL_RED, "锦江 -10.8% RevPAR"),
        ("02", "可能未来 5 年最好", "酒店圈广泛讨论的判断", COL_GOLD, "无清晰数据依据"),
        ("03", "中央 7 月发五年规划", "大提入境 1.9 亿人次", COL_BLUE, "国函〔2026〕61 号"),
    ]
    for i, (num, title, sub, color, badge) in enumerate(items):
        yi = y + i * (h + gap)
        # 卡片底
        draw.rounded_rectangle([(60, yi), (W - 60, yi + h)], radius=15, fill=COL_BG2)
        # 左侧大编号
        draw.text((100, yi + h // 2), num, fill=color, font=font(110, bold=True), anchor="lm")
        # 分隔
        draw.line([(220, yi + 30), (220, yi + h - 30)], fill=color, width=3)
        # 文
        draw.text((245, yi + 35), title, fill=COL_INK, font=font(46, bold=True))
        draw.text((245, yi + 105), sub, fill=COL_LIGHT, font=font(32))
        # 角标
        draw.rounded_rectangle([(245, yi + 155), (245 + 380, yi + 195)], radius=8, fill=COL_BG)
        draw.text((435, yi + 175), badge, fill=color, font=font(26, bold=True), anchor="mm")

    # 玉帝视角注脚
    notice_y = y + 3 * h + 3 * gap + 30
    draw.rounded_rectangle([(60, notice_y), (W - 60, notice_y + 100)], radius=12, fill=COL_BG2, outline=COL_GOLD, width=3)
    draw.text((W // 2, notice_y + 30), "玉帝视角:3 件事不是矛盾,是时间切片", fill=COL_GOLD, font=font(34, bold=True), anchor="mm")
    draw.text((W // 2, notice_y + 70), "国内卷到顶点 + 入境起飞 = 5 年战略级窗口", fill=COL_RED, font=font(30, bold=True), anchor="mm")

    draw_footer(draw, W, H, "01→09")
    draw_corner_marks(draw, W, H)
    return img


def gen_03_cold(idx, total):
    """国内冷核心证据: 4 数据 + 趋势"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "国内端 · 真冷")

    # 标题
    draw.text((60, 130), "酒店业这 10 年", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "从 黄金期 → 拐点 → 持续下行", fill=COL_GOLD, font=font(36))

    # 30 年小时间线 (顶部)
    tl_y = 300
    tl_data = [
        ("2015", "黄金期", COL_GREEN),
        ("2019", "拐点", COL_GOLD),
        ("2024", "首下滑", COL_RED2),
        ("2026", "内卷", COL_RED),
    ]
    draw.text((60, tl_y), "10 年时间轴", fill=COL_GRAY, font=font(22))
    for i, (year, label, c) in enumerate(tl_data):
        x = 60 + i * 240
        draw.ellipse([(x, tl_y + 30), (x + 30, tl_y + 60)], fill=c)
        draw.text((x + 15, tl_y + 90), year, fill=c, font=font(26, bold=True), anchor="mm")
        draw.text((x + 15, tl_y + 120), label, fill=c, font=font(22), anchor="mm")
        if i < 3:
            draw.line([(x + 30, tl_y + 45), (x + 240, tl_y + 45)], fill=COL_GRAY, width=2)

    # 4 大数据 (大字号)
    stats_y = 470
    stats = [
        ("-10.8%", "锦江全服务型\nRevPAR 2024", COL_RED),
        ("-6.77%", "亚朵 RevPAR\n持续 2 年下行", COL_RED),
        ("-7.41%", "锦江全服务型\nADR 难提", COL_RED2),
        ("-3 年", "格林酒店入住率\n76%→69.4%", COL_RED2),
    ]
    # 2x2 网格
    s_w = 480
    s_h = 200
    s_gap_x = 20
    s_gap_y = 20
    for i, (val, label, color) in enumerate(stats):
        col = i % 2
        row = i // 2
        x = 60 + col * (s_w + s_gap_x)
        y = stats_y + row * (s_h + s_gap_y)
        draw.rounded_rectangle([(x, y), (x + s_w, y + s_h)], radius=15, fill=COL_BG2, outline=color, width=3)
        # 数字
        draw.text((x + 30, y + 30), val, fill=color, font=font(80, bold=True))
        # 标签 (下)
        for li, ln in enumerate(label.split("\n")):
            draw.text((x + 30, y + 130 + li * 26), ln, fill=COL_LIGHT, font=font(24))

    # 玉帝视角结论
    conclusion_y = stats_y + 2 * (s_h + s_gap_y) + 30
    draw.rounded_rectangle([(60, conclusion_y), (W - 60, conclusion_y + 130)], radius=15, fill=COL_BG2)
    draw.text((W // 2, conclusion_y + 30), "—— 玉帝视角 ——", fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
    draw.text((W // 2, conclusion_y + 80), "不是某家的偶然 · 是 5 年结构拐点", fill=COL_RED, font=font(42, bold=True), anchor="mm")

    draw_footer(draw, W, H, "数据 · 锦江/亚朵/格林 2024 年报")
    draw_corner_marks(draw, W, H)
    return img


def gen_04_inbound(idx, total):
    """入境飞起证据"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W, COL_GOLD)
    draw_top_meta(draw, W, idx, total, "入境端 · 真火")

    # 标题
    draw.text((60, 130), "入境起飞 · 真数据", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "5 年唯一 两位数增长 的赛道", fill=COL_GOLD, font=font(36))

    # 时间线横向
    tl_y = 300
    draw.text((60, tl_y), "2026 年时间轴", fill=COL_GRAY, font=font(22))
    tl_data = [
        ("Q1", "+22.3%", "出入境外国人", "2133.3 万人次"),
        ("Q1免", "+29.3%", "免签入境", "831.5 万人次"),
        ("H1免", "+30.6%", "免签累计", "1781.5 万人次"),
        ("2025", "+39.2%", "入境花费", "1311 亿美元"),
    ]
    for i, (period, growth, label, volume) in enumerate(tl_data):
        x = 60 + i * 245
        # 卡片
        draw.rounded_rectangle([(x, tl_y + 40), (x + 235, tl_y + 200)], radius=12, fill=COL_BG2, outline=COL_GREEN, width=2)
        draw.text((x + 115, tl_y + 70), period, fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
        draw.text((x + 115, tl_y + 110), growth, fill=COL_GREEN, font=font(46, bold=True), anchor="mm")
        draw.text((x + 115, tl_y + 155), label, fill=COL_LIGHT, font=font(20), anchor="mm")
        draw.text((x + 115, tl_y + 180), volume, fill=COL_GRAY, font=font(18), anchor="mm")

    # 客源结构 (饼图替代: 百分比+标签列表)
    src_y = 550
    draw.text((60, src_y), "客源结构 (2026 H1)", fill=COL_RED, font=font(32, bold=True))
    sources = [
        ("亚洲", 60, COL_GOLD, "韩/马/新/日/泰 + 俄罗斯(120%↑)"),
        ("欧美", 18, COL_BLUE, "英/法/德/澳 单免签后均 +30%"),
        ("新兴", 14, COL_PURPLE, "一带一路 阿根廷/沙特 数倍增"),
        ("其他", 8, COL_GRAY, ""),
    ]
    # 横条进度图
    bar_y = src_y + 60
    bar_max_w = W - 120
    cumulative_x = 60
    for i, (label, pct, color, note) in enumerate(sources):
        w = int(bar_max_w * pct / 100)
        draw.rectangle([(cumulative_x, bar_y), (cumulative_x + w, bar_y + 50)], fill=color)
        if pct >= 12:
            draw.text((cumulative_x + w // 2, bar_y + 25), f"{pct}%", fill=COL_BG, font=font(22, bold=True), anchor="mm")
        cumulative_x += w

    # 图例 + note
    leg_y = bar_y + 70
    legend_x = 60
    for i, (label, pct, color, note) in enumerate(sources):
        # 色块
        draw.rectangle([(legend_x, leg_y), (legend_x + 14, leg_y + 14)], fill=color)
        draw.text((legend_x + 22, leg_y - 4), f"{label} {pct}%", fill=color, font=font(22, bold=True))
        if note:
            draw.text((legend_x + 22, leg_y + 22), note, fill=COL_LIGHT, font=font(20))
        legend_x += 240 if i == 0 else 240

    # 玉帝视角
    yv_y = leg_y + 130
    draw.rounded_rectangle([(60, yv_y), (W - 60, yv_y + 100)], radius=12, fill=COL_BG2, outline=COL_RED, width=3)
    draw.text((W // 2, yv_y + 30), "—— 玉帝视角 ——", fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
    draw.text((W // 2, yv_y + 70), "入境起飞是 5 年唯一高确定性赛道", fill=COL_RED, font=font(36, bold=True), anchor="mm")

    draw_footer(draw, W, H, "数据 · 国家移民管理局")
    draw_corner_marks(draw, W, H)
    return img


def gen_05_plan(idx, total):
    """5 年规划对齐"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "5 年规划 · 战略对齐")

    # 标题
    draw.text((60, 130), "国函〔2026〕61 号", fill=COL_GOLD, font=font(60, bold=True))
    draw.text((60, 200), "旅游强国十五五规划", fill=COL_INK, font=font(58, bold=True))
    draw.text((60, 265), "中央顶层纲领 · 2026 - 2030", fill=COL_LIGHT, font=font(32))

    # 2030 目标 (左右对比)
    goal_y = 350
    draw.text((60, goal_y), "2030 年目标", fill=COL_RED, font=font(30, bold=True))
    goals = [
        ("国内出游", "83 亿", "人次", "CAGR 6.7%", COL_GOLD),
        ("国内收入", "7.7 万亿", "元", "CAGR 6.2%", COL_GOLD),
        ("入境人次", "1.9 亿", "人次", "CAGR 7.6%", COL_RED),
        ("入境花费", "1500 亿", "美元", "CAGR 10.8%", COL_RED2),
    ]
    gw = 480
    gh = 130
    for i, (label, val, unit, cagr, color) in enumerate(goals):
        col = i % 2
        row = i // 2
        x = 60 + col * (gw + 20)
        y = goal_y + 50 + row * (gh + 15)
        draw.rounded_rectangle([(x, y), (x + gw, y + gh)], radius=12, fill=COL_BG2, outline=color, width=2)
        draw.text((x + 20, y + 15), label, fill=COL_LIGHT, font=font(24))
        draw.text((x + 20, y + 50), val + " " + unit, fill=color, font=font(46, bold=True))
        # CAGR 角标
        draw.rounded_rectangle([(x + gw - 100, y + gh - 38), (x + gw - 20, y + gh - 18)], radius=6, fill=color)
        draw.text((x + gw - 60, y + gh - 28), cagr, fill=COL_BG, font=font(20, bold=True), anchor="mm")

    # 88 城市 + 11 工程 + 9 保障
    struct_y = goal_y + 50 + 2 * (gh + 15) + 30
    draw.text((60, struct_y), "结构", fill=COL_RED, font=font(28, bold=True))
    structs = [
        ("88 城", "32+33+23", "城市体系"),
        ("11 工", "智慧/入境\n冰雪提质", "专项工程"),
        ("9 重", "资金/土地\n人才/组织", "保障体系"),
        ("3 化", "智能/绿色\n融合", "产业动能"),
    ]
    sw = 230
    sh = 130
    for i, (num, content, label) in enumerate(structs):
        x = 60 + i * (sw + 10)
        y = struct_y + 40
        draw.rounded_rectangle([(x, y), (x + sw, y + sh)], radius=10, fill=COL_BG2, outline=COL_GOLD, width=2)
        draw.text((x + sw // 2, y + 25), num, fill=COL_GOLD, font=font(34, bold=True), anchor="mm")
        # 多行
        for li, ln in enumerate(content.split("\n")):
            draw.text((x + sw // 2, y + 65 + li * 20), ln, fill=COL_INK, font=font(20), anchor="mm")
        draw.text((x + sw // 2, y + sh - 18), label, fill=COL_GRAY, font=font(18, bold=True), anchor="mm")

    # 玉帝视角
    yv_y = struct_y + 40 + sh + 50
    draw.rounded_rectangle([(60, yv_y), (W - 60, yv_y + 100)], radius=12, fill=COL_BG2)
    draw.text((W // 2, yv_y + 30), "—— 玉帝视角 ——", fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
    draw.text((W // 2, yv_y + 70), "入境 CAGR 10.8% > 国内 6.7%", fill=COL_RED, font=font(38, bold=True), anchor="mm")

    draw_footer(draw, W, H, "数据 · 国务院公报")
    draw_corner_marks(draw, W, H)
    return img


def gen_06_first_principles(idx, total):
    """第一性原理 + 来龙去脉"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "第一性原理")

    # 标题
    draw.text((60, 130), "剥到本质", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "入境 不是对冲 · 是 5 年国家战略", fill=COL_GOLD, font=font(36))

    # 三层还原 (蛋黄型)
    layers_y = 320
    layer_h = 150
    layers = [
        ("第 1 层 · 现象", "今年暑期冷 + 中央大提入境", COL_GRAY),
        ("第 2 层 · 机制", "国内卷化 + 入境起飞 同时出现", COL_GOLD),
        ("第 3 层 · 本质", "中国从 出口立国 → 消费+服务+出海", COL_RED),
    ]
    for i, (label, content, color) in enumerate(layers):
        y = layers_y + i * (layer_h + 15)
        # 左侧索引号 (大)
        draw.text((60, y + layer_h // 2), str(i + 1), fill=color, font=font(150, bold=True), anchor="lm")
        # 卡片
        draw.rounded_rectangle([(180, y), (W - 60, y + layer_h)], radius=12, fill=COL_BG2, outline=color, width=2)
        draw.text((210, y + 25), label, fill=color, font=font(28, bold=True))
        draw.text((210, y + 75), content, fill=COL_INK, font=font(38, bold=True))

    # 因为不是短期对冲 - 5 个理由
    reason_y = layers_y + 3 * (layer_h + 15) + 30
    draw.text((60, reason_y), "为什么不是对冲?", fill=COL_RED, font=font(30, bold=True))
    reasons = [
        ("①", "入境政策始于 2023", "显著早于今年暑期"),
        ("②", "5 年 2026-2030 规划", "不止一年,长期"),
        ("③", "对美博弈 + 文化输出", "超出经济对冲范畴"),
        ("④", "CAGR 10.8% 是战略目标", "不是应急反应"),
        ("⑤", "玉帝:不止 看飞 还要 造飞", "国家意志级投入"),
    ]
    # 两列
    rw = (W - 120 - 20) // 2
    rh = 50
    for i, (num, label, sub) in enumerate(reasons):
        col = i % 2
        row = i // 2
        x = 60 + col * (rw + 20)
        y = reason_y + 40 + row * (rh + 10)
        draw.ellipse([(x, y + 8), (x + 35, y + 43)], fill=COL_RED)
        draw.text((x + 17, y + 26), num, fill=COL_WHITE, font=font(20, bold=True), anchor="mm")
        draw.text((x + 45, y + 5), label, fill=COL_INK, font=font(24, bold=True))
        draw.text((x + 45, y + 30), sub, fill=COL_GRAY, font=font(20))

    # 玉帝视角 - 大结论
    yv_y = reason_y + 40 + 3 * (rh + 10) + 30
    draw.rounded_rectangle([(60, yv_y), (W - 60, yv_y + 90)], radius=12, fill=COL_RED)
    draw.text((W // 2, yv_y + 45), "时间巧合 · 本质长期", fill=COL_WHITE, font=font(48, bold=True), anchor="mm")

    draw_footer(draw, W, H, "5 角度论证 · 多源验证")
    draw_corner_marks(draw, W, H)
    return img


def gen_07_timeline(idx, total):
    """5 年时间线全景"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "5 年全景 · 时间线")

    # 标题
    draw.text((60, 130), "5 年战略节奏", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "Eric 4 个项目 × 5 年窗口", fill=COL_GOLD, font=font(36))

    # 横向时间线 (主线 + 4 个时间节点)
    tl_y = 360
    # 主线
    draw.line([(80, tl_y), (W - 80, tl_y)], fill=COL_GOLD, width=4)
    # 4 个节点
    nodes = [
        ("2026", "政策密集\n入境起飞", "AHL 升级\n+1 SKILL", COL_RED),
        ("2027-28", "AI 分水岭\n入境 1.85 亿", "集团立项\n完成", COL_GOLD),
        ("2028-29", "5 年规划中段", "AHL ≥100 酒店\n团队 ≥10", COL_RED2),
        ("2030", "5 年收官", "Eric 中期\n目标验证", COL_GOLD),
    ]
    nw = (W - 160) // 4
    for i, (year, headline, action, color) in enumerate(nodes):
        cx = 80 + i * nw + nw // 2
        # 节点圆
        draw.ellipse([(cx - 28, tl_y - 28), (cx + 28, tl_y + 28)], fill=color)
        draw.ellipse([(cx - 18, tl_y - 18), (cx + 18, tl_y + 18)], fill=COL_BG)
        draw.ellipse([(cx - 10, tl_y - 10), (cx + 10, tl_y + 10)], fill=color)
        # 年份
        draw.text((cx, tl_y - 80), year, fill=color, font=font(36, bold=True), anchor="mm")
        # 标题
        for li, ln in enumerate(headline.split("\n")):
            draw.text((cx, tl_y + 80 + li * 30), ln, fill=COL_INK, font=font(28, bold=True), anchor="mm")
        # 行动
        for li, ln in enumerate(action.split("\n")):
            draw.text((cx, tl_y + 160 + li * 28), ln, fill=COL_LIGHT, font=font(22), anchor="mm")
        # 卡片底 (圈住整个节点)
        card_w = nw - 30
        draw.rounded_rectangle([(cx - card_w // 2, tl_y + 90), (cx + card_w // 2, tl_y + 280)], radius=15, fill=COL_BG2)
        # 重新绘制内容 (避免遮挡)
        for li, ln in enumerate(headline.split("\n")):
            draw.text((cx, tl_y + 130 + li * 30), ln, fill=COL_INK, font=font(26, bold=True), anchor="mm")
        for li, ln in enumerate(action.split("\n")):
            draw.text((cx, tl_y + 210 + li * 26), ln, fill=COL_LIGHT, font=font(22), anchor="mm")

    # 4 个项目 × 时间线 (小卡片)
    proj_y = 800
    draw.text((60, proj_y), "Eric 5 年 × 4 个项目对齐", fill=COL_RED, font=font(28, bold=True))
    projects = [
        ("安逸集团", "P0 0-5 年", "接住 88 城 × 5 城红利", COL_GOLD),
        ("AHL 平台", "P0 升级", "智能旅游基础设施供应商", COL_RED),
        ("跨境业务", "P1 升级", "入境 + 出境 双轨", COL_BLUE),
        ("医养酒店", "P2 立项", "融合业态直接命中", COL_PURPLE),
    ]
    pw = 240
    for i, (name, priority, desc, color) in enumerate(projects):
        x = 60 + i * (pw + 8)
        y = proj_y + 40
        draw.rounded_rectangle([(x, y), (x + pw, y + 160)], radius=12, fill=COL_BG2, outline=color, width=2)
        draw.text((x + 15, y + 15), name, fill=color, font=font(26, bold=True))
        draw.text((x + 15, y + 50), priority, fill=COL_GOLD, font=font(20))
        draw.text((x + 15, y + 80), desc, fill=COL_LIGHT, font=font(20))
        # P0 高亮
        if priority.startswith("P0"):
            draw.rounded_rectangle([(x + pw - 50, y + 15), (x + pw - 15, y + 45)], radius=6, fill=COL_RED)
            draw.text((x + pw - 32, y + 30), "★", fill=COL_GOLD, font=font(20, bold=True), anchor="mm")

    # 玉帝视角
    yv_y = proj_y + 240
    draw.rounded_rectangle([(60, yv_y), (W - 60, yv_y + 100)], radius=12, fill=COL_BG2, outline=COL_GOLD, width=3)
    draw.text((W // 2, yv_y + 30), "—— 玉帝视角 ——", fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
    draw.text((W // 2, yv_y + 70), "4 项目 × 5 年 = 历史性窗口期", fill=COL_RED, font=font(40, bold=True), anchor="mm")

    draw_footer(draw, W, H, "玉帝视角 · 全景对齐")
    draw_corner_marks(draw, W, H)
    return img


def gen_08_types(idx, total):
    """5 类酒店不同命运: 矩阵图"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W)
    draw_top_meta(draw, W, idx, total, "5 类酒店 · 不同命运")

    # 标题
    draw.text((60, 130), "不是所有酒店都冷", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "5 类酒店 × 未来 5 年命运", fill=COL_GOLD, font=font(36))

    # 矩阵: 2x3 (5 类 + 1 大热)
    matrix_y = 310
    tw = 320
    th = 200
    tg_x = 30
    tg_y = 20
    types = [
        ("经济型", "持续压力", "ADR 难提", "-", COL_RED, "靠加盟下沉\n难以涨价"),
        ("中端", "微利内卷", "靠差异化活", "~", COL_RED2, "两头挤压\nAI 改造是关键"),
        ("高端", "提价有限", "靠体验升级", "+", COL_GOLD, "靠场景化\n+ 文化 IP"),
        ("度假资源", "稳定溢价", "稀缺资源", "+", COL_BLUE, "青城山/稻城\n九寨沟受益"),
        ("入境接待", "高增优先", "5 年窗口", "+++", COL_RED, "战略命中\n政策红利"),
    ]
    for i, (name, now, future, arrow, color, sub) in enumerate(types):
        col = i % 3
        row = i // 3
        x = 60 + col * (tw + tg_x)
        y = matrix_y + row * (th + tg_y)
        draw.rounded_rectangle([(x, y), (x + tw, y + th)], radius=15, fill=COL_BG2, outline=color, width=3)
        # 名称
        draw.text((x + 20, y + 15), name, fill=color, font=font(34, bold=True))
        # 趋势符号
        draw.rounded_rectangle([(x + tw - 80, y + 20), (x + tw - 20, y + 70)], radius=8, fill=color)
        draw.text((x + tw - 50, y + 45), arrow, fill=COL_BG, font=font(36, bold=True), anchor="mm")
        # 现在
        draw.text((x + 20, y + 75), "现在 · " + now, fill=COL_LIGHT, font=font(22))
        # 未来
        draw.text((x + 20, y + 110), "5 年后 · " + future, fill=COL_INK, font=font(26, bold=True))
        # 多行 sub
        for li, ln in enumerate(sub.split("\n")):
            draw.text((x + 20, y + 150 + li * 22), ln, fill=COL_GRAY, font=font(20))

    # 玉帝视角
    yv_y = matrix_y + 2 * (th + tg_y) + 30
    draw.rounded_rectangle([(60, yv_y), (W - 60, yv_y + 90)], radius=12, fill=COL_RED)
    draw.text((W // 2, yv_y + 45), "5 类酒店 · 5 种命运", fill=COL_WHITE, font=font(46, bold=True), anchor="mm")

    draw_footer(draw, W, H, "矩阵分类 · 玉帝视角")
    draw_corner_marks(draw, W, H)
    return img


def gen_09_action(idx, total):
    """行动建议"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    draw_top_strip(draw, W, COL_GOLD)
    draw_top_meta(draw, W, idx, total, "行动 · 别等")

    # 标题
    draw.text((60, 130), "别等 · 主动抢", fill=COL_INK, font=font(75, bold=True))
    draw.text((60, 215), "3 个动作 · 抓住 5 年窗口", fill=COL_RED, font=font(36, bold=True))

    # 3 个动作 (大卡片)
    action_y = 320
    actions = [
        ("01", "立即 · 14 天", "AHL Agent 加\n'入境多语 SKILL'", "智能升级", COL_RED),
        ("02", "30 天", "跨境业务升级为\n'入境 + 出境'双轨", "结构升级", COL_GOLD),
        ("03", "90 天", "集团内立项\n'智慧旅游 + 入境促进'双申报", "政策红利", COL_BLUE),
    ]
    aw = W - 120
    ah = 200
    for i, (num, timing, content, badge, color) in enumerate(actions):
        y = action_y + i * (ah + 25)
        # 主卡片
        draw.rounded_rectangle([(60, y), (60 + aw, y + ah)], radius=15, fill=COL_BG2, outline=color, width=3)
        # 左: 大编号
        draw.text((90, y + ah // 2), num, fill=color, font=font(140, bold=True), anchor="lm")
        # 中: timing + content
        draw.text((210, y + 30), timing, fill=color, font=font(36, bold=True))
        for li, ln in enumerate(content.split("\n")):
            draw.text((210, y + 85 + li * 38), ln, fill=COL_INK, font=font(34, bold=True))
        # 右: badge
        draw.rounded_rectangle([(60 + aw - 130, y + 30), (60 + aw - 30, y + 80)], radius=8, fill=color)
        draw.text((60 + aw - 80, y + 55), badge, fill=COL_BG, font=font(22, bold=True), anchor="mm")
        # 下方注释
        draw.text((210, y + ah - 30), "→ 立即执行,别等政策发布才动", fill=COL_GRAY, font=font(22))

    # 玉帝视角 · 心法
    heart_y = action_y + 3 * (ah + 25) + 30
    # 大色块
    draw.rounded_rectangle([(60, heart_y), (W - 60, heart_y + 130)], radius=15, fill=COL_RED)
    draw.text((W // 2, heart_y + 30), "—— 玉帝视角心法 ——", fill=COL_GOLD, font=font(28, bold=True), anchor="mm")
    draw.text((W // 2, heart_y + 75), "不在风口 · 在与已有能力的对接点", fill=COL_WHITE, font=font(34, bold=True), anchor="mm")

    draw_footer(draw, W, H, "ERIC的B166ER出品 · V3")
    draw_corner_marks(draw, W, H)
    return img


GENERATORS = [
    gen_01_cover,
    gen_02_question,
    gen_03_cold,
    gen_04_inbound,
    gen_05_plan,
    gen_06_first_principles,
    gen_07_timeline,
    gen_08_types,
    gen_09_action,
]

# ============ 主流程 ============

if __name__ == "__main__":
    print(f"开始生成 {len(GENERATORS)} 张 (玉帝视角 V2)...")
    for i, gen in enumerate(GENERATORS, 1):
        img = gen(i, len(GENERATORS))
        out_path = OUT_DIR / f"{i:02d}_v2.png"
        img.save(out_path, "PNG", optimize=True)
        print(f"  ✅ [{i:02d}/{len(GENERATORS):02d}] {out_path.name} ({out_path.stat().st_size / 1024:.1f} KB)")
    print(f"\n✅ 全部完成 → {OUT_DIR}")
