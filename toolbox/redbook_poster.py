"""小红书既定范式海报生成器 — 深蓝金奢华版 (PIL 本地渲染)
Author: B166ER & ERIC 出品
Version: 1.0  (2026-08-13)

输出：D:\\B166ER-OpenClaw\\workspace\\redbook_posters\\p1_cover.png ... p7_action.png
1080×1440  3:4 小红书主流竖版
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os, math

# =============== 路径配置 ===============
OUTPUT_DIR = Path(r'D:\B166ER-OpenClaw\workspace\redbook_posters')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SIZE = (1080, 1440)

# =============== 调色板(深蓝金奢华酒店科技感) ===============
NAVY = (10, 31, 61)
NAVY_DEEP = (4, 16, 35)
NAVY_LIGHT = (22, 50, 90)
GOLD = (201, 169, 97)
GOLD_BRIGHT = (235, 210, 165)
GOLD_DIM = (140, 110, 60)
WHITE = (245, 247, 250)
TEXT_DIM = (175, 190, 210)
GLASS_WHITE = (255, 255, 255)
GLASS_BG = (255, 255, 255, 8)
GLASS_BORDER = (201, 169, 97, 100)

# =============== 字体 fallback ===============
FONT_BOLD = [
    r'C:\Windows\Fonts\msyhbd.ttc',
    r'C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf',
    r'C:\Windows\Fonts\NotoSansSC-VF.ttf',
    r'C:\Windows\Fonts\msyh.ttc',
]
FONT_REG = [
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\NotoSansSC-VF.ttf',
    r'C:\Windows\Fonts\simfang.ttf',
]

_font_cache = {}

def font(size, bold=True):
    key = (size, 'B' if bold else 'R')
    if key in _font_cache:
        return _font_cache[key]
    paths = FONT_BOLD if bold else FONT_REG
    for p in paths:
        try:
            f = ImageFont.truetype(p, size)
            _font_cache[key] = f
            return f
        except Exception:
            continue
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f

# =============== 文字居中 ===============
def text_w(draw, text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0]

def draw_centered(draw, text, y, f, fill, w=SIZE[0]):
    tw = text_w(draw, text, f)
    draw.text(((w - tw)//2, y), text, fill=fill, font=f)

# =============== 背景层 ===============
def make_background():
    w, h = SIZE
    img = Image.new('RGB', SIZE, NAVY_DEEP)
    px = img.load()
    cy = h // 2
    for y in range(h):
        if y < cy:
            t = abs(y - cy) / cy
            r = int(NAVY[0] + (NAVY_LIGHT[0] - NAVY[0]) * (1 - t))
            g = int(NAVY[1] + (NAVY_LIGHT[1] - NAVY[1]) * (1 - t))
            b = int(NAVY[2] + (NAVY_LIGHT[2] - NAVY[2]) * (1 - t))
        else:
            t = abs(y - cy) / cy
            r = int(NAVY[0] + (NAVY_DEEP[0] - NAVY[0]) * t)
            g = int(NAVY[1] + (NAVY_DEEP[1] - NAVY[1]) * t)
            b = int(NAVY[2] + (NAVY_DEEP[2] - NAVY[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)

    # 顶部金色光晕
    overlay = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(500, 0, -8):
        alpha = max(0, int(50 * (1 - r / 500) ** 1.8))
        od.ellipse([w//2 - r, -r//2, w//2 + r, r//2], fill=(*GOLD, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

    # 散落金色粒子(星光)
    import random
    random.seed(42)
    overlay2 = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    od2 = ImageDraw.Draw(overlay2)
    for _ in range(120):
        x = random.randint(0, w)
        y = random.randint(0, h)
        rr = random.choice([1, 1, 1, 2])
        a = random.randint(40, 120)
        od2.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(*GOLD_BRIGHT, a))
    img = Image.alpha_composite(img.convert('RGBA'), overlay2).convert('RGB')
    return img

# =============== 通用装饰 ===============
def gold_line_with_diamond(draw, y, w, margin=80):
    draw.line([(margin, y), (w//2 - 18, y)], fill=GOLD, width=2)
    draw.line([(w//2 + 18, y), (w - margin, y)], fill=GOLD, width=2)
    # 中央菱形
    draw.polygon([(w//2 - 10, y - 8), (w//2, y), (w//2 + 10, y - 8),
                  (w//2, y + 8)], fill=GOLD)
    draw.polygon([(w//2 - 6, y - 5), (w//2, y - 1), (w//2 + 6, y - 5),
                  (w//2, y + 5)], fill=GOLD_BRIGHT)

def corner_decorations(draw, w, h):
    L, W = 60, 2
    corners = [
        (60, 60, 1, 1),
        (w - 60, 60, -1, 1),
        (60, h - 60, 1, -1),
        (w - 60, h - 60, -1, -1),
    ]
    for x, y, dx, dy in corners:
        draw.line([(x, y), (x + L*dx, y)], fill=GOLD, width=W)
        draw.line([(x, y), (x, y + L*dy)], fill=GOLD, width=W)
        draw.ellipse([x-3, y-3, x+3, y+3], fill=GOLD_BRIGHT)

def page_header(draw, w, section_text):
    f = font(20)
    draw.text((80, 72), section_text, fill=GOLD, font=f)
    gold_line_with_diamond(draw, 118, w, margin=80)

def page_footer(draw, w, h, page_no, total=7):
    draw.line([(80, h - 110), (w - 80, h - 110)], fill=GOLD_DIM, width=1)
    draw.text((80, h - 90), 'B166ER 数字笔记', fill=GOLD_BRIGHT, font=font(22))
    draw.text((80, h - 60), 'ERIC 出品', fill=TEXT_DIM, font=font(16, bold=False))
    pg_text = f'{page_no:02d} / {total:02d}'
    pg_w = text_w(draw, pg_text, font(20))
    draw.text((w - 80 - pg_w, h - 90), pg_text, fill=GOLD, font=font(20))

def glass_card(img, draw, x, y, cw, ch):
    overlay = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([(x, y), (x + cw, y + ch)], fill=(255, 255, 255, 10),
                 outline=(201, 169, 97, 120), width=1)
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert('RGB'))
    return ImageDraw.Draw(img)


# =============================================================
#  P1 封面
# =============================================================
def render_cover():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    # 顶部 AHL 标签
    draw.text((80, 72), 'AHL · HOTEL DIGITAL TRANSFORMATION',
              fill=GOLD, font=font(20))
    gold_line_with_diamond(draw, 118, w, margin=80)

    # 主体大标题（两行）
    f_title = font(86)
    title1 = '酒店'
    title2 = '数字化整合'
    draw_centered(draw, title1, h//2 - 240, f_title, GOLD_BRIGHT)
    draw_centered(draw, title2, h//2 - 150, f_title, GOLD_BRIGHT)

    # 中央金色光柱
    for i in range(3):
        overlay = Image.new('RGBA', SIZE, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([(w//2 - 1 - i*8, h//2 - 80), (w//2 + 1 + i*8, h//2 + 30)],
                     fill=(*GOLD, 30 - i*8))
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, overlay)
        img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # 副标题
    f_sub = font(32)
    draw_centered(draw, '做对这 7 件事  才是酒店的', h//2 - 10, f_sub, WHITE)
    draw_centered(draw, '「第二增长曲线」', h//2 + 36, f_sub, GOLD_BRIGHT)

    # 钩子（金色边短文案）
    gold_line_with_diamond(draw, h//2 + 130, w, margin=300)
    f_hook = font(22, bold=False)
    draw_centered(draw, '不踩坑 · 不浪费 · 不返工', h//2 + 160, f_hook, GOLD)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 1)
    return img


# =============================================================
#  P2 底层逻辑 — 4 卡片
# =============================================================
def render_logic():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '01  /  THE LOGIC  ·  底层逻辑')

    # 标题
    draw.text((80, 175), '数字化的', fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 240), '四个目的', fill=GOLD_BRIGHT, font=font(54))

    # 副标题
    draw.text((80, 320), '数字化不是工具,是经营方式的重构', fill=WHITE, font=font(22, bold=False))

    # 4 卡片 (2x2)
    items = [
        ('01', '降本', '人力/能耗/采购', '全链路降低边际成本'),
        ('02', '增效', '前台/客房/餐饮', '全流程自动化提效'),
        ('03', '体验跃迁', '入住/客房/服务', '全场景数字化体验'),
        ('04', '数据资产化', '客户/订单/行为', '全要素资产沉淀'),
    ]
    card_w, card_h = 430, 290
    gap_x, gap_y = 30, 30
    start_x = 85
    start_y = 410

    for i, (idx, name, sub1, sub2) in enumerate(items):
        col, row = i % 2, i // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        # 玻璃质感卡片
        draw = glass_card(img, draw, x, y, card_w, card_h)

        # 编号（金色描边大数字）
        draw.text((x + 25, y + 20), idx, fill=GOLD, font=font(28))
        # 横线
        draw.line([(x + 25, y + 70), (x + 60, y + 70)], fill=GOLD, width=1)

        # 名称
        draw.text((x + 25, y + 90), name, fill=GOLD_BRIGHT, font=font(38))

        # 描述两行
        draw.text((x + 25, y + 160), sub1, fill=WHITE, font=font(20))
        draw.text((x + 25, y + 195), sub2, fill=TEXT_DIM, font=font(18, bold=False))

        # 右下角小金点
        draw.ellipse([x + card_w - 20, y + card_h - 20,
                      x + card_w - 10, y + card_h - 10], fill=GOLD)

    # 底部金句
    draw_centered(draw, '不是项目,而是持续经营的能力',
                   SIZE[1] - 200, font(24), GOLD)
    draw_centered(draw, '—— 数字化的真正价值',
                   SIZE[1] - 165, font(16, bold=False), TEXT_DIM)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 2)
    return img


# =============================================================
#  P3 必做动作 — 6 模块矩阵
# =============================================================
def render_modules():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '02  /  THE ACTIONS  ·  必做动作')

    draw.text((80, 175), '必须做哪些事', fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 280), '六大模块,把数字化从"口号"变成"系统"',
              fill=WHITE, font=font(22, bold=False))

    # 6 模块 3x2
    mods = [
        ('PMS', '客房管理系统', '订单/排房/客控'),
        ('CRS', '中央预订系统', '直销/库存/价格'),
        ('CDP', '客户数据平台', '画像/标签/分群'),
        ('小程序', '直销阵地', '会员/营销/复购'),
        ('收益管理', 'RM 动态定价', '价格/库存/预测'),
        ('数据中台', 'AI 智能引擎', '分析/决策/Agent'),
    ]
    cw, ch = 290, 280
    gx, gy = 25, 25
    sx, sy = 95, 360

    for i, (m, sub, detail) in enumerate(mods):
        col, row = i % 3, i // 3
        x = sx + col * (cw + gx)
        y = sy + row * (ch + gy)
        draw = glass_card(img, draw, x, y, cw, ch)

        # 编号
        draw.text((x + 20, y + 18), f'0{i+1}', fill=GOLD, font=font(18))
        # 模块名
        draw.text((x + 20, y + 60), m, fill=GOLD_BRIGHT, font=font(30))
        # 横线
        draw.line([(x + 20, y + 105), (x + 60, y + 105)], fill=GOLD, width=1)
        # 副
        draw.text((x + 20, y + 125), sub, fill=WHITE, font=font(17, bold=False))
        # 详情
        draw.text((x + 20, y + 165), detail, fill=TEXT_DIM, font=font(14, bold=False))
        # 底部金点
        draw.ellipse([x + cw - 18, y + ch - 18, x + cw - 8, y + ch - 8], fill=GOLD)

    draw_centered(draw, '六模块齐备  =  完整的酒店数字化底座',
                   SIZE[1] - 180, font(22), GOLD)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 3)
    return img


# =============================================================
#  P4 公私域闭环(核心) — 5 流程
# =============================================================
def render_loop():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '03  /  THE LOOP  ·  公私域闭环  ·  核心')

    draw.text((80, 175), '公域 → 私域',
              fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 240), '数字化唯一的"价值闭环"', fill=GOLD_BRIGHT, font=font(28))

    # 5 步流程图(横向)
    steps = [
        ('1', '曝光', '小红书/抖音\nOTA/搜索'),
        ('2', '引流', '落地页/小店\n企微沉淀'),
        ('3', '转化', '小程序/商城\n一键下单'),
        ('4', '复购', '会员/CRM\n标签分群'),
        ('5', '回流', '数据反哺\n价格/营销'),
    ]
    step_w, step_h = 175, 200
    gap = 25
    total_w = step_w * 5 + gap * 4
    sx = (w - total_w) // 2
    sy = 360

    # 横向连接线
    draw.line([(sx, sy + step_h//2), (sx + total_w, sy + step_h//2)],
              fill=GOLD_DIM, width=2)
    # 在连线上加箭头装饰
    for k in range(5):
        cx = sx + k * (step_w + gap) + step_w + gap//2
        draw.polygon([(cx - 8, sy + step_h//2 - 10),
                      (cx + 8, sy + step_h//2),
                      (cx - 8, sy + step_h//2 + 10)],
                     fill=GOLD_BRIGHT)

    for i, (idx, name, detail) in enumerate(steps):
        x = sx + i * (step_w + gap)
        # 节点圆 + 编号
        cx, cy = x + step_w//2, sy + step_h//2
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=NAVY, outline=GOLD, width=2)
        draw.text((cx - 10, cy - 22), idx, fill=GOLD_BRIGHT, font=font(34))

        # 步骤名(底部)
        bbox = draw.textbbox((0, 0), name, font=font(28))
        nw = bbox[2] - bbox[0]
        draw.text((cx - nw//2, sy + step_h + 30), name, fill=GOLD_BRIGHT, font=font(28))

        # 描述
        for j, line in enumerate(detail.split('\n')):
            bbox = draw.textbbox((0, 0), line, font=font(16, bold=False))
            lw = bbox[2] - bbox[0]
            draw.text((cx - lw//2, sy + step_h + 75 + j*22), line,
                      fill=WHITE, font=font(16, bold=False))

    # 5 到 1 的回环(粗金色虚线箭头)
    # 从 step 5 顶部向上 → step 1 顶部
    bounce_x = sx + 4 * (step_w + gap) + step_w//2
    draw.line([(bounce_x, sy - 30), (bounce_x, sy - 60)],
              fill=GOLD, width=2)
    draw.line([(bounce_x, sy - 60), (sx + step_w//2, sy - 60)],
              fill=GOLD, width=2)
    draw.line([(sx + step_w//2, sy - 60), (sx + step_w//2, sy - 30)],
              fill=GOLD, width=2)
    # 回环标签
    fb_text = '数据回流  →  反哺'
    bbox = draw.textbbox((0, 0), fb_text, font=font(14, bold=False))
    bw = bbox[2] - bbox[0]
    draw.text(((sx + bounce_x - bw)//2, sy - 80), fb_text,
              fill=GOLD, font=font(14, bold=False))

    # 底部金句
    draw_centered(draw, '流量是血液  ·  数据是基因  ·  闭环是生命',
                   SIZE[1] - 220, font(24), GOLD)
    draw_centered(draw, '如果你的数字化没有闭环,只是在"花钱买流量"',
                   SIZE[1] - 180, font(17, bold=False), TEXT_DIM)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 4)
    return img


# =============================================================
#  P5 服务质量 — 3 场景对比
# =============================================================
def render_service():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '04  /  THE EXPERIENCE  ·  服务跃迁')

    draw.text((80, 175), '数字化如何', fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 240), '赋能服务质量', fill=GOLD_BRIGHT, font=font(54))

    # 3 大场景: 横向卡片
    scenes = [
        ('前台', '刷脸 / 自助入住', '30秒完成入住', '排队时间 -85%'),
        ('客房', '智能客控 / 小程序', '灯光/温度/服务 一键', '客户满意度 +35%'),
        ('餐饮', '扫码点餐 / 个性推荐', 'AI 推荐 + 库存联动', '翻台率 +20%'),
    ]
    cw, ch = 300, 540
    gx = 25
    sx = (w - (cw * 3 + gx * 2)) // 2
    sy = 340

    for i, (cat, f1, f2, kpi) in enumerate(scenes):
        x = sx + i * (cw + gx)
        draw = glass_card(img, draw, x, sy, cw, ch)

        # 编号
        draw.text((x + 22, y := sy + 25), f'0{i+1}', fill=GOLD, font=font(22))
        # 类目
        draw.text((x + 22, sy + 80), cat, fill=GOLD_BRIGHT, font=font(36))
        draw.line([(x + 22, sy + 140), (x + 70, sy + 140)], fill=GOLD, width=1)

        # 描述
        draw.text((x + 22, sy + 170), f1, fill=WHITE, font=font(18))
        draw.text((x + 22, sy + 210), f2, fill=TEXT_DIM, font=font(15, bold=False))

        # KPI 区块
        draw.line([(x + 22, sy + 300), (x + cw - 22, sy + 300)], fill=GOLD_DIM, width=1)
        draw.text((x + 22, sy + 330), 'KPI', fill=GOLD, font=font(14))
        # KPI 大字
        draw.text((x + 22, sy + 360), kpi, fill=GOLD_BRIGHT, font=font(24))

        # 底部装饰
        draw.ellipse([x + cw - 25, sy + ch - 25, x + cw - 10, sy + ch - 10], fill=GOLD)

    # 底部金句
    draw_centered(draw, '服务即数据  ·  数据即体验  ·  体验即复购',
                   SIZE[1] - 200, font(24), GOLD)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 5)
    return img


# =============================================================
#  P6 落地路径 — 0→1→N 阶梯
# =============================================================
def render_path():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '05  /  THE PATH  ·  落地路径')

    draw.text((80, 175), '从 0 到 N', fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 240), '的落地路径与节奏', fill=GOLD_BRIGHT, font=font(54))

    # 3 段阶梯
    stages = [
        ('阶段 0', '单店 MVP', '7 天', [
            '·  选 1 家酒店试点',
            '·  跑通 PMS + 小程序 + 收益管理',
            '·  跑出第一份"运营报表"',
        ]),
        ('阶段 1', '连锁标准化', '30 天', [
            '·  5-10 家酒店接入',
            '·  搭建 CDP + 中央 CRS',
            '·  形成 SOP + 数据看板',
        ]),
        ('阶段 2', '生态化', '90 天+', [
            '·  集团/区域全覆盖',
            '·  AI Agent 接入决策',
            '·  形成数据资产与品牌',
        ]),
    ]
    stage_w, stage_h = 290, 580
    gx = 30
    sx = (w - (stage_w * 3 + gx * 2)) // 2
    sy = 360

    for i, (label, name, period, items) in enumerate(stages):
        x = sx + i * (stage_w + gx)
        # 阶梯渐变（自下而上亮度递增）
        for j in range(3):
            overlay = Image.new('RGBA', SIZE, (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            c_bright = GOLD_BRIGHT if i == j else GOLD
            c_bright = (*c_bright, 35)
            od.rectangle([(x + j * 4, sy + stage_h - (j + 1) * 25),
                          (x + stage_w - j * 4, sy + stage_h - j * 25)],
                         fill=c_bright)
            img_rgba = img.convert('RGBA')
            img_rgba = Image.alpha_composite(img_rgba, overlay)
            img.paste(img_rgba.convert('RGB'))
        draw = ImageDraw.Draw(img)

        # 外框
        draw.rectangle([(x, sy), (x + stage_w, sy + stage_h)],
                       outline=GOLD, width=1)

        # 阶段标签
        draw.text((x + 22, sy + 25), label, fill=GOLD, font=font(18))
        # 阶段名
        draw.text((x + 22, sy + 75), name, fill=GOLD_BRIGHT, font=font(36))
        # 周期
        draw.text((x + 22, sy + 135), period, fill=GOLD, font=font(28))
        draw.line([(x + 22, sy + 185), (x + 70, sy + 185)], fill=GOLD, width=1)

        # 步骤列表
        for k, item in enumerate(items):
            draw.text((x + 22, sy + 220 + k * 60), item,
                      fill=WHITE, font=font(17))

        # 阶段编号大数字
        big_num = str(i)
        f_big = font(140)
        nbbox = draw.textbbox((0, 0), big_num, font=f_big)
        nw = nbbox[2] - nbbox[0]
        # 半透明背景大字
        overlay_big = Image.new('RGBA', SIZE, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay_big)
        od.text((x + stage_w - nw - 20, sy + stage_h - 200),
                big_num, fill=(*GOLD, 25), font=f_big)
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, overlay_big)
        img.paste(img_rgba.convert('RGB'))
        draw = ImageDraw.Draw(img)

    draw_centered(draw, '不从第一天就想要 N  ·  先从 0 走到 1',
                   SIZE[1] - 200, font(24), GOLD)

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 6)
    return img


# =============================================================
#  P7 行动清单
# =============================================================
def render_action():
    img = make_background()
    draw = ImageDraw.Draw(img)
    w, h = SIZE

    page_header(draw, w, '06  /  THE ACTIONS  ·  行动清单')

    draw.text((80, 175), '可立刻启动', fill=GOLD_BRIGHT, font=font(54))
    draw.text((80, 240), '的 9 件事', fill=GOLD_BRIGHT, font=font(54))

    # 3 段清单: 7 天 / 30 天 / 90 天
    buckets = [
        ('7 天 可启动', [
            '·  用 PMS 整理出真实房价',
            '·  上线扫码点餐/小程序',
            '·  把 OTA 评论接入日报',
        ], GOLD),
        ('30 天 可落地', [
            '·  上线收益管理 RM 系统',
            '·  搭建会员 CRM / 标签',
            '·  跑通 CDP 客户画像',
        ], GOLD_BRIGHT),
        ('90 天 可规模', [
            '·  接入 AI Agent 决策',
            '·  集团 CRS 中央预订',
            '·  形成数据资产看板',
        ], (220, 195, 130)),
    ]
    cw, ch = 295, 480
    gx = 25
    sx = (w - (cw * 3 + gx * 2)) // 2
    sy = 360

    for i, (period, items, color) in enumerate(buckets):
        x = sx + i * (cw + gx)
        draw = glass_card(img, draw, x, sy, cw, ch)

        # 顶部彩条
        overlay_top = Image.new('RGBA', SIZE, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay_top)
        od.rectangle([(x, sy), (x + cw, sy + 8)], fill=color)
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, overlay_top)
        img.paste(img_rgba.convert('RGB'))
        draw = ImageDraw.Draw(img)

        # 时间段标题
        draw.text((x + 22, sy + 50), period, fill=color, font=font(28))
        draw.line([(x + 22, sy + 100), (x + 80, sy + 100)], fill=color, width=2)

        # 列表
        for k, item in enumerate(items):
            yy = sy + 140 + k * 90
            # 序号圆
            draw.ellipse([x + 22, yy, x + 52, yy + 30], outline=color, width=1)
            n_text = str(k + 1)
            bbox = draw.textbbox((0, 0), n_text, font=font(16))
            nw = bbox[2] - bbox[0]
            nh = bbox[3] - bbox[1]
            draw.text((x + 37 - nw//2, yy + 7 - nh//2), n_text, fill=color, font=font(16))
            # 文
            draw.text((x + 70, yy + 5), item, fill=WHITE, font=font(17))

        # 底部行动 hook
        hook_y = sy + ch - 70
        draw.text((x + 22, hook_y), '→ 开始', fill=color, font=font(14, bold=False))

    # 底部 CTA
    draw_centered(draw, '关注 B166ER 数字笔记  ·  每周一份  ·  数字化落地指南',
                   SIZE[1] - 220, font(20, bold=False), GOLD)

    # 关注引导(清爽版 — 不用假二维码占位)
    hook_x = (w - 540) // 2
    hook_y = SIZE[1] - 215

    # 小图标(手机+心形) -- 用金色线条画一个简洁的红书首页示意
    icon_x = hook_x
    icon_y = hook_y
    # 手机外框
    draw.rounded_rectangle([(icon_x, icon_y), (icon_x + 60, icon_y + 100)],
                           radius=10, outline=GOLD, width=2)
    # 手机内顶部小条
    draw.rounded_rectangle([(icon_x + 8, icon_y + 8), (icon_x + 52, icon_y + 14)],
                           radius=2, fill=GOLD)
    # 屏幕区占位「B166ER」
    draw.text((icon_x + 12, icon_y + 36), 'B', fill=GOLD_BRIGHT, font=font(20))
    # 心形(象征关注)
    hx, hy = icon_x + 78, icon_y + 35
    draw.ellipse([hx, hy, hx + 22, hy + 22], outline=GOLD_BRIGHT, width=2)
    draw.ellipse([hx + 16, hy, hx + 38, hy + 22], outline=GOLD_BRIGHT, width=2)
    draw.polygon([(hx + 4, hy + 18), (hx + 34, hy + 18),
                  (hx + 19, hy + 50)], fill=GOLD_BRIGHT)

    # 文字(不空喊关注、而是给出具体动作)
    draw.text((icon_x + 130, icon_y + 10), '搜索关注', fill=GOLD_BRIGHT, font=font(22))
    draw.text((icon_x + 130, icon_y + 45), 'B166ER 数字笔记',
              fill=WHITE, font=font(26))
    draw.text((icon_x + 130, icon_y + 80), '每周一份  ·  数字化落地指南',
              fill=GOLD_DIM, font=font(16, bold=False))

    corner_decorations(draw, w, h)
    page_footer(draw, w, h, 7)
    return img


# =============================================================
#  主入口
# =============================================================
def main():
    pages = [
        ('p1_cover.png', render_cover),
        ('p2_logic.png', render_logic),
        ('p3_modules.png', render_modules),
        ('p4_loop.png', render_loop),
        ('p5_service.png', render_service),
        ('p6_path.png', render_path),
        ('p7_action.png', render_action),
    ]
    for name, fn in pages:
        path = OUTPUT_DIR / name
        img = fn()
        img.save(path, 'PNG', optimize=True)
        print(f'[OK] {name} -> {path} ({img.size[0]}x{img.size[1]})')

    print(f'\nDone. {len(pages)} files in {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
