# -*- coding: utf-8 -*-
"""
酒店项目诊断 · 上帝视角方法论 · 小红书主题图文（3:4 范式）
风格：麦肯锡 (深蓝灰机构感) + 美联储 (顶部红条 + 严谨数据感)
规格：1440×1920 (3:4, 高清版 · 小红书图文标准范式)
v3.0 · 2026-07-31 · 范式纠正：9:16 → 3:4
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ============== 设计令牌 ==============
W, H = 1440, 1920
MARGIN_L = 64
MARGIN_R = 64

NAVY = (15, 44, 74)
NAVY_DARK = (8, 24, 42)
RED = (185, 28, 28)
RED_DARK = (140, 20, 20)
CREAM = (250, 247, 240)
PAPER = (252, 250, 244)
GRAY_900 = (17, 24, 39)
GRAY_700 = (55, 65, 81)
GRAY_500 = (107, 114, 128)
GRAY_300 = (209, 213, 219)
GRAY_200 = (229, 231, 235)
GRAY_100 = (243, 244, 246)
GOLD = (180, 130, 50)

F_SERIF_HVY = r"C:/Windows/Fonts/msyhbd.ttc"
F_SERIF_REG = r"C:/Windows/Fonts/msyh.ttc"
F_HEI = r"C:/Windows/Fonts/simhei.ttf"
F_SONG = r"C:/Windows/Fonts/simsun.ttc"


def font(size, kind='hei'):
    if kind == 'hei':
        return ImageFont.truetype(F_HEI, size)
    if kind == 'song':
        return ImageFont.truetype(F_SONG, size)
    if kind == 'yahei_b':
        return ImageFont.truetype(F_SERIF_HVY, size)
    if kind == 'yahei_r':
        return ImageFont.truetype(F_SERIF_REG, size)
    return ImageFont.truetype(F_HEI, size)


def draw_fed_red_bar(draw, y, h=6):
    draw.rectangle([0, y, W, y + h], fill=RED)


def draw_header(draw, page_no, total=7, section=''):
    draw_fed_red_bar(draw, 0, 4)
    draw.text((MARGIN_L, 24), section, font=font(22, 'yahei_r'), fill=GRAY_500)
    page_text = f"{page_no:02d} / {total:02d}"
    bbox = draw.textbbox((0, 0), page_text, font=font(22, 'yahei_r'))
    tw = bbox[2] - bbox[0]
    draw.text((W - MARGIN_R - tw, 24), page_text, font=font(22, 'yahei_r'), fill=GRAY_500)
    draw.line([(MARGIN_L, 62), (W - MARGIN_R, 62)], fill=GRAY_200, width=1)


def draw_footer(draw, text='B166ER · 上帝视角五层穿透 · 酒店项目诊断'):
    fy = H - 56
    draw.line([(MARGIN_L, fy - 22), (W - MARGIN_R, fy - 22)], fill=GRAY_200, width=1)
    draw.text((MARGIN_L, fy), text, font=font(20, 'yahei_r'), fill=GRAY_500)
    side_text = 'ERIC的B166ER出品'
    bbox = draw.textbbox((0, 0), side_text, font=font(20, 'yahei_r'))
    tw = bbox[2] - bbox[0]
    draw.text((W - MARGIN_R - tw, fy), side_text, font=font(20, 'yahei_r'), fill=GRAY_500)


def draw_title(draw, y, big, sub=None, big_size=96, sub_size=30):
    lines = big.split('\n')
    line_h = int(big_size * 1.05)
    total_h = line_h * len(lines)
    draw.rectangle([(MARGIN_L, y), (MARGIN_L + 12, y + total_h)], fill=RED)
    for i, line in enumerate(lines):
        draw.text((MARGIN_L + 30, y + i * line_h), line,
                  font=font(big_size, 'yahei_b'), fill=NAVY_DARK)
    if sub:
        sy = y + total_h + 20
        draw.text((MARGIN_L, sy), sub, font=font(sub_size, 'yahei_r'), fill=GRAY_700)
    return sy if sub else y + total_h


# ============== 7 张图（v3.0 · 3:4 小红书范式）==============

def img_01_cover():
    """封面 · 开宗明义：如何诊断一个酒店项目"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_fed_red_bar(d, 0, 8)
    d.text((MARGIN_L, 48), '酒店项目 · 上帝视角诊断方法论 · v3.1', font=font(24, 'yahei_r'), fill=RED)
    # 开宗明义 · 问句型大标题
    draw_title(d, 180, '如何诊断\n一个酒店项目', '上帝视角 · 五层穿透 · 四路径决策', big_size=120, sub_size=30)
    # 方法论说明（直接告诉读者这是什么东西）
    sy = 720
    sh = 200
    d.rectangle([(MARGIN_L, sy), (W - MARGIN_R, sy + sh)], fill=CREAM, outline=GRAY_200, width=2)
    d.rectangle([(MARGIN_L, sy), (MARGIN_L + 8, sy + sh)], fill=RED)
    d.text((MARGIN_L + 40, sy + 30), '本方法论解决什么问题？', font=font(26, 'yahei_b'), fill=NAVY_DARK)
    d.text((MARGIN_L + 40, sy + 80), '酒店项目从「凭感觉」到「有判断」',
           font=font(32, 'yahei_b'), fill=NAVY_DARK)
    d.text((MARGIN_L + 40, sy + 130), '投资 · 翻牌 · 存量 · 转让 · 退出', font=font(24, 'yahei_r'), fill=GRAY_700)
    # 4 个核心数字（方法论结构）
    my = 980
    metrics = [('5', '层穿透', '物业·市场·经营·财务·战略'),
               ('27', '信息项', '5 模块诊断清单'),
               ('34', '维信源', '7 类交叉验证'),
               ('4', '条路径', '升级·翻牌·转让·退出')]
    seg_w = (W - MARGIN_L * 2) // 4
    for i, (num, label, sub) in enumerate(metrics):
        x = MARGIN_L + i * seg_w
        d.text((x, my), num, font=font(96, 'yahei_b'), fill=NAVY_DARK)
        d.text((x + 4, my + 110), label, font=font(22, 'yahei_b'), fill=NAVY_DARK)
        d.text((x + 4, my + 145), sub, font=font(18, 'yahei_r'), fill=GRAY_700)
        if i < 3:
            d.line([(x + seg_w, my + 20), (x + seg_w, my + 160)], fill=GRAY_200, width=1)
    # 大引言
    qy = 1260
    qh = 160
    d.rectangle([(MARGIN_L, qy), (W - MARGIN_R, qy + qh)], fill=NAVY)
    d.rectangle([(MARGIN_L, qy), (MARGIN_L + 8, qy + qh)], fill=RED)
    d.text((MARGIN_L + 40, qy + 35), '诊断不到 L5 · 任何建议都是治标', font=font(34, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, qy + 90), '只看一层 = 假装在做诊断', font=font(24, 'yahei_r'), fill=GRAY_300)
    # 三适用场景
    ay = 1500
    ah = 100
    d.rectangle([(MARGIN_L, ay), (W - MARGIN_R, ay + ah)], fill=CREAM, outline=GRAY_200, width=2)
    d.text((MARGIN_L + 30, ay + 22), '适用场景', font=font(20, 'yahei_r'), fill=GRAY_500)
    d.text((MARGIN_L + 30, ay + 55), '单体酒店  ·  连锁翻牌  ·  筹建期酒店  ·  资产转让评估  ·  退出决策', font=font(22, 'yahei_b'), fill=NAVY_DARK)
    # 底部 — 方法论出处
    by = 1700
    d.text((MARGIN_L, by), '方法论整合', font=font(22, 'yahei_r'), fill=GRAY_500)
    d.text((MARGIN_L, by + 40), 'Eric + B166ER', font=font(40, 'yahei_b'), fill=NAVY_DARK)
    d.text((MARGIN_L, by + 95), '酒店人 22 年  ·  AI 行业知识库  ·  头部信源', font=font(20, 'yahei_r'), fill=GRAY_700)
    draw_footer(d)
    return img


def img_02_philosophy():
    """诊断哲学 · 五层穿透"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 2, section='A · 诊断哲学')
    draw_title(d, 140, '上帝视角\n= 五层穿透', '从物业到战略 · 不留死角', big_size=96, sub_size=30)
    # 五层卡（垂直堆叠）
    layers = [
        ('L1', '物业层', '位置 / 工程 / 合规', '地基对吗？', GRAY_500),
        ('L2', '市场层', '需求 / 客群 / 竞品', '客在哪？', GRAY_700),
        ('L3', '经营层', 'OCC / ADR / 渠道 / 服务', '卖对了吗？', GOLD),
        ('L4', '财务层', 'GOP / ROI / 现金流', '赚钱吗？', NAVY),
        ('L5', '战略层', '定位 / 品牌 / 退出路径', '未来呢？', RED),
    ]
    ly = 540
    lh = 180
    gap = 18
    for i, (code, name, scope, q, color) in enumerate(layers):
        y = ly + i * (lh + gap)
        d.rectangle([(MARGIN_L, y), (W - MARGIN_R, y + lh)], fill=CREAM, outline=GRAY_200, width=2)
        d.rectangle([(MARGIN_L, y), (MARGIN_L + 12, y + lh)], fill=color)
        d.text((MARGIN_L + 30, y + 25), code, font=font(48, 'yahei_b'), fill=color)
        d.text((MARGIN_L + 150, y + 30), name, font=font(40, 'yahei_b'), fill=NAVY_DARK)
        d.text((MARGIN_L + 150, y + 90), scope, font=font(22, 'yahei_r'), fill=GRAY_700)
        # 核心问题
        bbox = d.textbbox((0, 0), q, font=font(34, 'yahei_b'))
        qw = bbox[2] - bbox[0]
        d.text((W - MARGIN_R - qw - 20, y + 60), q, font=font(34, 'yahei_b'), fill=color)
    # 底部金句
    by = 1600
    bh = 140
    d.rectangle([(MARGIN_L, by), (W - MARGIN_R, by + bh)], fill=NAVY_DARK)
    d.rectangle([(MARGIN_L, by), (MARGIN_L + 8, by + bh)], fill=RED)
    d.text((MARGIN_L + 40, by + 35), '诊断不到 L5 · 任何建议都是治标', font=font(32, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, by + 85), '只看一层 = 假装在做诊断', font=font(22, 'yahei_r'), fill=GRAY_300)
    draw_footer(d)
    return img


def img_03_phase1():
    """阶段 1 · 信息收集（5 模块 27 项）"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 3, section='B · 阶段 1')
    draw_title(d, 140, '阶段 1\n信息收集', '27 项 · 一次问清 · ≈ 53 分钟', big_size=96, sub_size=30)
    # 5 模块卡片（3 + 2）
    mods = [
        ('M1', '基础信息', '5 项 · 5 分钟', '全称 · 物业 · 房型 · 品牌', GRAY_500, False),
        ('M2', '经营数据', '12 项 · 30 分钟', '收入 · 成本 · 利润 三段', NAVY, True),
        ('M3', '定位与现状', '4 项 · 10 分钟', '客群 · 竞品 · 卡点', GRAY_500, False),
        ('M4', '已做过的', '3 项 · 5 分钟', '动作 · 有效无效 · 可投入', GRAY_500, False),
        ('M5', '输出形式', '3 项 · 3 分钟', '读者 · 场景 · 时限', GRAY_500, False),
    ]
    cy = 580
    ch = 420
    gap = 24
    cw1 = (W - MARGIN_L * 2 - gap * 2) // 3
    for i in range(3):
        code, name, meta, desc, accent, important = mods[i]
        x = MARGIN_L + i * (cw1 + gap)
        bg = NAVY if important else CREAM
        title_c = CREAM if important else NAVY_DARK
        meta_c = RED if important else GRAY_500
        d.rectangle([(x, cy), (x + cw1, cy + ch)], fill=bg, outline=NAVY if important else GRAY_200, width=2)
        d.rectangle([(x, cy), (x, cy + ch)], fill=accent)
        d.rectangle([(x, cy), (x + cw1, cy + 12)], fill=accent)
        d.text((x + 24, cy + 30), code, font=font(54, 'yahei_b'), fill=meta_c if not important else CREAM)
        d.text((x + 24, cy + 100), name, font=font(40, 'yahei_b'), fill=title_c)
        d.text((x + 24, cy + 160), meta, font=font(22, 'yahei_r'), fill=meta_c)
        d.line([(x + 24, cy + 210), (x + cw1 - 24, cy + 210)],
               fill=GRAY_200 if not important else CREAM, width=1)
        d.text((x + 24, cy + 235), desc, font=font(22, 'yahei_r'), fill=title_c if important else GRAY_700)
        if important:
            d.text((x + 24, cy + ch - 60), '★ 最重 · 占研判 60%', font=font(22, 'yahei_b'), fill=RED)
    # 第二行 2 个
    cy2 = cy + ch + 30
    cw2 = (W - MARGIN_L * 2 - gap) // 2
    for i in range(2):
        code, name, meta, desc, accent, important = mods[i + 3]
        x = MARGIN_L + i * (cw2 + gap)
        d.rectangle([(x, cy2), (x + cw2, cy2 + ch)], fill=CREAM, outline=GRAY_200, width=2)
        d.rectangle([(x, cy2), (x, cy2 + ch)], fill=accent)
        d.rectangle([(x, cy2), (x + cw2, cy2 + 12)], fill=accent)
        d.text((x + 24, cy2 + 30), code, font=font(54, 'yahei_b'), fill=accent)
        d.text((x + 24, cy2 + 100), name, font=font(40, 'yahei_b'), fill=NAVY_DARK)
        d.text((x + 24, cy2 + 160), meta, font=font(22, 'yahei_r'), fill=GRAY_500)
        d.line([(x + 24, cy2 + 210), (x + cw2 - 24, cy2 + 210)], fill=GRAY_200, width=1)
        d.text((x + 24, cy2 + 235), desc, font=font(22, 'yahei_r'), fill=GRAY_700)
    # 底部
    by = 1600
    bh = 140
    d.rectangle([(MARGIN_L, by), (W - MARGIN_R, by + bh)], fill=NAVY)
    d.rectangle([(MARGIN_L, by), (MARGIN_L + 8, by + bh)], fill=RED)
    d.text((MARGIN_L + 40, by + 35), '清单一遍 · 信息全景 · 不留盲区', font=font(32, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, by + 85), '业主 / 店长 · 谁填都行 · 模糊化也可', font=font(22, 'yahei_r'), fill=GRAY_300)
    draw_footer(d)
    return img


def img_04_phase2():
    """阶段 2 · 核心分析（34 维度信源审计）"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 4, section='C · 阶段 2')
    draw_title(d, 140, '阶段 2\n核心分析', '34 维信源 · 交叉验证 · 信息全景', big_size=96, sub_size=30)
    # 7 类信源
    sources = [
        ('A', '行业协会', '5 个', 'STR · 浩华 · 迈点 · 中国饭店协会 · 仲量联行'),
        ('B', '国际研究', '6 个', 'STR Global · HotStats · PkF · Deloitte · HVS · WATG'),
        ('C', '国内研究', '5 个', 'Fastdata · 迈点研究院 · 美团研究院 · 同程 · 携程'),
        ('D', 'OTA 平台', '6 个', '携程 · 美团 · 飞猪 · 同程 · Booking · Agoda'),
        ('E', '官方统计', '5 个', '文旅部 · 国家统计局 · 各省公报 · 城市统计公报'),
        ('F', '学术智库', '3 个', '中国社科院 · 清华建筑 · 北二外旅游管理学院'),
        ('G', '财经媒体', '4 个', '财新 · 第一财经 · 36Kr · 虎嗅'),
    ]
    cy = 540
    row_h = 130
    gap = 14
    for i, (code, name, count, members) in enumerate(sources):
        y = cy + i * (row_h + gap)
        d.rectangle([(MARGIN_L, y), (W - MARGIN_R, y + row_h)], fill=CREAM, outline=GRAY_200, width=2)
        colors = [NAVY, RED, GOLD, NAVY, GRAY_500, NAVY, RED]
        d.rectangle([(MARGIN_L, y), (MARGIN_L + 100, y + row_h)], fill=colors[i])
        d.text((MARGIN_L + 26, y + 25), code, font=font(48, 'yahei_b'), fill=CREAM)
        d.text((MARGIN_L + 26, y + 85), count, font=font(22, 'yahei_r'), fill=CREAM)
        d.text((MARGIN_L + 130, y + 25), name, font=font(34, 'yahei_b'), fill=NAVY_DARK)
        d.text((MARGIN_L + 130, y + 75), members, font=font(22, 'yahei_r'), fill=GRAY_700)
    # 底部
    by = 1600
    bh = 140
    d.rectangle([(MARGIN_L, by), (W - MARGIN_R, by + bh)], fill=NAVY_DARK)
    d.rectangle([(MARGIN_L, by), (MARGIN_L + 8, by + bh)], fill=GOLD)
    d.text((MARGIN_L + 40, by + 35), '覆盖率 ≥ 70% = 合格', font=font(34, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, by + 85), '34 维中至少 24 维有交叉验证 · 否则不交付', font=font(22, 'yahei_r'), fill=GRAY_300)
    draw_footer(d)
    return img


def img_05_5d_matrix():
    """五维可行性矩阵 · 评分决策"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 5, section='D · 决策矩阵')
    draw_title(d, 140, '五维 · 评分\n· 决策', '5 维 × 10 分 · 总分 50 · 一眼看穿', big_size=96, sub_size=30)
    # 5 维卡片（上下结构）
    dims = [
        ('M', '市场', '需求 · 客群 · 竞品', '人口 · 旅游收入'),
        ('P', '物业', '位置 · 工程 · 合规', '商圈 · 证照'),
        ('F', '财务', 'GOP · ROI · 现金流', 'IRR · 回收期'),
        ('O', '运营', 'OCC · ADR · 服务', '团队 · 系统'),
        ('E', '退出', '翻牌 · 转让 · REITs', '流动性 · 渠道'),
    ]
    cy = 540
    ch = 320
    gap = 18
    cw = (W - MARGIN_L * 2 - gap * 4) // 5
    for i, (code, name, scope, detail) in enumerate(dims):
        x = MARGIN_L + i * (cw + gap)
        d.rectangle([(x, cy), (x + cw, cy + ch)], fill=CREAM, outline=GRAY_200, width=2)
        block_h = 130
        d.rectangle([(x, cy), (x + cw, cy + block_h)], fill=NAVY)
        # 大字母居中
        bbox = d.textbbox((0, 0), code, font=font(72, 'yahei_b'))
        cw_code = bbox[2] - bbox[0]
        d.text((x + (cw - cw_code) // 2, cy + 12), code, font=font(72, 'yahei_b'), fill=CREAM)
        # 名称居中
        bbox = d.textbbox((0, 0), name, font=font(34, 'yahei_b'))
        nw = bbox[2] - bbox[0]
        d.text((x + (cw - nw) // 2, cy + 90), name, font=font(34, 'yahei_b'), fill=CREAM)
        # 范围
        d.text((x + 14, cy + 150), scope, font=font(18, 'yahei_r'), fill=GRAY_700)
        d.line([(x + 14, cy + 195), (x + cw - 14, cy + 195)], fill=GRAY_200, width=1)
        d.text((x + 14, cy + 215), detail, font=font(18, 'yahei_r'), fill=GRAY_500)
        # 评分
        d.text((x + 14, cy + 275), '/ 10', font=font(20, 'yahei_b'), fill=RED)
    # 三档决策
    dy = 940
    decisions = [
        ('≥ 40', '推荐执行', '立项 · 推进', NAVY, CREAM),
        ('30-40', '修正后执行', '补强短板 · 二次评估', GOLD, NAVY_DARK),
        ('< 30', '不建议', '止损 · 退出', RED, CREAM),
    ]
    dh = 320
    gap2 = 24
    cw3 = (W - MARGIN_L * 2 - gap2 * 2) // 3
    for i, (score, label, action, color, text_c) in enumerate(decisions):
        x = MARGIN_L + i * (cw3 + gap2)
        d.rectangle([(x, dy), (x + cw3, dy + dh)], fill=color)
        d.rectangle([(x, dy), (x, dy + dh)], fill=CREAM)
        d.text((x + 30, dy + 30), score, font=font(56, 'yahei_b'), fill=text_c)
        d.text((x + 30, dy + 110), label, font=font(34, 'yahei_b'), fill=text_c)
        d.line([(x + 30, dy + 170), (x + cw3 - 30, dy + 170)], fill=text_c, width=2)
        d.text((x + 30, dy + 190), '行动', font=font(22, 'yahei_r'), fill=text_c)
        d.text((x + 30, dy + 230), action, font=font(26, 'yahei_b'), fill=text_c)
    # 底部
    by = 1600
    bh = 140
    d.rectangle([(MARGIN_L, by), (W - MARGIN_R, by + bh)], fill=NAVY_DARK)
    d.rectangle([(MARGIN_L, by), (MARGIN_L + 8, by + bh)], fill=RED)
    d.text((MARGIN_L + 40, by + 35), '每维 ≤ 4 分 · 单独否决 · 无论总分', font=font(32, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, by + 85), '短板决定上限 · 不是平均分', font=font(22, 'yahei_r'), fill=GRAY_300)
    draw_footer(d)
    return img


def img_06_decision_tree():
    """决策树 · 4 条出路"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 6, section='E · 决策树')
    draw_title(d, 140, '决策树\n4 条出路', '升级 · 翻牌 · 转让 · 退出 · 因果触发', big_size=96, sub_size=30)
    # 2x2 决策矩阵
    paths = [
        ('升级', '保留品牌 · 局部改造', '症状：经营 OK 但增长停滞\n触发：连续 6 月 OCC>75% 但 ADR 下滑\n行动：客房升级 + 营销 · 50-100 万', NAVY),
        ('翻牌', '换品牌 · 重新定位', '症状：定位错配 · 评分低于竞品\n触发：连续 12 月 RevPAR 低于竞品均值 15%\n行动：选品牌 → 装修 → 二次开业 · 300+ 万', GOLD),
        ('转让', '资产变现 · 退出运营', '症状：现金流持续为负 · 业主无意运营\n触发：连续 6 月 GOP<0 · 救无可救\n行动：中介挂牌 · 接盘方 · 评估估值', RED),
        ('退出', '止损 · 关闭清算', '症状：法律风险 · 物业不可救\n触发：合规暴雷 · 物业到期 · 灾难\n行动：员工遣散 · 客户通知 · 清算', GRAY_500),
    ]
    cy = 560
    ch = 360
    gap = 24
    cw = (W - MARGIN_L * 2 - gap) // 2
    for i, (label, sub, detail, color) in enumerate(paths):
        col = i % 2
        row = i // 2
        x = MARGIN_L + col * (cw + gap)
        y = cy + row * (ch + gap)
        d.rectangle([(x, y), (x + cw, y + ch)], fill=CREAM, outline=GRAY_200, width=2)
        d.rectangle([(x, y), (x, y + ch)], fill=color)
        d.text((x + 20, y + 30), label, font=font(56, 'yahei_b'), fill=color)
        d.text((x + 20, y + 110), sub, font=font(24, 'yahei_r'), fill=NAVY_DARK)
        d.line([(x + 20, y + 160), (x + cw - 20, y + 160)], fill=GRAY_200, width=1)
        detail_lines = detail.split('\n')
        ly = y + 180
        for line in detail_lines:
            d.text((x + 20, ly), line, font=font(20, 'yahei_r'), fill=GRAY_700)
            ly += 36
    # 底部金句
    by = 1600
    bh = 140
    d.rectangle([(MARGIN_L, by), (W - MARGIN_R, by + bh)], fill=NAVY)
    d.rectangle([(MARGIN_L, by), (MARGIN_L + 8, by + bh)], fill=RED)
    d.text((MARGIN_L + 40, by + 35), '决策的本质 = L4 财务 和 L5 战略 之间取舍', font=font(28, 'yahei_b'), fill=CREAM)
    d.text((MARGIN_L + 40, by + 85), '别让沉没成本绑架未来', font=font(22, 'yahei_r'), fill=GRAY_300)
    draw_footer(d)
    return img


def img_07_principles():
    """方法论 · 6 条心法"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d, 7, section='G · 方法论心法')
    draw_title(d, 140, '方法论 · 6 条心法', '一图看懂酒店诊断 · 穿透的深度 = 决策的自由度', big_size=70, sub_size=26)
    # 6 条心法 - 2 行 3 列
    principles = [
        ('01', '终局思维', '3 年 5 年 10 年后 · 这个项目还在不在？', '先想终局 · 再倒推现在', NAVY),
        ('02', '五层穿透', '物业 / 市场 / 经营 / 财务 / 战略', '看不到 L5 · 不下结论', NAVY),
        ('03', '信息全景', '27 项 × 34 维信源 · 交叉验证', '不漏盲点 · 才有判断', NAVY),
        ('04', '短板否决', '每维 ≤ 4 分 · 单独死刑', '平均分 · 救不了命', RED),
        ('05', '路径对比', '升级 / 翻牌 / 转让 / 退出', '4 选 1 · 才是决策', GOLD),
        ('06', '不绑架', '别让沉没成本绑架未来', '止损 · 也是一种能力', GRAY_700),
    ]
    cy = 580
    cw = (W - MARGIN_L * 2 - 24) // 2
    ch = 280
    gap_x = 24
    gap_y = 30
    for i, (code, name, scope, hint, color) in enumerate(principles):
        col = i % 2
        row = i // 2
        x = MARGIN_L + col * (cw + gap_x)
        y = cy + row * (ch + gap_y)
        d.rectangle([(x, y), (x + cw, y + ch)], fill=CREAM, outline=GRAY_200, width=2)
        d.rectangle([(x, y), (x + 130, y + ch)], fill=color)
        d.text((x + 28, y + 60), code, font=font(60, 'yahei_b'), fill=CREAM)
        d.text((x + 160, y + 40), name, font=font(40, 'yahei_b'), fill=NAVY_DARK)
        d.line([(x + 160, y + 110), (x + cw - 24, y + 110)], fill=GRAY_200, width=1)
        d.text((x + 160, y + 130), scope, font=font(22, 'yahei_r'), fill=GRAY_700)
        d.line([(x + 160, y + 190), (x + cw - 24, y + 190)], fill=GRAY_200, width=1)
        d.text((x + 160, y + 215), hint, font=font(28, 'yahei_b'), fill=color)
    # 底部
    by = 1770
    d.text((MARGIN_L, by), '本套图 7 张 · 01 终局 → 02 哲学 → 03 信息 → 04 信源 → 05 评分 → 06 决策 → 07 心法',
           font=font(18, 'yahei_r'), fill=GRAY_500)
    draw_footer(d, text='B166ER · 方法论整合 · Eric 22 年实战 + AI 知识库 + 行业头部信源')
    return img


# ============== 主流程 ==============

def main():
    out_dir = r'D:\B166ER-OpenClaw\workspace\toolbox\hotel_diag_xhs\output'
    # 清理旧文件
    for f in os.listdir(out_dir):
        if f.endswith('.png'):
            os.remove(os.path.join(out_dir, f))
    os.makedirs(out_dir, exist_ok=True)
    funcs = [
        ('01_cover', img_01_cover),
        ('02_philosophy', img_02_philosophy),
        ('03_phase1', img_03_phase1),
        ('04_phase2', img_04_phase2),
        ('05_5d_matrix', img_05_5d_matrix),
        ('06_decision_tree', img_06_decision_tree),
        ('07_principles', img_07_principles),
    ]
    for name, fn in funcs:
        img = fn()
        path = os.path.join(out_dir, f'hotel_diag_{name}.png')
        img.save(path, 'PNG', optimize=True)
        print(f'OK -> {path} ({img.size})')
    print(f'\nDone. {len(funcs)} images generated in {out_dir}')


if __name__ == '__main__':
    main()