#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书范式 · 酒店品牌市场指数综合排名
12 张图卡片 · 1080x1440 (3:4) · 移动端优先
"""
import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter

# ============== 配置 ==============
OUTPUT_DIR = r"C:\Users\ericz\Desktop\小红书_酒店品牌地图"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1440  # 小红书 3:4 标准尺寸
MARGIN = 60

# 配色
BG = (250, 244, 234)        # 暖米色
CARD_BG = (255, 252, 247)   # 卡片背景
DARK = (60, 40, 25)         # 主文字深棕
GOLD = (183, 121, 31)       # 强调金
RED = (200, 16, 46)         # 重要数据红
GREEN = (31, 77, 42)        # 成功绿
GRAY = (130, 110, 90)       # 次要文字
LIGHT_GRAY = (210, 200, 185)
LINE = (220, 200, 175)      # 分隔线

# 字体
FONT_BOLD_PATH = r"C:\Windows\Fonts\msyhbd.ttc"  # 微软雅黑 Bold
FONT_REG_PATH = r"C:\Windows\Fonts\msyh.ttc"      # 微软雅黑 Regular
FONT_HEAVY_PATH = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"  # 思源宋体 Heavy

# 字体大小
SZ_TITLE = 76       # 大标题
SZ_SUBTITLE = 44    # 副标题
SZ_HEADING = 56     # 章节标题
SZ_BODY = 36        # 正文
SZ_BODY_SM = 30     # 小正文
SZ_CAPTION = 26     # 说明文字
SZ_TAG = 28         # 标签
SZ_NUM = 100        # 大数字
SZ_NUM_MED = 64     # 中数字
SZ_FOOTER = 24      # 页脚

# ============== 字体加载 ==============
def load_font(path, size):
    return ImageFont.truetype(path, size)

# ============== 工具函数 ==============

def new_canvas(bg=BG):
    img = Image.new('RGB', (W, H), bg)
    return img, ImageDraw.Draw(img)


def add_bg_pattern(img, draw):
    """添加细微背景纹理"""
    for i in range(0, W, 80):
        for j in range(0, H, 80):
            if (i + j) % 160 == 0:
                draw.ellipse([i, j, i+6, j+6], fill=(245, 235, 220))


def add_header_strip(draw, label, color=GOLD):
    """顶部小标签条"""
    # 计算文字宽度
    bbox = draw.textbbox((0, 0), label, font=load_font(FONT_BOLD_PATH, SZ_TAG))
    text_w = bbox[2] - bbox[0]
    # 居中绘制
    x = (W - text_w - 30) // 2
    draw.rounded_rectangle([x, 60, x + text_w + 30, 110], 25, fill=color)
    draw.text((x + 15, 70), label, font=load_font(FONT_BOLD_PATH, SZ_TAG), fill=(255, 255, 255))


def add_footer(img, draw, page_num, total_pages, extra_text=""):
    """底部页脚"""
    # 分隔线
    draw.line([(MARGIN, H - 130), (W - MARGIN, H - 130)], fill=LINE, width=2)
    # 左侧：账号标识
    draw.text((MARGIN, H - 110), "B166ER 出品", font=load_font(FONT_BOLD_PATH, SZ_FOOTER), fill=DARK)
    draw.text((MARGIN, H - 75), "ERIC的B166ER · 酒店行业地图", font=load_font(FONT_REG_PATH, SZ_FOOTER - 4), fill=GRAY)
    # 右侧：页码
    page_text = f"{page_num:02d} / {total_pages:02d}"
    bbox = draw.textbbox((0, 0), page_text, font=load_font(FONT_BOLD_PATH, SZ_FOOTER + 4), anchor='rt')
    draw.text((W - MARGIN, H - 100), page_text, font=load_font(FONT_BOLD_PATH, SZ_FOOTER + 4), fill=GOLD, anchor='rt')
    if extra_text:
        draw.text((W - MARGIN, H - 70), extra_text, font=load_font(FONT_REG_PATH, SZ_FOOTER - 4), fill=GRAY, anchor='rt')


def draw_card(draw, x, y, w, h, bg_color=CARD_BG, border_color=None, radius=20):
    """绘制圆角卡片"""
    draw.rounded_rectangle([x, y, x+w, y+h], radius, fill=bg_color)
    if border_color:
        draw.rounded_rectangle([x, y, x+w, y+h], radius, outline=border_color, width=2)


def draw_text_centered(draw, text, y, font, color=DARK, w_offset=0):
    """居中绘制文字"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2 - w_offset
    draw.text((x, y), text, font=font, fill=color)


def wrap_text(draw, text, font, max_width):
    """文字换行"""
    words = text
    lines = []
    current = ""
    for char in words:
        bbox = draw.textbbox((0, 0), current + char, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = char
        else:
            current += char
    if current:
        lines.append(current)
    return lines


# ============== 各页 ==============

TOTAL_PAGES = 12

def page_01_cover():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)

    # 顶部装饰条
    draw.rectangle([0, 0, W, 16], fill=GOLD)
    # 顶部小标签
    label = "酒店行业深度报告"
    bbox = draw.textbbox((0, 0), label, font=load_font(FONT_BOLD_PATH, SZ_TAG + 4))
    text_w = bbox[2] - bbox[0]
    x = (W - text_w - 40) // 2
    draw.rounded_rectangle([x, 60, x + text_w + 40, 116], 28, fill=RED)
    draw.text((x + 20, 70), label, font=load_font(FONT_BOLD_PATH, SZ_TAG + 4), fill=(255, 255, 255))

    # 顶部 emoji
    draw.text((MARGIN + 50, 170), "🏨", font=load_font(FONT_BOLD_PATH, 110))
    draw.text((W - MARGIN - 160, 170), "📊", font=load_font(FONT_BOLD_PATH, 110))

    # 主标题
    title_font = load_font(FONT_HEAVY_PATH, 92)
    draw.text((MARGIN, 300), "中国酒店品牌", font=title_font, fill=DARK)
    draw.text((MARGIN, 400), "市场指数地图", font=title_font, fill=DARK)

    # 副标题(强调)
    subtitle_font = load_font(FONT_BOLD_PATH, 56)
    draw.text((MARGIN, 520), "2026 H2 实时版", font=subtitle_font, fill=RED)

    # 关键数字带
    # 数字条
    bar_y = 620
    bar_h = 220
    draw.rounded_rectangle([MARGIN, bar_y, W - MARGIN, bar_y + bar_h], 25, fill=GOLD)
    # 数字
    draw.text((MARGIN + 40, bar_y + 25), "8", font=load_font(FONT_HEAVY_PATH, 110), fill=(255, 255, 255))
    draw.text((MARGIN + 130, bar_y + 50), "大层级", font=load_font(FONT_BOLD_PATH, 32), fill=(255, 255, 255))
    draw.text((MARGIN + 260, bar_y + 25), "378", font=load_font(FONT_HEAVY_PATH, 110), fill=(255, 255, 255))
    draw.text((MARGIN + 460, bar_y + 50), "个品牌", font=load_font(FONT_BOLD_PATH, 32), fill=(255, 255, 255))
    draw.text((MARGIN + 590, bar_y + 25), "6", font=load_font(FONT_HEAVY_PATH, 110), fill=(255, 255, 255))
    draw.text((MARGIN + 690, bar_y + 50), "维标签", font=load_font(FONT_BOLD_PATH, 32), fill=(255, 255, 255))

    draw.text((MARGIN + 40, bar_y + 130), "全季 / 亚朵 / 万豪 / 希尔顿 等 240+ 品牌实数据校准", font=load_font(FONT_REG_PATH, 26), fill=(255, 255, 255))

    # 卖点三连
    bullet_y = 900
    bullets = [
        ("🎯", "万豪 2026-06 正式破万", "全球第一酒店集团"),
        ("📈", "全季登顶中国单一品牌", "华住 3,565 家登顶"),
        ("🔍", "6 维综合标注", "STR+星级+服务+地段+业态"),
    ]
    for i, (emoji, title, sub) in enumerate(bullets):
        y = bullet_y + i * 130
        draw.text((MARGIN + 20, y), emoji, font=load_font(FONT_BOLD_PATH, 60))
        draw.text((MARGIN + 110, y), title, font=load_font(FONT_BOLD_PATH, 36), fill=DARK)
        draw.text((MARGIN + 110, y + 50), sub, font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    # 底部 CTA
    draw.rounded_rectangle([MARGIN, 1280, W - MARGIN, 1340], 30, fill=DARK)
    draw.text((MARGIN + 60, 1290), "👇 完整榜单向下滑", font=load_font(FONT_BOLD_PATH, 34), fill=(255, 255, 255))
    draw.text((W - MARGIN - 30, 1295), "⤵", font=load_font(FONT_BOLD_PATH, 36), fill=(255, 255, 255), anchor='rt')

    add_footer(img, draw, 1, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "01_封面.png"), 'PNG', quality=95)


def page_02_nav():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "CONTENTS · 本期导览", color=GOLD)

    # 大标题
    draw.text((MARGIN, 150), "📑", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "今天讲什么？", font=load_font(FONT_HEAVY_PATH, 72), fill=DARK)

    # 目录列表
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

    item_y = 380
    for num, title, sub, color in items:
        # 序号
        draw.rounded_rectangle([MARGIN, item_y, MARGIN + 60, item_y + 60], 12, fill=color)
        draw.text((MARGIN + 12, item_y + 12), num, font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
        # 标题
        draw.text((MARGIN + 80, item_y + 5), title, font=load_font(FONT_BOLD_PATH, 30), fill=DARK)
        # 副标题
        draw.text((MARGIN + 80, item_y + 38), sub, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        item_y += 75

    add_footer(img, draw, 2, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "02_导览.png"), 'PNG', quality=95)


def page_03_luxury():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "LUXURY · 奢华层", color=RED)

    # 大标题
    draw.text((MARGIN, 150), "👑", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "奢华层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)

    # 副标题
    draw.text((MARGIN, 360), "ADR 2,000+ 元  ·  全服务  ·  全不开放加盟", font=load_font(FONT_REG_PATH, 28), fill=GRAY)

    # 5 大品牌卡片
    brands = [
        ("1", "丽思卡尔顿 Ritz-Carlton", "万豪", "98", "S 标杆"),
        ("2", "四季 Four Seasons", "四季(独立)", "97", "S 标杆 · 综合价值 95 第一"),
        ("3", "宝格丽 Bvlgari", "万豪+LVMH", "96", "S 标杆"),
        ("4", "安缦 Aman", "独立", "95", "S 标杆 · 业主投资制"),
        ("5", "嘉佩乐 Capella", "独立", "93", "S 标杆"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GOLD, 16)
        # 排名
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GOLD)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        # 名称
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 36), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 24), fill=GRAY)
        # MBI
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 24), fill=RED)
        # 大皇冠
        draw.text((W - MARGIN - 80, card_y + 35), "🏆", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    # 关键洞察底栏
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "💡 关键洞察：奢华层全部不开放加盟", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "业主只能带物业找集团开发部谈管理合同 · GOP 8-15%", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 3, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "03_奢华层.png"), 'PNG', quality=95)


def page_04_highend():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "UPSCALE · 高端层", color=GREEN)

    # 大标题
    draw.text((MARGIN, 150), "🌆", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "高端层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "ADR 800-2,000 元  ·  万豪 2026-06 破万", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "JW 万豪", "万豪 (10,000 家)", "94", "S · 89 分"),
        ("2", "希尔顿 Hilton", "希尔顿 (9,200+ 家)", "92", "S · 88 分"),
        ("3", "君悦 Grand Hyatt", "凯悦 (1,528 家)", "88", "A · 84 分"),
        ("4", "凯悦 Hyatt Regency", "凯悦", "90", "S · 87 分"),
        ("5", "洲际 InterContinental", "IHG (6,963 家)", "89", "S · 85 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GREEN, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GREEN)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 36), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 24), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 24), fill=GREEN)
        draw.text((W - MARGIN - 80, card_y + 35), "🥇", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    # 关键洞察
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "💡 国际 5 星标杆组合", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "万豪 30+ / 希尔顿 24 / IHG 20 / 凯悦 20+ 品牌", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 4, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "04_高端层.png"), 'PNG', quality=95)


def page_05_upper_mid():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "UPPER MIDSCALE · 中高端", color=RED)

    draw.text((MARGIN, 150), "🎯", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "中高端 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "ADR 450-800 元  ·  亚朵系 = 中国 lifestyle 独苗", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "亚朵 Atour (2,015 家)", "亚朵 NASDAQ:ATAT", "94", "S · 95 分 冠军"),
        ("2", "亚朵 S Atour S", "亚朵", "88", "S · 92 分"),
        ("3", "希尔顿欢朋 Hampton", "希尔顿 (锦江运营)", "93", "S · 91 分"),
        ("4", "智选假日 HIEX", "IHG (6,963 家)", "91", "S · 89 分"),
        ("5", "全季 Ji Hotel (3,565)", "华住 (13,215 家)", "92", "S · 93 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, RED, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=RED)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 24), fill=RED)
        draw.text((W - MARGIN - 80, card_y + 35), "🔥", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    # 亚朵深度卡(占两行空间)
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=RED)
    draw.text((MARGIN + 30, 1235), "🔥 亚朵 = 中国唯一 lifestyle 标杆", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "2025 营收 97.9 亿 +35.1% / 净利 17.5 亿 +34.2% / 零售 36.7 亿", font=load_font(FONT_REG_PATH, 20), fill=(255, 235, 230))

    add_footer(img, draw, 5, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "05_中高端.png"), 'PNG', quality=95)


def page_06_midscale():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "MIDSCALE · 中端层", color=GOLD)

    draw.text((MARGIN, 150), "🏆", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "中端层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "ADR 250-450 元  ·  中国酒店主战场", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "全季 Ji Hotel (3,565)", "华住 · 中国第一", "93", "S · 94 分 冠军"),
        ("2", "维也纳 Vienna (2,000+)", "锦江 (铂涛)", "88", "A · 87 分"),
        ("3", "亚朵轻居 Atour Light", "亚朵", "85", "A · 88 分"),
        ("4", "桔子 Orange", "华住", "85", "A · 87 分"),
        ("5", "喆啡 James Joyce (610+)", "锦江 (铂涛)", "85", "A · 86 分 迈点 TOP1 lifestyle"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GOLD, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GOLD)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 22), fill=GOLD)
        draw.text((W - MARGIN - 80, card_y + 35), "⭐", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    # 关键洞察
    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=GOLD)
    draw.text((MARGIN + 30, 1235), "⚡ 全季已超汉庭 登顶中国单一品牌冠军", font=load_font(FONT_BOLD_PATH, 28), fill=DARK)
    draw.text((MARGIN + 30, 1272), "HOTELS Magazine 2025 + 华住 2025 年报双向验证", font=load_font(FONT_REG_PATH, 20), fill=(60, 40, 25))

    add_footer(img, draw, 6, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "06_中端层.png"), 'PNG', quality=95)


def page_07_economy():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "ECONOMY · 经济型", color=GREEN)

    draw.text((MARGIN, 150), "💰", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "经济型层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "ADR 100-250 元  ·  中国酒店基础盘", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "汉庭 3.51 / 4.0", "华住 (13,215 家)", "93", "S · 88 分 长期冠军"),
        ("2", "如家 4.0", "首旅 (7,802 家)", "90", "S · 87 分"),
        ("3", "7 天 3.0", "锦江 (14,132 家)", "88", "S · 86 分"),
        ("4", "锦江之星 (5,161)", "锦江", "85", "A · 84 分"),
        ("5", "尚客优 (2,548)", "尚美数智 · 下沉之王", "84", "A · 84 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GREEN, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GREEN)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 22), fill=GREEN)
        draw.text((W - MARGIN - 80, card_y + 35), "💵", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "📊 TOP 3 占行业规模 50%+", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "下沉首选：尚客优/城市便捷/柏曼/骏怡(东呈业绩对赌唯一)", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 7, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "07_经济型.png"), 'PNG', quality=95)


def page_08_lifestyle():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "LIFESTYLE · 生活方式", color=GOLD)

    draw.text((MARGIN, 150), "☕", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "生活方式 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "主题 + 文化 + 客户认同  ·  加盟 80%+", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "亚朵 Atour (2,015-2,088)", "亚朵", "94", "S · 95 分 冠军"),
        ("2", "喆啡 James Joyce", "锦江 (在营 610+)", "85", "A · 86 分 迈点 TOP1"),
        ("3", "桔子水晶 Crystal Orange", "华住", "86", "S · 89 分"),
        ("4", "亚朵 S Atour S", "亚朵", "88", "S · 92 分"),
        ("5", "希岸 Xana", "锦江", "80", "A · 82 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GOLD, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GOLD)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 22), fill=GOLD)
        draw.text((W - MARGIN - 80, card_y + 35), "🎨", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "🎯 生活方式 = 经营哲学", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "三件套：单一文化锚点 + 故事化空间 + 客户价值认同", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 8, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "08_生活方式.png"), 'PNG', quality=95)


def page_09_resort():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "RESORT · 度假层", color=GREEN)

    draw.text((MARGIN, 150), "🏝", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "度假层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "ADR 800-3,000+ 元  ·  2026 拐点：体验型崛起", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "安缦 Aman", "独立", "95", "S · 90 分 仍居 TOP"),
        ("2", "Club Med", "地中海俱乐部 (复星)", "92", "S · 91 分 一价全包+亲子"),
        ("3", "悦榕庄 Banyan Tree", "悦榕集团", "90", "S · 88 分 增速放缓"),
        ("4", "瑰丽 Rosewood", "新世界 (郑志刚)", "92", "S · 88 分"),
        ("5", "嘉佩乐 Capella", "独立", "93", "S · 87 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, GREEN, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=GREEN)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 22), fill=GREEN)
        draw.text((W - MARGIN - 80, card_y + 35), "🌴", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "⚡ 2026 行业拐点：体验型崛起", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "安缦/悦榕庄情怀祛魅 · Club Med 一价全包逆势", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 9, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "09_度假层.png"), 'PNG', quality=95)


def page_10_apartment():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "APARTMENT · 服务式公寓", color=RED)

    draw.text((MARGIN, 150), "🏢", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "公寓层 TOP 5", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "长住市场  ·  雅诗阁中国 110 家 / 20,000+ 公寓", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    brands = [
        ("1", "雅诗阁 Ascott", "凯德雅诗阁 (新加坡)", "92", "S · 90 分"),
        ("2", "万豪行政公寓 ExRes", "万豪", "88", "A · 85 分"),
        ("3", "盛捷 Somerset", "凯德雅诗阁", "84", "A · 85 分"),
        ("4", "馨乐庭 Citadines", "凯德雅诗阁", "82", "A · 84 分"),
        ("5", "辉盛坊 Fraser Suites", "Frasers (新加坡)", "82", "A · 82 分"),
    ]

    card_y = 440
    for rank, name, parent, mbi, grade in brands:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 130, CARD_BG, RED, 16)
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=RED)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 64), fill=(255, 255, 255))
        draw.text((MARGIN + 130, card_y + 25), name, font=load_font(FONT_BOLD_PATH, 34), fill=DARK)
        draw.text((MARGIN + 130, card_y + 75), parent, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        draw.text((MARGIN + 130, card_y + 105), f"MBI {mbi}  ·  {grade}", font=load_font(FONT_BOLD_PATH, 22), fill=RED)
        draw.text((W - MARGIN - 80, card_y + 35), "🏬", font=load_font(FONT_BOLD_PATH, 56))
        card_y += 145

    draw.rounded_rectangle([MARGIN, 1220, W - MARGIN, 1300], 16, fill=DARK)
    draw.text((MARGIN + 30, 1235), "🌐 凯德 + 万豪 + Frasers 三足鼎立", font=load_font(FONT_BOLD_PATH, 30), fill=(255, 255, 255))
    draw.text((MARGIN + 30, 1272), "中国本土性价比品牌正在崛起 (瑰悦/恺信/优帕克)", font=load_font(FONT_REG_PATH, 22), fill=(220, 200, 175))

    add_footer(img, draw, 10, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "10_公寓层.png"), 'PNG', quality=95)


def page_11_ma():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)
    add_header_strip(draw, "2025 三大并购事件", color=RED)

    draw.text((MARGIN, 150), "💥", font=load_font(FONT_BOLD_PATH, 80))
    draw.text((MARGIN, 250), "2025 行业剧变", font=load_font(FONT_HEAVY_PATH, 70), fill=DARK)
    draw.text((MARGIN, 360), "三大并购改变中国酒店业格局", font=load_font(FONT_REG_PATH, 26), fill=GRAY)

    events = [
        ("1", "同程旅行收购万达酒管", "2025-10-17 · 24.9 亿", "万达 9 大品牌 + 250+ 门店 + 400+ 筹建 并入同程 · 10/20 年不竞争协议"),
        ("2", "中旅酒店战略投资雅阁", "2025-06 · 战略入股", "中旅品牌矩阵扩展至 13+ 雅阁系 · 首次跻身全球 50 强"),
        ("3", "凯悦完成收购 Playa", "2025-06-17 · 全包度假", "凯悦总门店从 1,300 → 1,528 · Inclusive Collection 9 品牌矩阵成型"),
    ]

    card_y = 450
    for rank, title, when, desc in events:
        draw_card(draw, MARGIN, card_y, W - 2*MARGIN, 220, CARD_BG, RED, 16)
        # 大数字
        draw.rounded_rectangle([MARGIN + 20, card_y + 20, MARGIN + 100, card_y + 110], 16, fill=RED)
        draw.text((MARGIN + 35, card_y + 35), rank, font=load_font(FONT_HEAVY_PATH, 60), fill=(255, 255, 255))
        # 标题
        draw.text((MARGIN + 130, card_y + 25), title, font=load_font(FONT_BOLD_PATH, 32), fill=DARK)
        # 时间
        draw.text((MARGIN + 130, card_y + 70), when, font=load_font(FONT_BOLD_PATH, 24), fill=RED)
        # 描述
        draw.text((MARGIN + 130, card_y + 110), desc, font=load_font(FONT_REG_PATH, 22), fill=GRAY)
        # emoji
        draw.text((W - MARGIN - 70, card_y + 50), "💼", font=load_font(FONT_BOLD_PATH, 50))
        card_y += 240

    add_footer(img, draw, 11, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "11_行业并购.png"), 'PNG', quality=95)


def page_12_cta():
    img, draw = new_canvas()
    add_bg_pattern(img, draw)

    # 顶部装饰条
    draw.rectangle([0, 0, W, 16], fill=GOLD)

    # 主标题
    draw.text((MARGIN, 100), "🎁", font=load_font(FONT_BOLD_PATH, 110))
    draw.text((MARGIN, 230), "完整版桌面文档", font=load_font(FONT_HEAVY_PATH, 80), fill=DARK)
    draw.text((MARGIN, 340), "免费下载", font=load_font(FONT_HEAVY_PATH, 80), fill=RED)

    # 描述
    desc_lines = [
        "✅ 8 大层级 × 最多 50 品牌 = 378 个条目",
        "✅ 6 维综合标注 (STR / 星级 / 规模 / 服务 / 地段 / 业态)",
        "✅ 全球 TOP 13 + 中国 TOP 10 集团规模对照",
        "✅ 加盟费 / 管理费 / 单房造价 / 综合价值全维度",
        "✅ R66 数据校准 + 信源矩阵标注",
    ]
    for i, line in enumerate(desc_lines):
        y = 480 + i * 60
        draw.text((MARGIN + 30, y), line, font=load_font(FONT_BOLD_PATH, 30), fill=DARK)

    # 文档名卡片
    card_y = 820
    draw.rounded_rectangle([MARGIN, card_y, W - MARGIN, card_y + 160], 20, fill=DARK)
    draw.text((MARGIN + 30, card_y + 20), "📂", font=load_font(FONT_BOLD_PATH, 56))
    draw.text((MARGIN + 110, card_y + 20), "酒店品牌市场指数综合排名", font=load_font(FONT_BOLD_PATH, 32), fill=(255, 255, 255))
    draw.text((MARGIN + 110, card_y + 70), "_2026H2_v3.0_2026-08-20.docx", font=load_font(FONT_REG_PATH, 24), fill=(220, 200, 175))
    draw.text((MARGIN + 110, card_y + 110), "桌面路径：C:\\Users\\ericz\\Desktop\\", font=load_font(FONT_REG_PATH, 22), fill=(180, 165, 140))

    # CTA 按钮
    btn_y = 1020
    draw.rounded_rectangle([MARGIN, btn_y, W - MARGIN, btn_y + 110], 50, fill=GOLD)
    draw.text((MARGIN + 80, btn_y + 30), "👍 点赞 + ⭐ 收藏 + 🔄 转发", font=load_font(FONT_BOLD_PATH, 36), fill=(255, 255, 255))
    draw.text((MARGIN + 80, btn_y + 75), "下期讲：6 维标签完整解释 + 业主端选品矩阵", font=load_font(FONT_REG_PATH, 22), fill=(255, 250, 235))

    # 联系方式
    contact_y = 1170
    draw.text((MARGIN, contact_y), "📌 关注我：B166ER 出品", font=load_font(FONT_BOLD_PATH, 32), fill=DARK)
    draw.text((MARGIN, contact_y + 50), "ERIC的B166ER · 酒店行业地图系列", font=load_font(FONT_REG_PATH, 24), fill=GRAY)
    draw.text((MARGIN, contact_y + 90), "更新频率：每周 1-2 期深度报告", font=load_font(FONT_REG_PATH, 24), fill=GRAY)

    add_footer(img, draw, 12, TOTAL_PAGES)
    img.save(os.path.join(OUTPUT_DIR, "12_结尾CTA.png"), 'PNG', quality=95)


# ============== 主流程 ==============
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
    print(f"\n✓ 完成 {len(pages)} 张图")
    print(f"📂 输出路径: {OUTPUT_DIR}")
    print(f"📐 规格: 1080×1440 (3:4 小红书标准)")
    print(f"\n小红书发布建议:")
    print(f"1. 打开小红书 App → 创作 → 笔记 → 上传图片")
    print(f"2. 选中小红书_酒店品牌地图 文件夹所有 12 张图")
    print(f"3. 标题: 中国酒店品牌地图 2026｜8 大层级 × 378 品牌完整排名")
    print(f"4. 正文: 见各页底部 CTA 文本")
    print(f"5. 标签: #酒店 #酒店加盟 #酒店品牌 #酒店投资 #亚朵 #全季 #万豪 #洲际 #希尔顿")


if __name__ == '__main__':
    main()
