#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书范式 · 酒店品牌市场指数综合排名
12 张图卡片 · 1080x1440 (3:4) · 移动端优先
v2.0: emoji 用 Segoe UI Emoji 渲染 + 数字带重排
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
LIGHT_GOLD = (210, 165, 90)

# 字体
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_HEAVY = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
FONT_EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"  # Segoe UI Emoji

# 字体大小
SZ_TITLE = 84
SZ_SUBTITLE = 48
SZ_HEADING = 60
SZ_BODY = 36
SZ_BODY_SM = 30
SZ_CAPTION = 26
SZ_TAG = 28
SZ_NUM_BIG = 88
SZ_NUM_MED = 64
SZ_FOOTER = 22
SZ_emoji_lg = 64
SZ_emoji_md = 48
SZ_emoji_sm = 36


def load_font(path, size):
    return ImageFont.truetype(path, size)


def new_canvas(bg=BG):
    img = Image.new('RGB', (W, H), bg)
    return img, ImageDraw.Draw(img)


def add_bg_pattern(draw):
    for i in range(0, W, 90):
        for j in range(0, H, 90):
            if (i + j) % 180 == 0:
                draw.ellipse([i, j, i+8, j+8], fill=(245, 235, 220))


def draw_text_xy(draw, x, y, text, font, color, anchor='lt'):
    draw.text((x, y), text, font=font, fill=color, anchor=anchor)


def draw_centered(draw, text, y, font, color=DARK, x_off=0):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2 - x_off
    draw.text((x, y), text, font=font, fill=color)


def add_footer(draw, page_num, total_pages):
    draw.line([(MARGIN, H - 130), (W - MARGIN, H - 130)], fill=LINE, width=2)
    draw.text((MARGIN, H - 105), "B166ER 出品", font=load_font(FONT_BOLD, SZ_FOOTER + 2), fill=DARK)
    draw.text((MARGIN, H - 75), "ERIC的B166ER · 酒店行业地图", font=load_font(FONT_REG, SZ_FOOTER - 4), fill=GRAY)
    page_text = f"{page_num:02d} / {total_pages:02d}"
    draw.text((W - MARGIN, H - 90), page_text, font=load_font(FONT_BOLD, SZ_FOOTER + 4), fill=GOLD, anchor='rt')


def add_header_strip(draw, label, color=GOLD):
    bbox = draw.textbbox((0, 0), label, font=load_font(FONT_BOLD, SZ_TAG + 2))
    text_w = bbox[2] - bbox[0]
    x = (W - text_w - 40) // 2
    draw.rounded_rectangle([x, 60, x + text_w + 40, 116], 28, fill=color)
    draw.text((x + 20, 72), label, font=load_font(FONT_BOLD, SZ_TAG + 2), fill=WHITE)


def draw_card(draw, x, y, w, h, bg_color=CARD_BG, border_color=None, radius=20):
    draw.rounded_rectangle([x, y, x+w, y+h], radius, fill=bg_color)
    if border_color:
        draw.rounded_rectangle([x, y, x+w, y+h], radius, outline=border_color, width=2)


TOTAL_PAGES = 12


# ============== Page 01 封面 ==============
def page_01_cover():
    img, draw = new_canvas()
    add_bg_pattern(draw)

    draw.rectangle([0, 0, W, 16], fill=GOLD)

    label = "酒店行业深度报告"
    bbox = draw.textbbox((0, 0), label, font=load_font(FONT_BOLD, SZ_TAG + 4))
    text_w = bbox[2] - bbox[0]
    x = (W - text_w - 40) // 2
    draw.rounded_rectangle([x, 60, x + text_w + 40, 120], 30, fill=RED)
    draw.text((x + 20, 75), label, font=load_font(FONT_BOLD, SZ_TAG + 4), fill=WHITE)

    # emoji 标题组合
    emoji_font = load_font(FONT_EMOJI, 80)
    draw.text((MARGIN + 30, 180), "🏨", font=emoji_font, fill=DARK)
    draw.text((W - MARGIN - 130, 180), "📊", font=emoji_font, fill=DARK)

    title_font = load_font(FONT_HEAVY, 92)
    draw.text((MARGIN, 290), "中国酒店品牌", font=title_font, fill=DARK)
    draw.text((MARGIN, 390), "市场指数地图", font=title_font, fill=DARK)

    subtitle_font = load_font(FONT_BOLD, 54)
    draw.text((MARGIN, 510), "2026 H2 实时版", font=subtitle_font, fill=RED)

    # 数字带 — 重排为 3 张独立卡片
    bar_y = 640
    bar_h = 200
    card_w = (W - 2 * MARGIN - 30) // 3  # 每张卡片宽
    for i, (num, label_text) in enumerate([("8", "大层级"), ("378", "个品牌"), ("6", "维标签")]):
        x_pos = MARGIN + i * (card_w + 15)
        draw_card(draw, x_pos, bar_y, card_w, bar_h, GOLD, None, 18)
        num_font = load_font(FONT_HEAVY, 88)
        # 数字居中
        bbox = draw.textbbox((0, 0), num, font=num_font)
        num_w = bbox[2] - bbox[0]
        draw.text((x_pos + (card_w - num_w) // 2, bar_y + 18), num, font=num_font, fill=WHITE)
        # 标签居中
        bbox = draw.textbbox((0, 0), label_text, font=load_font(FONT_BOLD, 32))
        lab_w = bbox[2] - bbox[0]
        draw.text((x_pos + (card_w - lab_w) // 2, bar_y + 130), label_text, font=load_font(FONT_BOLD, 32), fill=WHITE)

    # 注释
    draw.text((MARGIN, 870), "全季 / 亚朵 / 万豪 / 希尔顿 等 240+ 品牌实数据校准",
              font=load_font(FONT_BOLD, 28), fill=DARK)

    # 卖点三连
    bullet_y = 940
    bullets = [
        ("🎯", "万豪 2026-06 正式破万", "全球第一酒店集团"),
        ("📈", "全季登顶中国单一品牌", "华住 3,565 家登顶"),
        ("🔍", "6 维综合标注", "STR+星级+服务+地段+业态"),
    ]
    for i, (emoji, title, sub) in enumerate(bullets):
        y = bullet_y + i * 100
        draw.text((MARGIN + 20, y), emoji, font=load_font(FONT_EMOJI, 56), fill=DARK)
        draw.text((MARGIN + 110, y + 5), title, font=load_font(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 110, y + 48), sub, font=load_font(FONT_REG, 24), fill=GRAY)

    # 底部 CTA
    draw.rounded_rectangle([MARGIN, 1270, W - MARGIN, 1330], 30, fill=DARK)
    draw.text((MARGIN + 40, 1280), "👇 完整榜单向下滑", font=load_font(FONT_BOLD, 32), fill=WHITE)
    # 右下角装饰三角
    draw.polygon([(W - MARGIN - 60, 1290), (W - MARGIN - 30, 1300), (W - MARGIN - 60, 1310)], fill=WHITE)

    add_footer(draw, 1, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "01_封面.png"), 'PNG', quality=95)


# ============== Page 02 导览 ==============
def page_02_nav():
    img, draw = new_canvas()
    add_bg_pattern(draw)
    add_header_strip(draw, "CONTENTS · 本期导览", color=GOLD)

    draw.text((MARGIN, 170), "📑", font=load_font(FONT_EMOJI, 80), fill=DARK)
    draw.text((MARGIN, 280), "今天讲什么？", font=load_font(FONT_HEAVY, 72), fill=DARK)

    items = [
        ("01", "封面 + 导览", "本图", GOLD),
        ("02", "奢华层 · ADR 2000+", "丽思/四季/宝格丽...", RED),
        ("03", "高端层 · ADR 800-2000", "JW 万豪/希尔顿/凯悦", RED),
        ("04", "中高端 · ADR 450-800", "亚朵系 = 中国 lifestyle 独苗", RED),
        ("05", "中端 · ADR 250-450", "全季已超汉庭登顶冠军", RED),
        ("06", "经济型 · ADR 100-250", "TOP3 = 汉庭+7 天+如家", RED),
        ("07", "生活方式 · 主题+文化", "喆啡/桔子水晶/亚朵", RED),
        ("08", "度假 · 目的地+体验", "安缦/Club Med/悦榕庄", RED),
        ("09", "服务式公寓 · 长住", "雅诗阁/万豪 ExRes/辉盛坊", RED),
        ("10", "2025 三大并购事件", "同程收购万达/中旅入股雅阁", GREEN),
        ("11", "业主端选品矩阵", "决策树", GREEN),
        ("12", "结尾 + 收藏", "完整版桌面文档下载", GOLD),
    ]

    item_y = 410
    for num, title, sub, color in items:
        draw.rounded_rectangle([MARGIN, item_y, MARGIN + 65, item_y + 60], 12, fill=color)
        draw.text((MARGIN + 16, item_y + 14), num, font=load_font(FONT_BOLD, 30), fill=WHITE)
        draw.text((MARGIN + 85, item_y + 8), title, font=load_font(FONT_BOLD, 30), fill=DARK)
        draw.text((MARGIN + 85, item_y + 40), sub, font=load_font(FONT_REG, 22), fill=GRAY)
        item_y += 75

    add_footer(draw, 2, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "02_导览.png"), 'PNG', quality=95)


# ============== 通用层级页 ==============
def page_tier(page_no, header_text, header_color, emoji, title, subtitle, brands, insight_title, insight_desc, insight_bg=DARK):
    img, draw = new_canvas()
    add_bg_pattern(draw)
    add_header_strip(draw, header_text, color=header_color)

    # emoji 居左 + 标题居中 (避免重叠)
    draw.text((MARGIN, 170), emoji, font=load_font(FONT_EMOJI, 80), fill=DARK)
    # 标题文字宽度计算,确保不和 emoji 重叠
    bbox = draw.textbbox((0, 0), title, font=load_font(FONT_HEAVY, 68))
    title_w = bbox[2] - bbox[0]
    draw.text(((W - title_w) // 2, 290), title, font=load_font(FONT_HEAVY, 68), fill=DARK)
    draw.text((MARGIN, 380), subtitle, font=load_font(FONT_REG, 26), fill=GRAY)

    card_y = 450
    for rank, name, parent, mbi, grade, emo in brands:
        draw_card(draw, MARGIN, card_y, W - 2 * MARGIN, 130, CARD_BG, header_color, 16)
        # 排名
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=header_color)
        draw.text((MARGIN + 36, card_y + 36), rank, font=load_font(FONT_HEAVY, 60), fill=WHITE)
        # 名称
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 130, card_y + 70), parent, font=load_font(FONT_REG, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 100), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD, 22), fill=header_color)
        # emoji
        draw.text((W - MARGIN - 90, card_y + 35), emo, font=load_font(FONT_EMOJI, 50), fill=DARK)
        card_y += 140

    # 关键洞察
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=insight_bg)
    draw.text((MARGIN + 25, 1235), insight_title, font=load_font(FONT_BOLD, 28), fill=WHITE)
    draw.text((MARGIN + 25, 1272), insight_desc, font=load_font(FONT_REG, 22), fill=(220, 200, 175))

    add_footer(draw, page_no, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, f"{page_no:02d}_{title.split(' ')[0]}.png"), 'PNG', quality=95)


# ============== Page 03 奢华层 ==============
def page_03_luxury():
    page_tier(
        page_no=3,
        header_text="LUXURY · 奢华层",
        header_color=RED,
        emoji="👑",
        title="奢华层 TOP 5",
        subtitle="ADR 2,000+ 元  ·  全服务  ·  全不开放加盟",
        brands=[
            ("1", "丽思卡尔顿 Ritz-Carlton", "万豪", "98", "S 标杆", "★"),
            ("2", "四季 Four Seasons", "四季(独立)", "97", "S 标杆", "★"),
            ("3", "宝格丽 Bvlgari", "万豪+LVMH", "96", "S 标杆", "✓"),
            ("4", "安缦 Aman", "独立", "95", "S 标杆", "✓"),
            ("5", "嘉佩乐 Capella", "独立", "93", "S 标杆", "✓"),
        ],
        insight_title="💡 奢华层全部不开放加盟",
        insight_desc="业主只能带物业找集团谈管理合同 · GOP 8-15%",
    )


# ============== Page 04 高端层 ==============
def page_04_highend():
    page_tier(
        page_no=4,
        header_text="UPSCALE · 高端层",
        header_color=GREEN,
        emoji="🌆",
        title="高端层 TOP 5",
        subtitle="ADR 800-2,000 元  ·  万豪 2026-06 破万",
        brands=[
            ("1", "JW 万豪", "万豪 (10,000 家)", "94", "S · 89 分", "★"),
            ("2", "希尔顿 Hilton", "希尔顿 (9,200+ 家)", "92", "S · 88 分", "★"),
            ("3", "君悦 Grand Hyatt", "凯悦 (1,528 家)", "88", "A · 84 分", "★"),
            ("4", "凯悦 Hyatt Regency", "凯悦", "90", "S · 87 分", "✓"),
            ("5", "洲际 InterContinental", "IHG (6,963 家)", "89", "S · 85 分", "✓"),
        ],
        insight_title="💡 国际 5 星标杆组合",
        insight_desc="万豪 30+ / 希尔顿 24 / IHG 20 / 凯悦 20+ 品牌",
    )


# ============== Page 05 中高端 ==============
def page_05_upper_mid():
    page_tier(
        page_no=5,
        header_text="UPPER MIDSCALE · 中高端",
        header_color=RED,
        emoji="🎯",
        title="中高端 TOP 5",
        subtitle="ADR 450-800 元  ·  亚朵系 = 中国 lifestyle 独苗",
        brands=[
            ("1", "亚朵 Atour (2,015 家)", "亚朵 NASDAQ:ATAT", "94", "S · 95 分 冠军", "🔥"),
            ("2", "亚朵 S Atour S", "亚朵", "88", "S · 92 分", "✓"),
            ("3", "希尔顿欢朋 Hampton", "希尔顿 (锦江运营)", "93", "S · 91 分", "✓"),
            ("4", "智选假日 HIEX", "IHG (6,963 家)", "91", "S · 89 分", "✓"),
            ("5", "全季 Ji Hotel (3,565)", "华住 (13,215 家)", "92", "S · 93 分", "✓"),
        ],
        insight_title="🔥 亚朵 = 中国唯一 lifestyle 标杆",
        insight_desc="2025 营收 97.9 亿 +35.1% / 净利 17.5 亿 +34.2%",
    )


# ============== Page 06 中端层 ==============
def page_06_midscale():
    page_tier(
        page_no=6,
        header_text="MIDSCALE · 中端层",
        header_color=GOLD,
        emoji="🏆",
        title="中端层 TOP 5",
        subtitle="ADR 250-450 元  ·  中国酒店主战场",
        brands=[
            ("1", "全季 Ji Hotel (3,565)", "华住 · 中国第一", "93", "S · 94 分 冠军", "★"),
            ("2", "维也纳 Vienna (2,000+)", "锦江 (铂涛)", "88", "A · 87 分", "✓"),
            ("3", "亚朵轻居 Atour Light", "亚朵", "85", "A · 88 分", "☕"),
            ("4", "桔子 Orange", "华住", "85", "A · 87 分", "☕"),
            ("5", "喆啡 James Joyce (610+)", "锦江 (铂涛) · 迈点 TOP1 lifestyle", "85", "A · 86 分", "☕"),
        ],
        insight_title="🔥 全季已超汉庭 登顶单一品牌冠军",
        insight_desc="HOTELS Magazine 2025 + 华住 2025 年报双向验证",
        insight_bg=GOLD,
    )


# ============== Page 07 经济型 ==============
def page_07_economy():
    page_tier(
        page_no=7,
        header_text="ECONOMY · 经济型",
        header_color=GREEN,
        emoji="💰",
        title="经济型层 TOP 5",
        subtitle="ADR 100-250 元  ·  中国酒店基础盘",
        brands=[
            ("1", "汉庭 3.51 / 4.0", "华住 (13,215 家)", "93", "S · 88 分 长期冠军", "★"),
            ("2", "如家 4.0", "首旅 (7,802 家)", "90", "S · 87 分", "★"),
            ("3", "7 天 3.0", "锦江 (14,132 家)", "88", "S · 86 分", "✓"),
            ("4", "锦江之星 (5,161)", "锦江", "85", "A · 84 分", "★"),
            ("5", "尚客优 (2,548)", "尚美数智 · 下沉之王", "84", "A · 84 分", "✓"),
        ],
        insight_title="📊 TOP 3 占行业规模 50%+",
        insight_desc="下沉首选：尚客优/城市便捷/柏曼/骏怡(东呈业绩对赌唯一)",
    )


# ============== Page 08 生活方式 ==============
def page_08_lifestyle():
    page_tier(
        page_no=8,
        header_text="LIFESTYLE · 生活方式",
        header_color=GOLD,
        emoji="☕",
        title="生活方式 TOP 5",
        subtitle="主题 + 文化 + 客户认同  ·  加盟 80%+",
        brands=[
            ("1", "亚朵 Atour (2,015-2,088)", "亚朵", "94", "S · 95 分 冠军", "🔥"),
            ("2", "喆啡 James Joyce", "锦江 (在营 610+)", "85", "A · 86 分 迈点 TOP1", "☕"),
            ("3", "桔子水晶 Crystal Orange", "华住", "86", "S · 89 分", "★"),
            ("4", "亚朵 S Atour S", "亚朵", "88", "S · 92 分", "✓"),
            ("5", "希岸 Xana", "锦江", "80", "A · 82 分", "✓"),
        ],
        insight_title="🎯 生活方式 = 经营哲学",
        insight_desc="三件套：单一文化锚点 + 故事化空间 + 客户价值认同",
        insight_bg=GOLD,
    )


# ============== Page 09 度假层 ==============
def page_09_resort():
    page_tier(
        page_no=9,
        header_text="RESORT · 度假层",
        header_color=GREEN,
        emoji="🏝",
        title="度假层 TOP 5",
        subtitle="ADR 800-3,000+ 元  ·  2026 拐点：体验型崛起",
        brands=[
            ("1", "安缦 Aman", "独立", "95", "S · 90 分 仍居 TOP", "✓"),
            ("2", "Club Med", "地中海俱乐部 (复星)", "92", "S · 91 分 一价全包+亲子", "🌴"),
            ("3", "悦榕庄 Banyan Tree", "悦榕集团", "90", "S · 88 分 增速放缓", "✓"),
            ("4", "瑰丽 Rosewood", "新世界 (郑志刚)", "92", "S · 88 分", "✓"),
            ("5", "嘉佩乐 Capella", "独立", "93", "S · 87 分", "✓"),
        ],
        insight_title="🔥 2026 行业拐点：体验型崛起",
        insight_desc="安缦/悦榕庄情怀祛魅 · Club Med 一价全包逆势",
    )


# ============== Page 10 公寓层 ==============
def page_10_apartment():
    page_tier(
        page_no=10,
        header_text="APARTMENT · 服务式公寓",
        header_color=RED,
        emoji="🏢",
        title="公寓层 TOP 5",
        subtitle="长住市场  ·  雅诗阁中国 110 家 / 20,000+ 公寓",
        brands=[
            ("1", "雅诗阁 Ascott", "凯德雅诗阁 (新加坡)", "92", "S · 90 分", "✓"),
            ("2", "万豪行政公寓 ExRes", "万豪", "88", "A · 85 分", "✓"),
            ("3", "盛捷 Somerset", "凯德雅诗阁", "84", "A · 85 分", "✓"),
            ("4", "馨乐庭 Citadines", "凯德雅诗阁", "82", "A · 84 分", "✓"),
            ("5", "辉盛坊 Fraser Suites", "Frasers (新加坡)", "82", "A · 82 分", "✓"),
        ],
        insight_title="🌐 凯德 + 万豪 + Frasers 三足鼎立",
        insight_desc="中国本土性价比品牌正在崛起 (瑰悦/恺信/优帕克)",
    )


# ============== Page 11 行业并购 ==============
def page_11_ma():
    img, draw = new_canvas()
    add_bg_pattern(draw)
    add_header_strip(draw, "2025 三大并购事件", color=RED)

    draw.text((MARGIN, 170), "💥", font=load_font(FONT_EMOJI, 80), fill=DARK)
    draw.text((MARGIN, 280), "2025 行业剧变", font=load_font(FONT_HEAVY, 70), fill=DARK)
    draw.text((MARGIN, 380), "三大并购改变中国酒店业格局", font=load_font(FONT_REG, 26), fill=GRAY)

    events = [
        ("1", "同程旅行收购万达酒管", "2025-10-17  ·  24.9 亿",
         "万达 9 大品牌 + 250+ 门店 + 400+ 筹建 并入同程 · 10/20 年不竞争协议", "💼"),
        ("2", "中旅酒店战略投资雅阁", "2025-06  ·  战略入股",
         "中旅品牌矩阵扩展至 13+ 雅阁系 · 首次跻身全球 50 强", "🤝"),
        ("3", "凯悦完成收购 Playa", "2025-06-17  ·  全包度假",
         "凯悦总门店从 1,300 → 1,528 · Inclusive Collection 9 品牌矩阵成型", "🌴"),
    ]

    card_y = 460
    for rank, title, when, desc, emo in events:
        draw_card(draw, MARGIN, card_y, W - 2 * MARGIN, 220, CARD_BG, RED, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=RED)
        draw.text((MARGIN + 36, card_y + 36), rank, font=load_font(FONT_HEAVY, 60), fill=WHITE)
        draw.text((MARGIN + 130, card_y + 22), title, font=load_font(FONT_BOLD, 32), fill=DARK)
        draw.text((MARGIN + 130, card_y + 68), when, font=load_font(FONT_BOLD, 24), fill=RED)
        draw.text((MARGIN + 130, card_y + 110), desc, font=load_font(FONT_REG, 22), fill=GRAY)
        draw.text((W - MARGIN - 80, card_y + 50), emo, font=load_font(FONT_EMOJI, 56), fill=DARK)
        card_y += 240

    add_footer(draw, 11, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "11_行业并购.png"), 'PNG', quality=95)


# ============== Page 12 结尾 CTA ==============
def page_12_cta():
    img, draw = new_canvas()
    add_bg_pattern(draw)
    draw.rectangle([0, 0, W, 16], fill=GOLD)

    draw.text((MARGIN, 110), "🎁", font=load_font(FONT_EMOJI, 100), fill=DARK)
    draw.text((MARGIN, 240), "完整版桌面文档", font=load_font(FONT_HEAVY, 80), fill=DARK)
    draw.text((MARGIN, 340), "免费下载", font=load_font(FONT_HEAVY, 80), fill=RED)

    desc_lines = [
        "✅ 8 大层级 × 最多 50 品牌 = 378 个条目",
        "✅ 6 维综合标注 (STR / 星级 / 规模 / 服务 / 地段 / 业态)",
        "✅ 全球 TOP 13 + 中国 TOP 10 集团规模对照",
        "✅ 加盟费 / 管理费 / 单房造价 / 综合价值全维度",
        "✅ R66 数据校准 + 信源矩阵标注",
    ]
    for i, line in enumerate(desc_lines):
        draw.text((MARGIN + 30, 480 + i * 56), line, font=load_font(FONT_BOLD, 30), fill=DARK)

    # 文档卡片
    card_y = 800
    draw.rounded_rectangle([MARGIN, card_y, W - MARGIN, card_y + 160], 20, fill=DARK)
    draw.text((MARGIN + 30, card_y + 22), "📂", font=load_font(FONT_EMOJI, 56), fill=WHITE)
    draw.text((MARGIN + 110, card_y + 25), "酒店品牌市场指数综合排名", font=load_font(FONT_BOLD, 32), fill=WHITE)
    draw.text((MARGIN + 110, card_y + 75), "_2026H2_v3.0_2026-08-20.docx", font=load_font(FONT_REG, 24), fill=(220, 200, 175))
    draw.text((MARGIN + 110, card_y + 115), "桌面路径：C:\\Users\\ericz\\Desktop\\", font=load_font(FONT_REG, 22), fill=(180, 165, 140))

    # CTA 按钮
    btn_y = 1000
    draw.rounded_rectangle([MARGIN, btn_y, W - MARGIN, btn_y + 110], 50, fill=GOLD)
    draw.text((MARGIN + 70, btn_y + 28), "👍 点赞 + ⭐ 收藏 + 🔄 转发", font=load_font(FONT_BOLD, 36), fill=WHITE)
    draw.text((MARGIN + 70, btn_y + 75), "下期讲：6 维标签完整解释 + 业主端选品矩阵", font=load_font(FONT_REG, 22), fill=(255, 250, 235))

    # 关注信息
    contact_y = 1170
    draw.text((MARGIN, contact_y), "📌 关注我：B166ER 出品", font=load_font(FONT_BOLD, 32), fill=DARK)
    draw.text((MARGIN, contact_y + 50), "ERIC的B166ER · 酒店行业地图系列", font=load_font(FONT_REG, 24), fill=GRAY)
    draw.text((MARGIN, contact_y + 90), "更新频率：每周 1-2 期深度报告", font=load_font(FONT_REG, 24), fill=GRAY)

    add_footer(draw, 12, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "12_结尾CTA.png"), 'PNG', quality=95)


# ============== 水印 ==============
def add_watermark(filepath, tag="B166ER-20260820"):
    img = Image.open(filepath)
    draw = ImageDraw.Draw(img)
    font = load_font(FONT_BOLD, 14)
    text = f"  {tag}  "
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 右下角半透明
    overlay = Image.new('RGBA', (tw + 16, th + 8), (255, 255, 255, 0))
    o_draw = ImageDraw.Draw(overlay)
    o_draw.rectangle([0, 0, tw + 16, th + 8], fill=(255, 255, 255, 200))
    o_draw.text((8, 0), text, font=font, fill=(60, 40, 25))
    img_rgba = img.convert('RGBA')
    img_rgba.paste(overlay, (W - tw - 32, H - 32), overlay)
    img_rgba.convert('RGB').save(filepath, 'PNG', quality=95)


def main():
    pages = [
        page_01_cover,
        page_02_nav,
        page_03_luxury,
        page_04_highend,
        page_05_upper_mid,
        page_06_midscale,
        page_07_economy,
        page_08_lifestyle,
        page_09_resort,
        page_10_apartment,
        page_11_ma,
        page_12_cta,
    ]
    for page_func in pages:
        print(f"生成: {page_func.__name__}")
        page_func()

    # 加水印
    print("\n加水印...")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            add_watermark(os.path.join(OUTPUT_DIR, f))

    print(f"\n完成 {len(pages)} 张图")
    print(f"输出路径: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()