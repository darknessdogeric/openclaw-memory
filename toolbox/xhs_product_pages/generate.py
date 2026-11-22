"""小红书商品详情页生成器 v6
产品：酒店品牌市场指数综合排名 2026 H2 v3.0
风格：xhs_marketcode_2026-08-08 范式（新中式专业主义/杂志化信息流）
画布：1080 × 1440 (3:4)
作者：ERIC的B166ER出品
日期：2026-08-21

v6 关键修订：
- 范式：xhs_marketcode_2026-08-08（米白底+森林绿+芥末黄+砖红 + 9 张叙事）
- 内容：酒店品牌市场指数综合排名 2026 H2 v3.0
- 24 年酒店经验
- ¥39.9
- 字体：微软雅黑（无衬线 = DIN 替代）
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ===== 视觉系统 (xhs_marketcode_2026-08-08 范式) =====
W, H = 1080, 1440
MARGIN = 60

# 配色（新中式专业主义）
BG          = (250, 246, 238)   # F2F1ED 类象牙白底（带纸张质感）
CARD_BG     = (255, 252, 247)   # 浅卡内白
DARK        = (45, 35, 25)      # 主文字深棕黑
GOLD        = (183, 121, 31)    # 金棕
RED         = (200, 16, 46)     # 红强调
BRICK       = (189, 94, 68)     # BD5E44 砖红（印章感）
GREEN       = (45, 90, 65)      # 2D5A41 森林绿（主色）
DEEP_GREEN  = (27, 61, 51)      # 1B3D33 深绿（表头/分析）
MUSTARD     = (233, 210, 154)   # E9D29A 芥末黄
LIGHT_MUSTARD = (249, 232, 193) # F9E8C1 浅黄（卡片底）
GRAY        = (130, 110, 90)    # 浅棕灰
LINE        = (220, 200, 175)   # 浅棕线
LIGHT_GREEN = (200, 220, 200)   # 浅绿（辅助）
LIGHT_GRAY  = (235, 230, 220)   # 浅灰（卡片底）
WHITE       = (255, 255, 255)

# 字体（无衬线 = xhs_marketcode 范式特征）
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG  = r"C:\Windows\Fonts\msyh.ttc"
FONT_HEAVY = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"

# 字号（V4 体系升级版）
SZ_TITLE = 96        # 主标题
SZ_HEADING = 64      # 章节标题
SZ_H2 = 50           # 二级标题
SZ_BODY = 32         # 正文
SZ_TAG = 26          # 小标签
SZ_SMALL = 22        # 小字
SZ_FOOTER = 18       # 页脚
SZ_NUM = 90          # 大数字

def f(path, size):
    return ImageFont.truetype(path, size, index=0)

def f_reg(size):
    return ImageFont.truetype(FONT_REG, size, index=0)

def f_bold(size):
    return ImageFont.truetype(FONT_BOLD, size, index=0)

def f_heavy(size):
    return ImageFont.truetype(FONT_HEAVY, size, index=0)

def f_mixed(size, is_ascii=False):
    """自动选字体：ASCII 用 msyhbd，中文用 Source Han Serif Heavy"""
    if is_ascii:
        return f_bold(size)
    return f_heavy(size)

# ===== 通用组件 =====
def new_canvas():
    img = Image.new('RGB', (W, H), BG)
    return img, ImageDraw.Draw(img)

def bg_pattern(draw):
    """纸张质感纹理"""
    for i in range(0, W, 100):
        for j in range(0, H, 100):
            if (i + j) % 200 == 0:
                draw.ellipse([i, j, i+4, j+4], fill=(245, 240, 228))

def card(draw, x, y, w, h, bg=CARD_BG, border=None, r=24):
    """圆角卡片"""
    draw.rounded_rectangle([x, y, x+w, y+h], r, fill=bg)
    if border:
        draw.rounded_rectangle([x, y, x+w, y+h], r, outline=border, width=2)

def header_strip(draw, page_label, page, total, issue="ISSUE 26-321"):
    """顶部 masthead"""
    # 左侧品牌
    draw.text((MARGIN, 50), "B166ER · 商业内参", font=f_bold(22), fill=DARK)
    draw.text((MARGIN, 78), "ERIC的B166ER出品", font=f_reg(15), fill=GRAY)

    # 右侧日期 + 期号
    date_str = "2026.08.21"
    issue_str = f"{issue}"
    bb1 = d.textbbox((0,0), date_str, font=f_bold(20)) if False else None
    draw.text((W-MARGIN, 50), date_str, font=f_bold(20), fill=DARK, anchor='rt')
    draw.text((W-MARGIN, 78), issue_str, font=f_bold(16), fill=GOLD, anchor='rt')

    # 分隔线
    draw.line([(MARGIN, 110), (W-MARGIN, 110)], fill=LINE, width=2)

    # 胶囊形章节标签
    label_w = 240
    label_x = MARGIN
    label_y = 130
    draw.rounded_rectangle([label_x, label_y, label_x+label_w, label_y+40], 20, fill=DEEP_GREEN)
    draw.text((label_x+18, label_y+20), page_label, font=f_bold(20), fill=WHITE, anchor='lm')

def footer_strip(draw, page, total, left_label="酒店品牌市场指数 · 全案解读"):
    """底部页脚"""
    y = H - 90
    draw.line([(MARGIN, y-15), (W-MARGIN, y-15)], fill=LINE, width=1)
    draw.text((MARGIN, y+5), left_label, font=f_reg(15), fill=GRAY)
    draw.text((W-MARGIN, y+5), f"{page:02d} / {total:02d}", font=f_bold(20), fill=GOLD, anchor='rt')

def pill(draw, x, y, text, color, txt_color=WHITE, font_size=18, pad_x=14, pad_y=8):
    """胶囊标签"""
    f_ = f_bold(font_size)
    bb = draw.textbbox((0,0), text, font=f_)
    w = (bb[2]-bb[0]) + 2*pad_x
    h = (bb[3]-bb[1]) + 2*pad_y
    draw.rounded_rectangle([x, y, x+w, y+h], h//2, fill=color)
    draw.text((x+w/2, y+h/2+2), text, font=f_, fill=txt_color, anchor='mm')
    return w, h

# ===== 图 1: 封面 =====
def slide_01():
    img, d = new_canvas()
    bg_pattern(d)

    # 顶部 masthead
    d.text((MARGIN, 50), "B166ER · 商业内参", font=f_bold(22), fill=DARK)
    d.text((MARGIN, 78), "ERIC的B166ER出品", font=f_reg(15), fill=GRAY)
    d.text((W-MARGIN, 50), "2026.08.21", font=f_bold(20), fill=DARK, anchor='rt')
    d.text((W-MARGIN, 78), "ISSUE 26-321", font=f_bold(16), fill=GOLD, anchor='rt')
    d.line([(MARGIN, 110), (W-MARGIN, 110)], fill=LINE, width=2)

    # 主标题（"酒店品牌市场指数" + "综合排名" + "2026 H2" + "v3.0 实时校准"）
    y = 180
    pill(d, MARGIN, y, "深度长文", BRICK)
    y += 80

    d.text((MARGIN, y), "酒店品牌", font=f_heavy(110), fill=DARK)
    y += 130
    d.text((MARGIN, y), "市场指数综合排名", font=f_heavy(95), fill=DARK)
    y += 110

    # 红色 2026 H2 大字（数字用 msyhbd，避免 Source Han Serif 不渲染 ASCII）
    d.text((MARGIN, y), "2026 ", font=f_bold(150), fill=RED)
    d.text((MARGIN+360, y), "H2", font=f_bold(150), fill=RED)
    y += 170
    d.text((MARGIN, y), "v3.0 ", font=f_bold(36), fill=DEEP_GREEN)
    d.text((MARGIN+85, y), "实时校准版", font=f_heavy(36), fill=DEEP_GREEN)
    y += 50

    # 公式条
    d.line([(MARGIN, y), (W-MARGIN, y)], fill=DARK, width=2)
    y += 30
    d.text((W//2, y), "8 大层级  X  50 品牌  =  6 维综合标注", font=f_bold(38), fill=DARK, anchor='mm')
    y += 40
    d.line([(MARGIN, y), (W-MARGIN, y)], fill=DARK, width=2)

    # 9 张图结构说明（左侧适用人群 + 右侧全篇结构）
    y += 30
    col_w = (W - 2*MARGIN - 20) // 2
    # 左侧：适用人群（森林绿）
    card(d, MARGIN, y, col_w, 320, bg=LIGHT_GREEN, border=GREEN)
    d.text((MARGIN+24, y+30), "适用人群", font=f_bold(24), fill=DEEP_GREEN)
    d.line([(MARGIN+24, y+62), (MARGIN+col_w-24, y+62)], fill=DEEP_GREEN, width=2)
    audiences = [
        "酒店投资人（年投 500 万+）",
        "酒店业主（已开/筹备）",
        "民宿主（单店 - 10+ 店）",
        "酒店从业者（想转型）",
        "行业研究者（学生/媒体）",
    ]
    yy = y + 90
    for a in audiences:
        d.ellipse([MARGIN+30, yy, MARGIN+44, yy+14], fill=GREEN)
        d.text((MARGIN+58, yy+7), a, font=f_reg(20), fill=DARK, anchor='lm')
        yy += 40

    # 右侧：全篇结构（芥末黄）
    card(d, MARGIN+col_w+20, y, col_w, 320, bg=LIGHT_MUSTARD, border=GOLD)
    d.text((MARGIN+col_w+44, y+30), "全篇结构", font=f_bold(24), fill=GOLD)
    d.line([(MARGIN+col_w+44, y+62), (W-MARGIN-24, y+62)], fill=GOLD, width=2)
    structure = [
        "01 概念引入",
        "02 评估模型（6 维）",
        "03 8 层级结构",
        "04 奢华/高端 TOP",
        "05 中端/经济 TOP",
        "06 6 大行业判断",
        "07 加盟费数据卡",
        "08 数据应用 + 进阶",
        "09 收口 + 行动",
    ]
    yy = y + 90
    for i, s in enumerate(structure):
        d.ellipse([MARGIN+col_w+50, yy, MARGIN+col_w+62, yy+12], fill=GOLD)
        d.text((MARGIN+col_w+76, yy+6), s, font=f_reg(19), fill=DARK, anchor='lm')
        yy += 26

    # 底部页脚
    footer_strip(d, 1, 9)

    return img

# ===== 图 2: 概念引入 =====
def slide_02():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "01 · 概念引入", 2, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "酒店品牌市场指数", font=f_heavy(80), fill=DARK)
    y += 110
    # "到底"黑色 + "在"红色 + "评什么"黑色 + "?" msyhbd
    d.text((MARGIN, y), "到底", font=f_heavy(80), fill=DARK)
    d.text((MARGIN+260, y), "在", font=f_heavy(80), fill=RED)
    d.text((MARGIN+360, y), "评什么", font=f_heavy(80), fill=DARK)
    d.text((MARGIN+610, y), "?", font=f_bold(80), fill=DARK)

    # 引言卡（红色左边）
    y += 140
    card(d, MARGIN, y, W-2*MARGIN, 130, bg=CARD_BG)
    d.rectangle([MARGIN, y, MARGIN+5, y+130], fill=RED)
    d.text((MARGIN+30, y+30), "DEFINITION  /  定义", font=f_bold(16), fill=RED)
    d.text((MARGIN+30, y+65), "基于公开财报 + 信源数据，对中国酒店市场 50+ 头部品牌", font=f_reg(24), fill=DARK)
    d.text((MARGIN+30, y+95), "进行 6 维综合评估的  量化排名体系。", font=f_reg(24), fill=DARK)

    # 5 个数字序号（圆点）
    y += 170
    d.text((MARGIN, y), "本报告  5 个数据锚点", font=f_bold(34), fill=DEEP_GREEN)

    y += 70
    anchors = [
        ("01", "万豪 10,000", "全球门店数（2026-06 突破）"),
        ("02", "希尔顿 9,200+", "全球门店数（5 星标杆）"),
        ("03", "雅高 5,836", "全球门店数（欧洲代表）"),
        ("04", "全季 3,565", "华住单一品牌冠军"),
        ("05", "亚朵 2,088", "lifestyle 独苗"),
    ]
    for i, (num, val, note) in enumerate(anchors):
        yy = y + i*72
        # 圆点
        d.ellipse([MARGIN, yy, MARGIN+50, yy+50], fill=GREEN)
        d.text((MARGIN+25, yy+25), num, font=f_bold(20), fill=WHITE, anchor='mm')
        # 数值
        d.text((MARGIN+80, yy+10), val, font=f_bold(32), fill=RED)
        # 描述
        d.text((MARGIN+80, yy+50), note, font=f_reg(20), fill=GRAY)

    footer_strip(d, 2, 9)
    return img

# ===== 图 3: 评估模型 =====
def slide_03():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "02 · 评估模型", 3, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "6 ", font=f_bold(80), fill=DARK)
    d.text((MARGIN+90, y), "维综合标注", font=f_heavy(80), fill=DARK)
    d.text((MARGIN+450, y), "X", font=f_bold(80), fill=BRICK, anchor='lm')
    y += 110
    # 拆开中文 / 英文部分，避免字体不支持 ASCII
    d.text((MARGIN, y), "MBI", font=f_bold(40), fill=DEEP_GREEN)
    d.text((MARGIN+105, y), "+ ", font=f_bold(40), fill=DEEP_GREEN)
    d.text((MARGIN+155, y), "综合价值评分体系", font=f_heavy(40), fill=DEEP_GREEN)

    # 6 维卡片网格（3 列 × 2 行）
    y += 80
    dims = [
        ("01", "品牌势能", "30%", "MBI 影响力 + 品牌溢价"),
        ("02", "投资回报", "30%", "回本周期 + RevPAR 提升"),
        ("03", "业主支持", "20%", "集采 / 培训 / 督导 / 会员"),
        ("04", "退出灵活性", "10%", "解约条件 + 数据归属"),
        ("05", "抗风险", "10%", "集团财务 + 开/关店比"),
        ("06", "MBI 影响力", "0-100", "搜索 / 媒体 / 点评 / 运营  各 25%"),
    ]
    colors_6 = [GREEN, GREEN, GREEN, GREEN, GREEN, BRICK]
    card_w = (W - 2*MARGIN - 30) // 3
    card_h = 230
    for i, (num, title, weight, sub) in enumerate(dims):
        col = i % 3
        row = i // 3
        x = MARGIN + col * (card_w + 15)
        yy = y + row * (card_h + 15)
        c = colors_6[i]
        bg = LIGHT_GREEN if c == GREEN else LIGHT_MUSTARD
        card(d, x, yy, card_w, card_h, bg=bg, border=c)
        # 序号
        pill(d, x+18, yy+18, num, c, font_size=18, pad_x=10, pad_y=4)
        # 标题
        d.text((x+18, yy+80), title, font=f_bold(28), fill=DARK)
        # 权重
        d.text((x+18, yy+125), weight, font=f_bold(36), fill=BRICK if c == GREEN else DEEP_GREEN)
        # 描述
        d.text((x+18, yy+175), sub, font=f_reg(18), fill=GRAY)

    footer_strip(d, 3, 9)
    return img

# ===== 图 4: 8 层级结构 =====
def slide_04():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "03 · 8 层级结构", 4, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "8大层级", font=f_heavy(80), fill=DARK)
    y += 100
    d.text((MARGIN, y), "覆盖  奢华  ->  经济  全谱系", font=f_bold(36), fill=DEEP_GREEN)

    # 8 大层级卡片（2 列 4 行）
    y += 70
    tiers = [
        ("L1 奢华", "Luxury", "ADR 2000+ CNY", "丽思/四季/宝格丽/安缦"),
        ("L2 超高端", "Upper Upscale", "ADR 1200-2000", "JW万豪/希尔顿/凯悦"),
        ("L3 高端", "Upscale", "ADR 800-1200", "皇冠/喜来登/万丽/华邑"),
        ("L4 中高端", "Upper Midscale", "ADR 450-800", "亚朵/希尔顿欢朋/智选假日"),
        ("L5 中端", "Midscale", "ADR 250-450", "全季 3,565 / 维也纳 / 桔子"),
        ("L6 经济型", "Economy", "ADR <250", "汉庭 / 如家 / 7天 / 城市便捷"),
        ("L7 生活方式", "Lifestyle", "差异化品牌", "亚朵 / 喆啡 / 桔子水晶"),
        ("L8 长住公寓", "Long-stay", "服务式公寓", "雅诗阁 / 万豪 ExRes / 辉盛坊"),
    ]
    tier_colors = [BRICK, BRICK, GOLD, GREEN, GREEN, GREEN, DEEP_GREEN, DEEP_GREEN]
    tier_bgs = [LIGHT_MUSTARD, LIGHT_MUSTARD, LIGHT_MUSTARD, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN]

    row_h = 110
    for i, ((code, en, adr, brands), color, bg) in enumerate(zip(tiers, tier_colors, tier_bgs)):
        col = i % 2
        row = i // 2
        x = MARGIN + col * ((W - 2*MARGIN - 20) // 2 + 20)
        yy = y + row * (row_h + 15)
        cw = (W - 2*MARGIN - 20) // 2
        card(d, x, yy, cw, row_h, bg=bg, border=color)
        # 层级代码
        d.text((x+18, yy+25), code, font=f_bold(24), fill=color)
        # 英文名
        d.text((x+18, yy+58), en, font=f_reg(18), fill=GRAY)
        # ADR
        d.text((x+150, yy+25), adr, font=f_bold(18), fill=DARK)
        # 品牌示例
        d.text((x+150, yy+55), brands, font=f_reg(18), fill=DARK)

    footer_strip(d, 4, 9)
    return img

# ===== 图 5: 奢华/高端 TOP =====
def slide_05():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "04 · 奢华 + 高端 TOP", 5, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "奢华+高端", font=f_heavy(80), fill=DARK)
    y += 100
    d.text((MARGIN, y), "TOP ", font=f_bold(30), fill=DEEP_GREEN)
    d.text((MARGIN+60, y), "5 品牌对比（仅看 ", font=f_bold(30), fill=DEEP_GREEN)
    d.text((MARGIN+330, y), "MBI", font=f_bold(30), fill=DEEP_GREEN)
    d.text((MARGIN+395, y), "排序）", font=f_bold(30), fill=DEEP_GREEN)

    # 表格化
    y += 70
    # 表头
    d.rectangle([MARGIN, y, W-MARGIN, y+50], fill=DEEP_GREEN)
    headers = ["#", "品牌", "母公司", "星级", "MBI", "综合价值"]
    cw = [60, 280, 200, 100, 100, 200]
    cx = MARGIN
    for h, w in zip(headers, cw):
        d.text((cx+w/2, y+25), h, font=f_bold(20), fill=WHITE, anchor='mm')
        cx += w

    # 数据
    data = [
        ("01", "丽思卡尔顿", "万豪", "白金五星+", "98", "92"),
        ("02", "四季", "独立", "白金五星+", "97", "95"),
        ("03", "宝格丽", "万豪+LVMH", "白金五星+", "96", "90"),
        ("04", "安缦", "独立", "白金五星+", "95", "88"),
        ("05", "嘉佩乐", "独立", "白金五星+", "93", "87"),
    ]
    yy = y + 50
    for i, row in enumerate(data):
        bg = LIGHT_MUSTARD if i % 2 == 0 else CARD_BG
        d.rectangle([MARGIN, yy, W-MARGIN, yy+70], fill=bg)
        cx = MARGIN
        for j, (val, w) in enumerate(zip(row, cw)):
            color = BRICK if j in [4, 5] else DARK
            font_ = f_bold(24) if j in [4, 5] else f_bold(20)
            d.text((cx+w/2, yy+35), val, font=font_, fill=color, anchor='mm')
            cx += w
        yy += 70

    # 洞察条
    yy += 30
    d.rectangle([MARGIN, yy, W-MARGIN, yy+100], fill=LIGHT_GREEN, outline=GREEN, width=2)
    d.text((MARGIN+24, yy+30), "⚑  KEY INSIGHT", font=f_bold(20), fill=DEEP_GREEN)
    d.text((MARGIN+24, yy+62), "奢华层  TOP 5  全部不开放加盟  ·  带物业谈管理合同", font=f_bold(22), fill=DARK)

    footer_strip(d, 5, 9)
    return img

# ===== 图 6: 中端/经济 TOP =====
def slide_06():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "05 · 中端 + 经济 TOP", 6, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "中端+经济", font=f_heavy(80), fill=DARK)
    y += 100
    d.text((MARGIN, y), "加盟赛道  主战场", font=f_bold(30), fill=DEEP_GREEN)

    # 6 个 TOP 品牌卡片（3 列 × 2 行）
    y += 70
    tops = [
        ("全季", "华住", "3,565", "中端冠军", "亚朵系"),
        ("汉庭", "华住", "≈3,400", "经济型代表", "华住系"),
        ("维也纳", "锦江", "≈2,000", "中端稳居", "锦江系"),
        ("如家", "首旅", "≈2,000", "经济型老牌", "首旅系"),
        ("7天", "锦江", "≈2,500", "经济型冠军", "锦江系"),
        ("亚朵轻居", "亚朵", "≈800", "中端新锐", "亚朵系"),
    ]
    card_w = (W - 2*MARGIN - 30) // 3
    card_h = 220
    tier_bgs = [LIGHT_GREEN, LIGHT_MUSTARD, LIGHT_GREEN, LIGHT_MUSTARD, LIGHT_MUSTARD, LIGHT_GREEN]
    for i, ((brand, parent, count, role, lineage), bg) in enumerate(zip(tops, tier_bgs)):
        col = i % 3
        row = i // 3
        x = MARGIN + col * (card_w + 15)
        yy = y + row * (card_h + 15)
        color = GREEN if '绿' in str(bg) else GOLD
        card(d, x, yy, card_w, card_h, bg=bg, border=color)
        # 品牌
        d.text((x+24, yy+25), brand, font=f_bold(34), fill=DARK)
        # 母公司
        d.text((x+24, yy+72), parent, font=f_reg(20), fill=GRAY)
        # 门店数
        d.text((x+24, yy+115), count, font=f_bold(40), fill=RED)
        # 角色
        d.text((x+24, yy+170), role, font=f_bold(20), fill=DEEP_GREEN)
        # 右上 系别
        d.text((x+card_w-24, yy+25), lineage, font=f_bold(20), fill=color, anchor='rt')

    footer_strip(d, 6, 9)
    return img

# ===== 图 7: 6 大行业判断 =====
def slide_07():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "06 · 6 大行业判断", 7, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "6大行业判断", font=f_heavy(80), fill=DARK)
    y += 100
    d.text((MARGIN, y), "2026 ", font=f_bold(30), fill=DEEP_GREEN)
    d.text((MARGIN+95, y), "H2 ", font=f_bold(30), fill=DEEP_GREEN)
    d.text((MARGIN+145, y), "· 投资人选品牌必看", font=f_bold(30), fill=DEEP_GREEN)

    # 6 个判断卡片（2 列 × 3 行）
    y += 60
    judgments = [
        ("01", "亚朵系", "中国唯一 lifestyle 标杆", "MBI 94 · 综合价值 95 · 双榜首", GREEN),
        ("02", "东呈业绩对赌", "行业破冰", "城市便捷 2,000+ · 2 年回本承诺", BRICK),
        ("03", "奢华层", "全部不开放加盟", "GOP 8-15% + 业绩激励 · 带物业谈", BRICK),
        ("04", "度假酒店 2026 拐点", "体验型崛起", "ClubMed 一价全包 · 安缦/悦榕放缓", GREEN),
        ("05", "国际集团", "Tier + 软品牌双轨", "万豪 10,000 · 希尔顿 9,200+", DEEP_GREEN),
        ("06", "2025 三大并购", "重组行业格局", "同程 24.9 亿收万达酒管 · 中旅战投雅阁", GOLD),
    ]
    card_w = (W - 2*MARGIN - 20) // 2
    card_h = 175
    for i, (num, head, sub, note, color) in enumerate(judgments):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (card_w + 20)
        yy = y + row * (card_h + 15)
        bg = LIGHT_GREEN if color in [GREEN, DEEP_GREEN] else LIGHT_MUSTARD
        card(d, x, yy, card_w, card_h, bg=bg, border=color)
        # 序号
        pill(d, x+18, yy+18, num, color, font_size=18, pad_x=10, pad_y=4)
        # 主标题
        d.text((x+18, yy+80), head, font=f_bold(28), fill=DARK)
        # 副
        d.text((x+18, yy+118), sub, font=f_bold(20), fill=color)
        # 注解
        d.text((x+18, yy+148), note, font=f_reg(18), fill=GRAY)

    footer_strip(d, 7, 9)
    return img

# ===== 图 8: 加盟费数据卡 =====
def slide_08():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "07 · 加盟费数据卡", 8, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "加盟费数据卡", font=f_heavy(80), fill=DARK)
    y += 100
    d.text((MARGIN, y), "一次性  +  持续管理费  +  单房改造成本", font=f_bold(28), fill=DEEP_GREEN)

    # 3 列对比
    y += 70
    items = [
        ("一次性加盟费", "0-200 万", "品牌特许使用 + 设计 + 工程指导", LIGHT_MUSTARD, GOLD, "万"),
        ("履约保证金", "5-50 万", "合同期满可退（无息）", LIGHT_GREEN, GREEN, "万"),
        ("持续管理费", "营收 3-10%", "或 GOP 抽成 · 含品牌支持/集采/系统/会员", LIGHT_MUSTARD, GOLD, "营收/GOP"),
        ("单房改造成本", "1.5-50 万", "视层级差异巨大", LIGHT_GREEN, GREEN, "万"),
        ("总投入 (100 房店)", "100-8000 万", "含装修 + 加盟 + 保证金", LIGHT_MUSTARD, BRICK, "万"),
    ]
    card_w = (W - 2*MARGIN - 30) // 3
    card_h = 200
    for i, (title, val, sub, bg, color, unit) in enumerate(items):
        col = i % 3
        row = i // 3
        x = MARGIN + col * (card_w + 15)
        yy = y + row * (card_h + 15)
        card(d, x, yy, card_w, card_h, bg=bg, border=color)
        # 标题
        d.text((x+24, yy+30), title, font=f_bold(24), fill=DARK)
        # 数值
        d.text((x+24, yy+78), val, font=f_bold(44), fill=BRICK)
        # 单位
        d.text((x+24, yy+135), unit, font=f_bold(20), fill=color)
        # 描述
        d.text((x+24, yy+165), sub, font=f_reg(18), fill=GRAY)

    footer_strip(d, 8, 9)
    return img

# ===== 图 9: 收口 CTA =====
def slide_09():
    img, d = new_canvas()
    bg_pattern(d)
    header_strip(d, "08 · 收口 + 行动", 9, 9)

    # 主标题
    y = 220
    d.text((MARGIN, y), "¥39.9", font=f_bold(110), fill=RED)
    d.text((MARGIN+250, y+50), "看清酒店品牌加盟全貌", font=f_heavy(40), fill=DARK)
    y += 130

    # 4 步落地清单
    card(d, MARGIN, y, W-2*MARGIN, 320, bg=CARD_BG)
    d.text((MARGIN+24, y+30), "4 步落地", font=f_bold(28), fill=DEEP_GREEN)
    d.line([(MARGIN+24, y+72), (W-MARGIN-24, y+72)], fill=DEEP_GREEN, width=2)
    steps = [
        ("01", "看完整数据地图", "8 层级 X 50 品牌 X 6 维"),
        ("02", "对比加盟 vs 自创", "5 大加盟费 + ROI 估算"),
        ("03", "锁定 3-5 个目标品牌", "按业主视角 / 投资回报"),
        ("04", "实地考察 + 谈判", "总部开发部 + 带物业谈"),
    ]
    yy = y + 95
    for num, head, sub in steps:
        d.ellipse([MARGIN+30, yy, MARGIN+66, yy+36], fill=GREEN)
        d.text((MARGIN+48, yy+18), num, font=f_bold(18), fill=WHITE, anchor='mm')
        d.text((MARGIN+90, yy+4), head, font=f_bold(22), fill=DARK)
        d.text((MARGIN+90, yy+38), sub, font=f_reg(17), fill=GRAY)
        yy += 55

    # 总结金句（黄色）
    y += 360
    d.rectangle([MARGIN, y, W-MARGIN, y+130], fill=LIGHT_MUSTARD, outline=BRICK, width=3)
    d.text((MARGIN+24, y+25), "▶  CORE LAW  /  核心法则", font=f_bold(18), fill=BRICK)
    d.text((MARGIN+24, y+58), "选品牌 ≠ 听招商会  ·  =  看完整数据地图", font=f_bold(26), fill=DARK)
    d.text((MARGIN+24, y+95), "24 年酒店实战老兵  ·  B166ER 编制  ·  一手信源", font=f_reg(18), fill=GRAY)

    # CTA 区
    y = H - 200
    d.rectangle([MARGIN, y, W-MARGIN, y+90], fill=DEEP_GREEN)
    d.text((MARGIN+24, y+22), "ERIC的B166ER出品", font=f_bold(22), fill=GOLD)
    d.text((MARGIN+24, y+58), "小红书店铺直接拍  ·  私信 \"报告\" 领 ¥10 早鸟券", font=f_reg(18), fill=WHITE)
    d.text((W-MARGIN-24, y+22), "¥39.9", font=f_bold(50), fill=RED, anchor='rt')
    d.text((W-MARGIN-24, y+62), "原价 ¥299", font=f_reg(18), fill=WHITE, anchor='rt')

    return img


# ===== 水印 (R12) =====
def apply_watermark(img, text="B166ER-20260821"):
    d = ImageDraw.Draw(img)
    wm_font = f_reg(11)
    bb = d.textbbox((0, 0), text, font=wm_font)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    x = W - tw - 14
    y = 14
    d.rectangle([x-6, y-4, x+tw+6, y+th+4], fill=(250, 247, 240))
    d.text((x+tw/2, y+th/2), text, font=wm_font, fill=GRAY, anchor='mm')
    return img


def main():
    out = r'D:\B166ER-OpenClaw\workspace\output\小红书商品图_酒店品牌市场指数_xhs_marketcode'
    os.makedirs(out, exist_ok=True)

    pages = [
        ('01_封面',         slide_01()),
        ('02_概念引入',     slide_02()),
        ('03_评估模型',     slide_03()),
        ('04_8层级结构',    slide_04()),
        ('05_奢华高端TOP',  slide_05()),
        ('06_中端经济TOP',  slide_06()),
        ('07_6大判断',      slide_07()),
        ('08_加盟费卡',     slide_08()),
        ('09_收口CTA',      slide_09()),
    ]

    for name, img in pages:
        img = apply_watermark(img)
        path = os.path.join(out, f'{name}.png')
        img.save(path, 'PNG', quality=95)
        print(f'OK {name}.png ({img.size[0]}x{img.size[1]})')

    print(f'\n生成完成 -> {out}')
    print(f'共 {len(pages)} 张图 (1080x1440 xhs_marketcode_2026-08-08 范式)')

if __name__ == '__main__':
    main()