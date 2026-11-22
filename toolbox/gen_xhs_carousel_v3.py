#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书范式 · 酒店品牌市场指数综合排名
12 张图卡片 · 1080x1440 (3:4) · 移动端优先
v3.0: emoji 全部改用纯文字符号 + 几何图形 (避免字体兼容问题)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\ericz\Desktop\小红书_酒店品牌地图"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1440
MARGIN = 60

# 配色
BG = (250, 244, 234)
CARD_BG = (255, 252, 247)
DARK = (60, 40, 25)
GOLD = (183, 121, 31)
RED = (200, 16, 46)
GREEN = (31, 77, 42)
GRAY = (130, 110, 90)
LINE = (220, 200, 175)
WHITE = (255, 255, 255)
LIGHT_GOLD = (220, 180, 100)

# 字体
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_HEAVY = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
FONT_SYM = r"C:\Windows\Fonts\seguiemj.ttf"

# 字体大小
SZ_TITLE = 84
SZ_HEADING = 64
SZ_BODY = 36
SZ_TAG = 28
SZ_NUM = 92
SZ_NUM_MED = 72
SZ_FOOTER = 22


def f(path, size):
    return ImageFont.truetype(path, size)


def new_canvas():
    img = Image.new('RGB', (W, H), BG)
    return img, ImageDraw.Draw(img)


def bg_pattern(draw):
    for i in range(0, W, 90):
        for j in range(0, H, 90):
            if (i + j) % 180 == 0:
                draw.ellipse([i, j, i+8, j+8], fill=(245, 235, 220))


def add_footer(draw, page, total):
    draw.line([(MARGIN, H - 130), (W - MARGIN, H - 130)], fill=LINE, width=2)
    draw.text((MARGIN, H - 105), "B166ER 出品", font=f(FONT_BOLD, SZ_FOOTER + 2), fill=DARK)
    draw.text((MARGIN, H - 75), "ERIC的B166ER · 酒店行业地图", font=f(FONT_REG, SZ_FOOTER - 4), fill=GRAY)
    pt = f"{page:02d} / {total:02d}"
    draw.text((W - MARGIN, H - 90), pt, font=f(FONT_BOLD, SZ_FOOTER + 4), fill=GOLD, anchor='rt')


def header_strip(draw, label, color=GOLD):
    bb = draw.textbbox((0, 0), label, font=f(FONT_BOLD, SZ_TAG + 2))
    tw = bb[2] - bb[0]
    x = (W - tw - 40) // 2
    draw.rounded_rectangle([x, 60, x + tw + 40, 116], 28, fill=color)
    draw.text((x + 20, 72), label, font=f(FONT_BOLD, SZ_TAG + 2), fill=WHITE)


def card(draw, x, y, w, h, bg=CARD_BG, border=None, r=20):
    draw.rounded_rectangle([x, y, x+w, y+h], r, fill=bg)
    if border:
        draw.rounded_rectangle([x, y, x+w, y+h], r, outline=border, width=2)


def big_star(draw, x, y, size, color):
    """绘制实心五角星"""
    import math
    points = []
    for i in range(10):
        angle = math.pi / 2 - i * math.pi * 2 / 10
        r = size * (1 if i % 2 == 0 else 0.42)
        points.append((x + r * math.cos(angle), y - r * math.sin(angle)))
    draw.polygon(points, fill=color)


def check_mark(draw, x, y, size, color):
    """绘制对勾"""
    w = size * 0.6
    draw.line([(x - w * 0.6, y), (x - w * 0.15, y + w * 0.4)], fill=color, width=int(size * 0.18))
    draw.line([(x - w * 0.15, y + w * 0.4), (x + w * 0.6, y - w * 0.4)], fill=color, width=int(size * 0.18))


def badge_circle(draw, x, y, size, char, color, text_color=WHITE, font_path=None):
    """圆圈徽章(替代 emoji 圆圈)"""
    draw.ellipse([x - size/2, y - size/2, x + size/2, y + size/2], fill=color)
    fp = font_path or FONT_BOLD
    fs = int(size * 0.55)
    bb = draw.textbbox((0, 0), char, font=f(fp, fs))
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text((x - tw/2, y - th/2 - size*0.05), char, font=f(fp, fs), fill=text_color)


# ============== Page 01 封面 ==============
TOTAL = 12

def page_01_cover():
    img, draw = new_canvas()
    bg_pattern(draw)
    draw.rectangle([0, 0, W, 16], fill=GOLD)

    label = "酒店行业深度报告"
    bb = draw.textbbox((0, 0), label, font=f(FONT_BOLD, SZ_TAG + 4))
    tw = bb[2] - bb[0]
    x = (W - tw - 40) // 2
    draw.rounded_rectangle([x, 60, x + tw + 40, 120], 30, fill=RED)
    draw.text((x + 20, 75), label, font=f(FONT_BOLD, SZ_TAG + 4), fill=WHITE)

    # 顶部装饰: 两个徽章(替代 emoji)
    badge_circle(draw, MARGIN + 100, 240, 120, "H", GOLD, font_path=FONT_BOLD)
    badge_circle(draw, W - MARGIN - 100, 240, 120, "★", RED, font_path=FONT_BOLD)

    # 大标题
    title_font = f(FONT_BOLD, 92)
    draw.text((MARGIN, 320), "中国酒店品牌", font=title_font, fill=DARK)
    draw.text((MARGIN, 420), "市场指数地图", font=title_font, fill=DARK)
    draw.text((MARGIN, 540), "2026 H2 实时版", font=f(FONT_BOLD, 54), fill=RED)

    # 3 张独立卡片(数字带)
    bar_y = 660
    bar_h = 200
    card_w = (W - 2 * MARGIN - 30) // 3
    for i, (num, lbl) in enumerate([("8", "大层级"), ("378", "个品牌"), ("6", "维标签")]):
        x_pos = MARGIN + i * (card_w + 15)
        card(draw, x_pos, bar_y, card_w, bar_h, GOLD, None, 18)
        nf = f(FONT_BOLD, 88)
        bb = draw.textbbox((0, 0), num, font=nf)
        nw = bb[2] - bb[0]
        draw.text((x_pos + (card_w - nw) // 2, bar_y + 18), num, font=nf, fill=WHITE)
        bb = draw.textbbox((0, 0), lbl, font=f(FONT_BOLD, 32))
        lw = bb[2] - bb[0]
        draw.text((x_pos + (card_w - lw) // 2, bar_y + 130), lbl, font=f(FONT_BOLD, 32), fill=WHITE)

    draw.text((MARGIN, 900), "全季 / 亚朵 / 万豪 / 希尔顿 等 240+ 品牌实数据校准",
              font=f(FONT_BOLD, 28), fill=DARK)

    # 3 个卖点(用徽章 + 文字)
    bullet_y = 970
    for i, (mark, title, sub) in enumerate([
        ("1", "万豪 2026-06 正式破万", "全球第一酒店集团"),
        ("2", "全季登顶中国单一品牌", "华住 3,565 家登顶"),
        ("3", "6 维综合标注", "STR+星级+服务+地段+业态"),
    ]):
        y = bullet_y + i * 95
        # 圆圈序号
        draw.ellipse([MARGIN + 20, y, MARGIN + 100, y + 80], fill=GOLD)
        bb = draw.textbbox((0, 0), mark, font=f(FONT_BOLD, 56))
        tw = bb[2] - bb[0]
        draw.text((MARGIN + 60 - tw/2, y + 8), mark, font=f(FONT_BOLD, 56), fill=WHITE)
        draw.text((MARGIN + 125, y + 10), title, font=f(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 125, y + 50), sub, font=f(FONT_REG, 24), fill=GRAY)

    # CTA
    draw.rounded_rectangle([MARGIN, 1280, W - MARGIN, 1340], 30, fill=DARK)
    draw.text((MARGIN + 40, 1290), "完整榜单  ↓  ↓  ↓", font=f(FONT_BOLD, 32), fill=WHITE)
    draw.text((W - MARGIN - 30, 1290), "12 图", font=f(FONT_BOLD, 28), fill=GOLD, anchor='rt')

    add_footer(draw, 1, TOTAL)
    img.save(os.path.join(OUTPUT_DIR, "01_封面.png"), 'PNG', quality=95)


# ============== Page 02 导览 ==============
def page_02_nav():
    img, draw = new_canvas()
    bg_pattern(draw)
    header_strip(draw, "CONTENTS · 本期导览", GOLD)

    # 顶部徽章(替代 📑)
    badge_circle(draw, MARGIN + 80, 240, 100, "≡", GOLD)

    bb = draw.textbbox((0, 0), "今天讲什么？", font=f(FONT_BOLD, 72))
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, 300), "今天讲什么？", font=f(FONT_BOLD, 72), fill=DARK)

    items = [
        ("01", "封面 + 导览", GOLD),
        ("02", "奢华层 · ADR 2000+", RED),
        ("03", "高端层 · ADR 800-2000", RED),
        ("04", "中高端 · ADR 450-800", RED),
        ("05", "中端 · ADR 250-450", RED),
        ("06", "经济型 · ADR 100-250", RED),
        ("07", "生活方式", RED),
        ("08", "度假酒店", RED),
        ("09", "服务式公寓", RED),
        ("10", "2025 行业并购", GREEN),
        ("11", "业主端选品矩阵", GREEN),
        ("12", "结尾 + 收藏", GOLD),
    ]

    item_y = 440
    for num, title, color in items:
        draw.rounded_rectangle([MARGIN, item_y, MARGIN + 65, item_y + 60], 12, fill=color)
        draw.text((MARGIN + 16, item_y + 14), num, font=f(FONT_BOLD, 30), fill=WHITE)
        draw.text((MARGIN + 85, item_y + 12), title, font=f(FONT_BOLD, 30), fill=DARK)
        item_y += 72

    add_footer(draw, 2, TOTAL)
    img.save(os.path.join(OUTPUT_DIR, "02_导览.png"), 'PNG', quality=95)


# ============== 通用层级页模板 ==============
def tier_page(page_no, header_text, color, badge_char, title, subtitle, brands, insight_title, insight_text):
    img, draw = new_canvas()
    bg_pattern(draw)
    header_strip(draw, header_text, color)

    # 顶部徽章(用 ASCII 安全字符)
    badge_circle(draw, MARGIN + 80, 240, 110, badge_char, color, font_path=FONT_BOLD)

    # 标题(左移避开徽章)
    bb = draw.textbbox((0, 0), title, font=f(FONT_BOLD, 64))
    tw = bb[2] - bb[0]
    title_x = MARGIN + 200
    draw.text((title_x, 310), title, font=f(FONT_BOLD, 64), fill=DARK)
    # 副标题左对齐
    bb = draw.textbbox((0, 0), subtitle, font=f(FONT_REG, 26))
    draw.text((title_x, 400), subtitle, font=f(FONT_REG, 26), fill=GRAY)

    card_y = 470
    for rank, name, parent, mbi, grade, mark in brands:
        card(draw, MARGIN, card_y, W - 2 * MARGIN, 130, CARD_BG, color, 16)
        # 排名圆
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=color)
        draw.text((MARGIN + 38, card_y + 38), rank, font=f(FONT_BOLD, 60), fill=WHITE)
        # 名称
        draw.text((MARGIN + 130, card_y + 25), name, font=f(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 130, card_y + 70), parent, font=f(FONT_REG, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 100), f"MBI {mbi}  ·  {grade}", font=f(FONT_BOLD, 22), fill=color)
        # 右侧装饰符号
        cx, cy = W - MARGIN - 70, card_y + 65
        if mark == "★":
            big_star(draw, cx, cy, 40, color)
        elif mark == "✓":
            check_mark(draw, cx, cy, 60, color)
        elif mark == "◆":
            draw.polygon([(cx, cy - 30), (cx + 28, cy), (cx, cy + 30), (cx - 28, cy)], fill=color)
        elif mark == "✦":
            draw.line([(cx, cy - 30), (cx, cy + 30)], fill=color, width=4)
            draw.line([(cx - 30, cy), (cx + 30, cy)], fill=color, width=4)
        card_y += 140

    # 洞察底栏
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=color)
    draw.text((MARGIN + 25, 1235), insight_title, font=f(FONT_BOLD, 28), fill=WHITE)
    draw.text((MARGIN + 25, 1272), insight_text, font=f(FONT_REG, 22), fill=WHITE)

    add_footer(draw, page_no, TOTAL)
    img.save(os.path.join(OUTPUT_DIR, f"{page_no:02d}_{title.split(' ')[0]}.png"), 'PNG', quality=95)


# ============== 各层级页 ==============
def page_03():
    tier_page(3, "LUXURY · 奢华层", RED, "①", "奢华层 TOP 5",
              "ADR 2,000+ 元  ·  全服务  ·  不开放加盟",
              [("1", "丽思卡尔顿 Ritz-Carlton", "万豪", "98", "S 标杆", "★"),
               ("2", "四季 Four Seasons", "四季(独立)", "97", "S 标杆", "★"),
               ("3", "宝格丽 Bvlgari", "万豪+LVMH", "96", "S 标杆", "◆"),
               ("4", "安缦 Aman", "独立", "95", "S 标杆", "✦"),
               ("5", "嘉佩乐 Capella", "独立", "93", "S 标杆", "✓")],
              "★ 奢华层全部不开放加盟", "业主只能带物业找集团谈管理合同 · GOP 8-15%")


def page_04():
    tier_page(4, "UPSCALE · 高端层", GREEN, "②", "高端层 TOP 5",
              "ADR 800-2,000 元  ·  万豪 2026-06 破万",
              [("1", "JW 万豪", "万豪 (10,000 家)", "94", "S · 89 分", "★"),
               ("2", "希尔顿 Hilton", "希尔顿 (9,200+ 家)", "92", "S · 88 分", "★"),
               ("3", "君悦 Grand Hyatt", "凯悦 (1,528 家)", "88", "A · 84 分", "◆"),
               ("4", "凯悦 Hyatt Regency", "凯悦", "90", "S · 87 分", "✦"),
               ("5", "洲际 InterContinental", "IHG (6,963 家)", "89", "S · 85 分", "✓")],
              "★ 国际 5 星标杆组合", "万豪 30+ / 希尔顿 24 / IHG 20 / 凯悦 20+ 品牌")


def page_05():
    tier_page(5, "UPPER MIDSCALE · 中高端", RED, "③", "中高端 TOP 5",
              "ADR 450-800 元  ·  亚朵系 = 中国 lifestyle 独苗",
              [("1", "亚朵 Atour (2,015 家)", "亚朵 NASDAQ:ATAT", "94", "S · 95 分 冠军", "★"),
               ("2", "亚朵 S Atour S", "亚朵", "88", "S · 92 分", "◆"),
               ("3", "希尔顿欢朋 Hampton", "希尔顿 (锦江运营)", "93", "S · 91 分", "✦"),
               ("4", "智选假日 HIEX", "IHG (6,963 家)", "91", "S · 89 分", "✓"),
               ("5", "全季 Ji Hotel (3,565)", "华住 (13,215 家)", "92", "S · 93 分", "✓")],
              "★ 亚朵 = 中国唯一 lifestyle 标杆", "2025 营收 97.9 亿 +35.1% · 净利 17.5 亿 +34.2%")


def page_06():
    tier_page(6, "MIDSCALE · 中端层", GOLD, "④", "中端层 TOP 5",
              "ADR 250-450 元  ·  中国酒店主战场",
              [("1", "全季 Ji Hotel (3,565)", "华住 · 中国第一", "93", "S · 94 分 冠军", "★"),
               ("2", "维也纳 Vienna (2,000+)", "锦江 (铂涛)", "88", "A · 87 分", "◆"),
               ("3", "亚朵轻居 Atour Light", "亚朵", "85", "A · 88 分", "✦"),
               ("4", "桔子 Orange", "华住", "85", "A · 87 分", "✓"),
               ("5", "喆啡 James Joyce (610+)", "锦江 · 迈点 TOP1 lifestyle", "85", "A · 86 分", "✓")],
              "★ 全季已超汉庭 登顶单一品牌冠军", "HOTELS Magazine 2025 + 华住 2025 年报双向验证")


def page_07():
    tier_page(7, "ECONOMY · 经济型", GREEN, "⑤", "经济型层 TOP 5",
              "ADR 100-250 元  ·  中国酒店基础盘",
              [("1", "汉庭 3.51 / 4.0", "华住 (13,215 家)", "93", "S · 88 分 长期冠军", "★"),
               ("2", "如家 4.0", "首旅 (7,802 家)", "90", "S · 87 分", "◆"),
               ("3", "7 天 3.0", "锦江 (14,132 家)", "88", "S · 86 分", "✦"),
               ("4", "锦江之星 (5,161)", "锦江", "85", "A · 84 分", "✓"),
               ("5", "尚客优 (2,548)", "尚美数智 · 下沉之王", "84", "A · 84 分", "✓")],
              "★ TOP 3 占行业规模 50%+", "下沉首选：尚客优/城市便捷/柏曼/骏怡(东呈业绩对赌唯一)")


def page_08():
    tier_page(8, "LIFESTYLE · 生活方式", GOLD, "⑥", "生活方式 TOP 5",
              "主题 + 文化 + 客户认同  ·  加盟 80%+",
              [("1", "亚朵 Atour (2,015-2,088)", "亚朵", "94", "S · 95 分 冠军", "★"),
               ("2", "喆啡 James Joyce", "锦江 (在营 610+)", "85", "A · 86 分 迈点 TOP1", "◆"),
               ("3", "桔子水晶 Crystal Orange", "华住", "86", "S · 89 分", "✦"),
               ("4", "亚朵 S Atour S", "亚朵", "88", "S · 92 分", "✓"),
               ("5", "希岸 Xana", "锦江", "80", "A · 82 分", "✓")],
              "★ 生活方式 = 经营哲学", "三件套：单一文化锚点 + 故事化空间 + 客户价值认同")


def page_09():
    tier_page(9, "RESORT · 度假层", GREEN, "⑦", "度假层 TOP 5",
              "ADR 800-3,000+ 元  ·  2026 拐点：体验型崛起",
              [("1", "安缦 Aman", "独立", "95", "S · 90 分 仍居 TOP", "★"),
               ("2", "Club Med", "地中海俱乐部 (复星)", "92", "S · 91 分 一价全包+亲子", "◆"),
               ("3", "悦榕庄 Banyan Tree", "悦榕集团", "90", "S · 88 分 增速放缓", "✦"),
               ("4", "瑰丽 Rosewood", "新世界 (郑志刚)", "92", "S · 88 分", "✓"),
               ("5", "嘉佩乐 Capella", "独立", "93", "S · 87 分", "✓")],
              "2026 拐点：体验型崛起", "安缦/悦榕庄情怀祛魅 · Club Med 一价全包逆势")


def page_10():
    tier_page(10, "APARTMENT · 服务式公寓", RED, "⑧", "公寓层 TOP 5",
              "长住市场  ·  雅诗阁中国 110 家 / 20,000+ 公寓",
              [("1", "雅诗阁 Ascott", "凯德雅诗阁 (新加坡)", "92", "S · 90 分", "★"),
               ("2", "万豪行政公寓 ExRes", "万豪", "88", "A · 85 分", "◆"),
               ("3", "盛捷 Somerset", "凯德雅诗阁", "84", "A · 85 分", "✦"),
               ("4", "馨乐庭 Citadines", "凯德雅诗阁", "82", "A · 84 分", "✓"),
               ("5", "辉盛坊 Fraser Suites", "Frasers (新加坡)", "82", "A · 82 分", "✓")],
              "★ 凯德 + 万豪 + Frasers 三足鼎立", "中国本土性价比品牌正在崛起 (瑰悦/恺信/优帕克)")


# ============== Page 11 行业并购 ==============
def page_11_ma():
    img, draw = new_canvas()
    bg_pattern(draw)
    header_strip(draw, "2025 三大并购事件", RED)
    badge_circle(draw, MARGIN + 80, 240, 110, "$", RED, font_path=FONT_BOLD)

    bb = draw.textbbox((0, 0), "2025 行业剧变", font=f(FONT_BOLD, 70))
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, 310), "2025 行业剧变", font=f(FONT_BOLD, 70), fill=DARK)
    bb = draw.textbbox((0, 0), "三大并购改变中国酒店业格局", font=f(FONT_REG, 26))
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, 400), "三大并购改变中国酒店业格局", font=f(FONT_REG, 26), fill=GRAY)

    events = [
        ("1", "同程旅行收购万达酒管", "2025-10-17  ·  24.9 亿元",
         "万达 9 大品牌 + 250+ 门店 + 400+ 筹建 并入同程 · 10/20 年不竞争协议"),
        ("2", "中旅酒店战略投资雅阁", "2025-06  ·  战略入股",
         "中旅品牌矩阵扩展至 13+ 雅阁系 · 首次跻身全球 50 强"),
        ("3", "凯悦完成收购 Playa", "2025-06-17  ·  全包度假",
         "凯悦总门店从 1,300 → 1,528 · Inclusive Collection 9 品牌矩阵"),
    ]

    card_y = 480
    for rank, title, when, desc in events:
        card(draw, MARGIN, card_y, W - 2 * MARGIN, 220, CARD_BG, RED, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=RED)
        draw.text((MARGIN + 40, card_y + 32), rank, font=f(FONT_BOLD, 56), fill=WHITE)
        draw.text((MARGIN + 130, card_y + 22), title, font=f(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 130, card_y + 68), when, font=f(FONT_BOLD, 24), fill=RED)
        draw.text((MARGIN + 130, card_y + 110), desc, font=f(FONT_REG, 22), fill=GRAY)
        # 右侧装饰币符号
        cx, cy = W - MARGIN - 80, card_y + 110
        draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], outline=RED, width=5)
        draw.text((cx - 12, cy - 22), "¥", font=f(FONT_BOLD, 40), fill=RED)
        card_y += 240

    add_footer(draw, 11, TOTAL)
    img.save(os.path.join(OUTPUT_DIR, "11_行业并购.png"), 'PNG', quality=95)


# ============== Page 12 CTA ==============
def page_12_cta():
    img, draw = new_canvas()
    bg_pattern(draw)
    draw.rectangle([0, 0, W, 16], fill=GOLD)

    badge_circle(draw, MARGIN + 80, 220, 110, "★", GOLD, font_path=FONT_BOLD)
    draw.text((MARGIN, 260), "完整版桌面文档", font=f(FONT_BOLD, 80), fill=DARK)
    draw.text((MARGIN, 360), "免费下载", font=f(FONT_BOLD, 80), fill=RED)

    desc_lines = [
        "① 8 大层级 × 最多 50 品牌 = 378 个条目",
        "② 6 维综合标注 (STR / 星级 / 规模 / 服务 / 地段 / 业态)",
        "③ 全球 TOP 13 + 中国 TOP 10 集团规模对照",
        "④ 加盟费 / 管理费 / 单房造价 / 综合价值全维度",
        "⑤ R66 数据校准 + 信源矩阵标注",
    ]
    for i, line in enumerate(desc_lines):
        draw.text((MARGIN + 30, 500 + i * 56), line, font=f(FONT_BOLD, 30), fill=DARK)

    card_y = 820
    card(draw, MARGIN, card_y, W - 2 * MARGIN, 160, DARK, None, 20)
    draw.rounded_rectangle([MARGIN + 30, card_y + 25, MARGIN + 110, card_y + 105], 18, fill=GOLD)
    draw.text((MARGIN + 50, card_y + 38), "DOCX", font=f(FONT_BOLD, 22), fill=DARK)
    draw.text((MARGIN + 130, card_y + 30), "酒店品牌市场指数综合排名", font=f(FONT_BOLD, 32), fill=WHITE)
    draw.text((MARGIN + 130, card_y + 80), "_2026H2_v3.0_2026-08-20.docx", font=f(FONT_REG, 24), fill=(220, 200, 175))
    draw.text((MARGIN + 130, card_y + 120), "桌面路径 C:\\Users\\ericz\\Desktop\\", font=f(FONT_REG, 22), fill=(180, 165, 140))

    btn_y = 1020
    draw.rounded_rectangle([MARGIN, btn_y, W - MARGIN, btn_y + 110], 50, fill=GOLD)
    draw.text((MARGIN + 70, btn_y + 28), "点赞 + 收藏 + 转发", font=f(FONT_BOLD, 36), fill=WHITE)
    draw.text((MARGIN + 70, btn_y + 75), "下期讲：6 维标签完整解释 + 业主端选品矩阵", font=f(FONT_REG, 22), fill=(255, 250, 235))

    contact_y = 1180
    draw.text((MARGIN, contact_y), "关注我：B166ER 出品", font=f(FONT_BOLD, 32), fill=DARK)
    draw.text((MARGIN, contact_y + 50), "ERIC的B166ER · 酒店行业地图系列", font=f(FONT_REG, 24), fill=GRAY)
    draw.text((MARGIN, contact_y + 90), "更新频率：每周 1-2 期深度报告", font=f(FONT_REG, 24), fill=GRAY)

    add_footer(draw, 12, TOTAL)
    img.save(os.path.join(OUTPUT_DIR, "12_结尾CTA.png"), 'PNG', quality=95)


# ============== 水印 ==============
def add_watermark(filepath, tag="B166ER-20260820"):
    img = Image.open(filepath).convert('RGBA')
    draw = ImageDraw.Draw(img)
    font = f(FONT_BOLD, 14)
    text = f"  {tag}  "
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    overlay = Image.new('RGBA', (tw + 16, th + 8), (255, 255, 255, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.rectangle([0, 0, tw + 16, th + 8], fill=(255, 255, 255, 200))
    o_draw.text((8, 0), text, font=font, fill=DARK)
    img.paste(overlay, (W - tw - 32, H - 32), overlay)
    img.convert('RGB').save(filepath, 'PNG', quality=95)


def main():
    pages = [
        page_01_cover,
        page_02_nav,
        page_03,
        page_04,
        page_05,
        page_06,
        page_07,
        page_08,
        page_09,
        page_10,
        page_11_ma,
        page_12_cta,
    ]
    for page_func in pages:
        print(f"生成: {page_func.__name__}")
        page_func()
    print("\n加水印...")
    for f_name in sorted(os.listdir(OUTPUT_DIR)):
        if f_name.endswith('.png'):
            add_watermark(os.path.join(OUTPUT_DIR, f_name))
    print(f"\n完成 {len(pages)} 张图 → {OUTPUT_DIR}")


if __name__ == '__main__':
    main()