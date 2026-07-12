#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_v5_pillow.py — 酒管公司供应链工程 V5 小红书详情页 (FINAL)
范式: 收益管理 V3 + B166ER 官方 B 标 (圆 B + 金环 + 深棕)
价格: ¥99 (整套资料)
排版: 居中 + 紧凑 + 大字 + 匀称
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 字体
FONT_HEI_B = "C:/Windows/Fonts/msyhbd.ttc"
FONT_HEI = "C:/Windows/Fonts/msyh.ttc"
FONT_KAI = "C:/Windows/Fonts/simkai.ttf"
FONT_SONG = "C:/Windows/Fonts/simsun.ttc"

# B166ER 品牌色 (从 brand_standard_usage.html)
COL_BG = (245, 241, 234)        # 燕麦白背景
COL_BG2 = (232, 225, 212)       # 暗燕麦
COL_INK = (26, 20, 16)          # 深棕黑 #1a1410
COL_INK2 = (58, 46, 34)         # 暗棕 #3a2e22
COL_BROWN = (42, 31, 20)        # #2a1f14
COL_GOLD = (201, 168, 124)      # #c9a87c 金色
COL_GOLD2 = (224, 211, 120)     # #e0d378 米黄
COL_RED = (184, 68, 42)         # 砖红
COL_GRAY = (138, 127, 111)      # 中性灰
COL_LIGHT = (250, 250, 250)     # 纯白

# 9 个页面 - 价格统一 ¥99
PAGES = [
    {
        "name": "p01_cover",
        "version": "V5 · 2026",
        "kicker": "酒店供应链工程",
        "title_lines": ["采购", "实战 24 年"],
        "title_em": "全套资料 ¥99",
        "lede": "5 大模块 + 13 章节 SOP + 10 类合同模板",
        "price": "¥99",
        "price_old": "原价 ¥2980",
        "stats": [("13", "章节"), ("10", "合同"), ("5", "档版本"), ("24", "年实战")],
        "cta": "¥99 立即领取",
        "cta_sub": "5 分钟发资料",
    },
    {
        "name": "p02_painpoints",
        "version": "1/9",
        "kicker": "六大痛",
        "title_lines": ["采购", "六大痛"],
        "lede": "为什么采购总是救火? 因为没体系。",
        "items": [
            "供应商管不住",
            "比价靠 Excel",
            "合同不专业",
            "绩效考核缺",
            "系统不会选",
            "账期压现金流",
        ],
    },
    {
        "name": "p03_value",
        "version": "2/9",
        "kicker": "你得到什么",
        "title_lines": ["¥99", "能拿到"],
        "lede": "5 大模块 + 13 章节 SOP + 10 类合同模板 + 工具清单",
        "items": [
            "5 大模块 完整体系",
            "13 章节 SOP",
            "10 类合同模板",
            "供应链工具矩阵",
            "5 大角色路径",
            "3 阶段实施节奏",
        ],
    },
    {
        "name": "p04_audience",
        "version": "3/9",
        "kicker": "适合谁",
        "title_lines": ["谁", "该买"],
        "lede": "5 类人, 一一对应。",
        "items": [
            "酒管公司采购总监",
            "集团供应链负责人",
            "单体酒店总经理",
            "准备酒店创业的老板",
            "酒店 IT 数字化",
        ],
    },
    {
        "name": "p05_chapters",
        "version": "4/9",
        "kicker": "13 章节",
        "title_lines": ["13 章节", "全维度"],
        "lede": "采购到付款全链路 SOP, 24-36 月可执行。",
        "items": [
            "01 供应链战略地图",
            "02 供应商分级 SOP",
            "03 比价议价 SOP",
            "04 合同模板 10 类",
            "05 应付账款管理",
            "06 供应商绩效考核",
            "07 数字化采购系统",
            "08 KPI 仪表盘",
            "09-13 工具/模板/路径",
        ],
    },
    {
        "name": "p06_templates",
        "version": "5/9",
        "kicker": "5 档版本",
        "title_lines": ["5 档", "版本"],
        "lede": "按酒管规模精准匹配。",
        "items": [
            "速赢版 ¥99 (3 月)",
            "标准版 ¥8980 (6-12 月) ★",
            "完整版 ¥19800 (12-24 月)",
            "定制版 面议",
            "陪跑版 ¥49800/年",
        ],
    },
    {
        "name": "p07_quotes",
        "version": "6/9",
        "kicker": "为什么选我",
        "title_lines": ["¥99", "替代 30 万"],
        "lede": "对比传统咨询和自建团队。",
        "items": [
            "咨询公司 1 天 ¥5000+",
            "招供应链总监 ¥30万/年",
            "顾问项目 6 月 ¥50万起",
            "本资料全套 ¥99",
            "1 次付费 · 永久可用",
            "13 章节 · 即拿即用",
        ],
    },
    {
        "name": "p08_delivery",
        "version": "7/9",
        "kicker": "怎么交付",
        "title_lines": ["5 分钟", "拿到"],
        "lede": "无需登录, 无需会员, 5 分钟拿到完整资料。",
        "items": [
            "扫码加微信",
            "备注「供应链 v1.0」",
            "5 分钟内发完整资料",
            "支持企业开票",
            "提供 1 对 1 答疑",
        ],
    },
    {
        "name": "p09_cta",
        "version": "8/9",
        "kicker": "立即购买",
        "title_lines": ["¥99", "立即购买"],
        "lede": "24-36 月体系建设, 从这一份资料开始。",
        "items": [
            "扫码加微信",
            "¥99 立即购买",
            "5 分钟发资料",
        ],
    },
]


def fnt(size, bold=True, italic=False, kai=False):
    if kai:
        return ImageFont.truetype(FONT_KAI, size)
    if italic:
        return ImageFont.truetype(FONT_KAI, size)
    if bold:
        return ImageFont.truetype(FONT_HEI_B, size)
    return ImageFont.truetype(FONT_HEI, size)


def draw_brand_b(draw, x, y, size=64, with_text=True):
    """B166ER 官方 B 标 (圆 B + 金环 + 深棕底)"""
    # 深棕圆底
    r = size // 2
    draw.ellipse([(x, y), (x + size, y + size)], fill=COL_BROWN)
    # 金色描边 (1.5px)
    draw.ellipse([(x, y), (x + size, y + size)], outline=COL_GOLD, width=2)
    # 字母 B (居中)
    bf = fnt(int(size * 0.55), bold=True)
    bch = "B"
    bbox = draw.textbbox((0, 0), bch, font=bf)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    draw.text((x + (size - bw) // 2 - bbox[0], y + (size - bh) // 2 - bbox[1] - 2),
              bch, fill=COL_GOLD, font=bf)
    # 副文字 (右侧)
    if with_text:
        text_x = x + size + 12
        # ERIC × B166ER
        ef = fnt(int(size * 0.28), bold=True)
        draw.text((text_x, y + size // 4), "ERIC × B166ER", fill=COL_INK, font=ef)
        # 共研出品
        cf = fnt(int(size * 0.22), bold=False)
        draw.text((text_x, y + size // 2 + 4), "共研出品", fill=COL_GRAY, font=cf)


def measure_text(text, font_obj):
    bbox = font_obj.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_page_v5(page, page_num, total_pages):
    """绘制 V5 风格页面 (1080x1440 = 3:4) - 居中紧凑版"""
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    side = 60

    # ===== 顶部 (8%) =====
    top_h = 110
    top_pad = 28

    # 上分隔线
    draw.line([(side, top_h - 1), (W - side, top_h - 1)], fill=COL_INK, width=3)

    # 左侧 B 标 (官方)
    draw_brand_b(draw, side, top_pad, size=64, with_text=True)

    # 右侧页码 + 版本
    version_text = f"{page.get('version', '')}"
    vf = fnt(20, bold=True)
    bbox = draw.textbbox((0, 0), version_text, font=vf)
    vw = bbox[2] - bbox[0]
    draw.text((W - side - vw, top_pad + 8), version_text, fill=COL_INK, font=vf)

    page_text = f"0{page_num} / 0{total_pages}"
    pf = fnt(20, bold=False)
    bbox = draw.textbbox((0, 0), page_text, font=pf)
    pw = bbox[2] - bbox[0]
    draw.text((W - side - pw, top_pad + 38), page_text, fill=COL_GRAY, font=pf)

    # ===== 主区 (居中紧凑) =====
    # 计算可用高度
    avail_h = H - top_h - 130  # 留底部 130
    cx = W // 2  # 中心 X

    # 1. Kicker (居中)
    if "kicker" in page:
        kicker = page["kicker"]
        kf = fnt(28, bold=True)  # 放大
        kbox = draw.textbbox((0, 0), kicker, font=kf)
        kw = kbox[2] - kbox[0]
        # 黑底白字
        kp = 20
        kw_padded = kw + kp * 2
        kicker_y = top_h + 50
        draw.rectangle([(cx - kw_padded // 2, kicker_y), (cx + kw_padded // 2, kicker_y + 56)], fill=COL_INK)
        draw.text((cx - kw // 2 - kbox[0], kicker_y + 14 - kbox[1]), kicker, fill=COL_LIGHT, font=kf)
        main_y = kicker_y + 56 + 40

    # 2. 标题 (居中大字)
    if "title_lines" in page:
        title_lines = page["title_lines"]
        line_h = 170
        title_f = fnt(170, bold=True)  # 加大到 170
        total_title_h = len(title_lines) * line_h
        title_y_start = main_y
        for i, line in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), line, font=title_f)
            tw = bbox[2] - bbox[0]
            ty = title_y_start + i * line_h
            draw.text((cx - tw // 2 - bbox[0], ty - bbox[1]), line, fill=COL_INK, font=title_f)
        main_y = title_y_start + total_title_h + 20

        # 3. em (居中斜体)
        if "title_em" in page:
            em_text = page["title_em"]
            em_f = fnt(64, italic=True)  # 加大
            bbox = draw.textbbox((0, 0), em_text, font=em_f)
            ew = bbox[2] - bbox[0]
            draw.text((cx - ew // 2 - bbox[0], main_y - bbox[1]), em_text, fill=COL_RED, font=em_f)
            main_y += 70 + 20
        else:
            main_y += 10

    # 4. Lede (居中)
    if "lede" in page:
        lede = page["lede"]
        lf = fnt(34, bold=False)  # 加大
        # 自动换行 (居中)
        max_w = W - 2 * side
        line1 = ""
        line2 = ""
        for ch in lede:
            test = line1 + ch
            bbox = draw.textbbox((0, 0), test, font=lf)
            if bbox[2] - bbox[0] <= max_w:
                line1 = test
            else:
                line2 += ch
        bbox1 = draw.textbbox((0, 0), line1, font=lf)
        l1w = bbox1[2] - bbox1[0]
        draw.text((cx - l1w // 2 - bbox1[0], main_y - bbox1[1]), line1, fill=COL_INK2, font=lf)
        main_y += 50
        if line2:
            bbox2 = draw.textbbox((0, 0), line2, font=lf)
            l2w = bbox2[2] - bbox2[0]
            draw.text((cx - l2w // 2 - bbox2[0], main_y - bbox2[1]), line2, fill=COL_INK2, font=lf)
            main_y += 50
        main_y += 30

    # 5. 价格 (居中)
    if "price" in page:
        # 分隔线
        draw.line([(side + 100, main_y), (W - side - 100, main_y)], fill=COL_INK, width=2)
        main_y += 16
        # 价格大 + 旧价小
        pf = fnt(96, bold=True)  # 加大
        price = page["price"]
        bbox = draw.textbbox((0, 0), price, font=pf)
        pw = bbox[2] - bbox[0]
        draw.text((cx - pw // 2 - bbox[0], main_y - bbox[1]), price, fill=COL_RED, font=pf)
        main_y += 110
        # 旧价
        if "price_old" in page:
            of = fnt(24, bold=False)
            op = page["price_old"]
            bbox = draw.textbbox((0, 0), op, font=of)
            ow = bbox[2] - bbox[0]
            draw.text((cx - ow // 2 - bbox[0], main_y - bbox[1]), op, fill=COL_GRAY, font=of)
            # 删除线
            line_y = main_y + 14
            draw.line([(cx - ow // 2, line_y), (cx + ow // 2, line_y)], fill=COL_GRAY, width=2)
            main_y += 40
        main_y += 20

    # 6. Stats (居中 4 列)
    if "stats" in page:
        stats = page["stats"]
        n = len(stats)
        col_w = (W - 2 * side) // n
        for i, (num, label) in enumerate(stats):
            x = side + i * col_w
            if i < n - 1:
                draw.line([(x + col_w - 2, main_y), (x + col_w - 2, main_y + 100)], fill=COL_INK, width=2)
            num_f = fnt(56, bold=True)  # 加大
            bbox = draw.textbbox((0, 0), num, font=num_f)
            nw = bbox[2] - bbox[0]
            draw.text((x + col_w // 2 - nw // 2 - bbox[0], main_y - bbox[1]), num, fill=COL_GOLD, font=num_f)
            lbl_f = fnt(20, bold=False)
            bbox2 = draw.textbbox((0, 0), label, font=lbl_f)
            lw = bbox2[2] - bbox2[0]
            draw.text((x + col_w // 2 - lw // 2 - bbox2[0], main_y + 70 - bbox2[1]), label, fill=COL_INK2, font=lbl_f)
        main_y += 120 + 16

    # 7. items (居中紧凑)
    if "items" in page:
        items = page["items"]
        # 自动计算行高
        item_h = 56
        for item in items:
            # 圆点
            dot_y = main_y + 18
            draw.ellipse([(cx - 200, dot_y), (cx - 184, dot_y + 16)], fill=COL_RED)
            it_f = fnt(30, bold=False)  # 加大
            bbox = draw.textbbox((0, 0), item, font=it_f)
            iw = bbox[2] - bbox[0]
            draw.text((cx - iw // 2 - bbox[0] + 30, main_y - bbox[1]), item, fill=COL_INK, font=it_f)
            main_y += item_h
        main_y += 16

    # 8. CTA (全宽)
    if "cta" in page:
        cta = page["cta"]
        cta_h = 110
        cta_w = W - 2 * side
        cta_x = side
        cta_y = main_y + 16
        # 主体按钮 (砖红)
        draw.rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], fill=COL_RED)
        # 内白框装饰
        draw.rectangle([(cta_x + 8, cta_y + 8), (cta_x + cta_w - 8, cta_y + cta_h - 8)], outline=COL_PAPER if False else (250, 240, 230), width=2)
        cta_f = fnt(54, bold=True)  # 加大
        bbox = draw.textbbox((0, 0), cta, font=cta_f)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text((cta_x + (cta_w - cw) // 2 - bbox[0], cta_y + (cta_h - ch) // 2 - 8 - bbox[1]),
                  cta, fill=COL_BG, font=cta_f)
        main_y += cta_h + 12
        # 副 CTA
        if "cta_sub" in page:
            csf = fnt(24, bold=False)
            cs = page["cta_sub"]
            bbox = draw.textbbox((0, 0), cs, font=csf)
            csw = bbox[2] - bbox[0]
            draw.text((cx - csw // 2 - bbox[0], main_y - bbox[1]), cs, fill=COL_GRAY, font=csf)

    # ===== 底部 (8%) - B 标 + 共同出品 =====
    bot_y = H - 110
    # 分隔线
    draw.line([(side, bot_y), (W - side, bot_y)], fill=COL_INK, width=3)
    # 左 B 标
    draw_brand_b(draw, side, bot_y + 25, size=64, with_text=True)
    # 右 日期
    date_text = "ERIC × B166ER 共研出品 · 2026"
    df = fnt(20, bold=False)
    bbox = draw.textbbox((0, 0), date_text, font=df)
    dw = bbox[2] - bbox[0]
    draw.text((W - side - dw, bot_y + 50 - bbox[1]), date_text, fill=COL_GRAY, font=df)

    return img


def main():
    print("=" * 60)
    print("V5 范式 FINAL - 酒管公司供应链工程 ¥99")
    print("=" * 60)

    total = len(PAGES)
    for i, page in enumerate(PAGES, 1):
        img = draw_page_v5(page, i, total)
        out = OUT_DIR / f"v5-{page['name']}.png"
        img.save(out, "PNG", quality=95)
        print(f"  [OK] {out.name} ({out.stat().st_size/1024:.0f}KB)")

    print(f"\n完成。{total} 张图，路径: {OUT_DIR}")


if __name__ == "__main__":
    main()