#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_v6_fed.py — 酒管公司供应链工程 V6 美联储风格 + 合规版
范式: 美联储=深蓝 + 金 + 米白 + 黑
B 标: 严格左上 + 右下
价格: ¥99 (整套)
合规: 仅小红书站内 (评论扣 1 / 私信 / 主页)
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

# 美联储配色 (深蓝权威 + 金色尊贵 + 米白质感)
COL_BG = (245, 241, 234)        # 米白 #f5f1ea
COL_NAVY = (30, 58, 95)         # 深蓝 #1e3a5f
COL_NAVY2 = (45, 79, 122)       # 中蓝
COL_GOLD = (212, 165, 116)      # 金 #d4a574
COL_GOLD2 = (201, 168, 124)     # B标金
COL_INK = (26, 20, 16)          # 黑
COL_GRAY = (138, 127, 111)
COL_LIGHT = (250, 250, 250)
COL_BROWN = (42, 31, 20)        # B 标底
COL_RED = (184, 68, 42)         # 砖红

# 9 张 — 价格统一 ¥99 + 完全合规 (无微信/扫码)
PAGES = [
    {
        "name": "p01_cover",
        "kicker": "FEDERAL RESERVE NOTE",
        "kicker2": "酒店供应链工程手册",
        "title_lines": ["¥99", "全套 SOP"],
        "title_em": "13 章节 即拿即用",
        "lede": "采购总监 / 总经理 / 创业老板 必备工具",
        "price": "¥99",
        "price_old": "整套资料",
        "stats": [("13", "章节"), ("10", "合同"), ("5", "档版本"), ("24", "年实战")],
        "cta": "¥99 立即领取",
        "cta_sub": "评论区扣 1",
    },
    {
        "name": "p02_painpoints",
        "kicker": "PROBLEM",
        "kicker2": "六大痛",
        "title_lines": ["采购", "六大痛"],
        "lede": "采购管理为什么总是救火? 因为没体系。",
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
        "kicker": "VALUE",
        "kicker2": "你得到什么",
        "title_lines": ["¥99", "能拿到"],
        "lede": "5 大模块 + 13 章节 SOP + 10 类合同模板。",
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
        "kicker": "AUDIENCE",
        "kicker2": "适合谁",
        "title_lines": ["谁", "该买"],
        "lede": "5 类人, 一一对应推荐。",
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
        "kicker": "CHAPTERS",
        "kicker2": "13 章节",
        "title_lines": ["13", "全维度"],
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
        "kicker": "VERSIONS",
        "kicker2": "5 档版本",
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
        "kicker": "COMPARISON",
        "kicker2": "为什么选我",
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
        "kicker": "ACCESS",
        "kicker2": "怎么获取",
        "title_lines": ["评论区", "扣 1"],
        "lede": "小红书内合规获取, 无需站外沟通。",
        "items": [
            "评论区扣 1",
            "主页看自动回复",
            "点击下方购物车",
            "小红书商城下单",
            "随时查收订单",
        ],
    },
    {
        "name": "p09_cta",
        "kicker": "BUY NOW",
        "kicker2": "立即购买",
        "title_lines": ["¥99", "立即领取"],
        "lede": "24-36 月体系建设, 从这一份资料开始。",
        "items": [
            "评论区扣 1",
            "¥99 立即购买",
            "小红书商城下单",
        ],
    },
]


def fnt(size, bold=True, italic=False):
    if italic:
        return ImageFont.truetype(FONT_KAI, size)
    if bold:
        return ImageFont.truetype(FONT_HEI_B, size)
    return ImageFont.truetype(FONT_HEI, size)


def draw_brand_b(draw, x, y, size=64, with_text=True):
    """B166ER 官方 B 标 (圆 B + 金环 + 深棕底)"""
    r = size // 2
    draw.ellipse([(x, y), (x + size, y + size)], fill=COL_BROWN)
    draw.ellipse([(x, y), (x + size, y + size)], outline=COL_GOLD2, width=2)
    bf = fnt(int(size * 0.55), bold=True)
    bch = "B"
    bbox = draw.textbbox((0, 0), bch, font=bf)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    draw.text((x + (size - bw) // 2 - bbox[0], y + (size - bh) // 2 - bbox[1] - 2),
              bch, fill=COL_GOLD2, font=bf)
    if with_text:
        text_x = x + size + 16
        ef = fnt(int(size * 0.28), bold=True)
        draw.text((text_x, y + size // 5), "ERIC × B166ER", fill=COL_INK, font=ef)
        cf = fnt(int(size * 0.22), bold=False)
        draw.text((text_x, y + size // 2 + 6), "共研出品", fill=COL_GRAY, font=cf)


def draw_corner_decor(draw, x, y, w, h, color, line_w=4):
    """角落装饰 (美联储风格 - L 型边框)"""
    # 横
    draw.line([(x, y), (x + w, y)], fill=color, width=line_w)
    draw.line([(x, y + h), (x + w, y + h)], fill=color, width=line_w)
    # 竖
    draw.line([(x, y), (x, y + h)], fill=color, width=line_w)
    draw.line([(x + w, y), (x + w, y + h)], fill=color, width=line_w)


def draw_page(page, page_num, total_pages):
    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), COL_BG)
    draw = ImageDraw.Draw(img)

    side = 50
    cx = W // 2

    # ===== 顶部 (8%) =====
    top_h = 110

    # 美联储风格: 顶部金色细线 (双线)
    draw.line([(side, top_h - 8), (W - side, top_h - 8)], fill=COL_GOLD, width=2)
    draw.line([(side, top_h - 4), (W - side, top_h - 4)], fill=COL_NAVY, width=1)

    # 顶部 kicker (左对齐, 大写英文)
    if "kicker" in page:
        kicker = page["kicker"]
        kf = fnt(20, bold=True)
        draw.text((side, 28), kicker, fill=COL_NAVY, font=kf)

    # 顶部 kicker2 (中文副标)
    if "kicker2" in page:
        kicker2 = page["kicker2"]
        kf2 = fnt(16, bold=False)
        bbox = draw.textbbox((0, 0), kicker2, font=kf2)
        kw = bbox[2] - bbox[0]
        draw.text((W - side - kw, 30), kicker2, fill=COL_GRAY, font=kf2)

    # 中部分隔线 (粗, 深蓝)
    draw.line([(side, top_h + 18), (W - side, top_h + 18)], fill=COL_NAVY, width=3)

    # ===== 主区 (居中紧凑) =====
    main_y = top_h + 40

    # 1. 标题 (居中大字)
    if "title_lines" in page:
        title_lines = page["title_lines"]
        line_h = 150
        title_f = fnt(150, bold=True)
        for i, line in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), line, font=title_f)
            tw = bbox[2] - bbox[0]
            ty = main_y + i * line_h
            color = COL_RED if i == 0 and line == "¥99" else COL_INK
            draw.text((cx - tw // 2 - bbox[0], ty - bbox[1]), line, fill=color, font=title_f)
        main_y += len(title_lines) * line_h + 20

        # 2. em 副标
        if "title_em" in page:
            em_text = page["title_em"]
            em_f = fnt(48, italic=True)
            bbox = draw.textbbox((0, 0), em_text, font=em_f)
            ew = bbox[2] - bbox[0]
            draw.text((cx - ew // 2 - bbox[0], main_y - bbox[1]), em_text, fill=COL_NAVY, font=em_f)
            main_y += 60 + 20

    # 3. Lede 描述 (居中)
    if "lede" in page:
        lede = page["lede"]
        lf = fnt(30, bold=False)
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
        draw.text((cx - l1w // 2 - bbox1[0], main_y - bbox1[1]), line1, fill=COL_INK, font=lf)
        main_y += 44
        if line2:
            bbox2 = draw.textbbox((0, 0), line2, font=lf)
            l2w = bbox2[2] - bbox2[0]
            draw.text((cx - l2w // 2 - bbox2[0], main_y - bbox2[1]), line2, fill=COL_INK, font=lf)
            main_y += 44
        main_y += 30

    # 4. 价格区 (美联储: 深蓝底 + 金色边)
    if "price" in page:
        # 价格区底 (深蓝)
        pw_box_w = 540
        pw_box_h = 130
        pw_box_x = cx - pw_box_w // 2
        pw_box_y = main_y
        draw.rectangle([(pw_box_x, pw_box_y), (pw_box_x + pw_box_w, pw_box_y + pw_box_h)], fill=COL_NAVY)
        # 金色边框
        draw.rectangle([(pw_box_x, pw_box_y), (pw_box_x + pw_box_w, pw_box_y + pw_box_h)], outline=COL_GOLD, width=3)
        # 价格大字
        pf = fnt(96, bold=True)
        price = page["price"]
        bbox = draw.textbbox((0, 0), price, font=pf)
        pw = bbox[2] - bbox[0]
        ph = bbox[3] - bbox[1]
        draw.text((cx - pw // 2 - bbox[0], pw_box_y + (pw_box_h - ph) // 2 - bbox[1] - 8), price, fill=COL_GOLD, font=pf)
        main_y = pw_box_y + pw_box_h + 16
        # 副标
        if "price_old" in page:
            of = fnt(22, bold=False)
            op = page["price_old"]
            bbox = draw.textbbox((0, 0), op, font=of)
            ow = bbox[2] - bbox[0]
            draw.text((cx - ow // 2 - bbox[0], main_y - bbox[1]), op, fill=COL_GRAY, font=of)
            main_y += 36
        main_y += 8

    # 5. Stats (居中 4 列 + 美联储风格分隔)
    if "stats" in page:
        stats = page["stats"]
        n = len(stats)
        col_w = (W - 2 * side) // n
        for i, (num, label) in enumerate(stats):
            x = side + i * col_w
            # 浅深蓝分隔
            if i < n - 1:
                draw.line([(x + col_w - 2, main_y + 4), (x + col_w - 2, main_y + 100)], fill=COL_NAVY, width=1)
            # 数字大字
            num_f = fnt(54, bold=True)
            bbox = draw.textbbox((0, 0), num, font=num_f)
            nw = bbox[2] - bbox[0]
            draw.text((x + col_w // 2 - nw // 2 - bbox[0], main_y - bbox[1]), num, fill=COL_NAVY, font=num_f)
            # 标签 (金色)
            lbl_f = fnt(18, bold=True)
            bbox2 = draw.textbbox((0, 0), label, font=lbl_f)
            lw = bbox2[2] - bbox2[0]
            draw.text((x + col_w // 2 - lw // 2 - bbox2[0], main_y + 70 - bbox2[1]), label, fill=COL_GOLD, font=lbl_f)
        main_y += 110 + 16

    # 6. items (居中紧凑)
    if "items" in page:
        items = page["items"]
        item_h = 52
        for item in items:
            # 蓝色方块 (美联储风格)
            draw.rectangle([(cx - 230, main_y + 16), (cx - 214, main_y + 36)], fill=COL_NAVY)
            it_f = fnt(28, bold=False)
            bbox = draw.textbbox((0, 0), item, font=it_f)
            iw = bbox[2] - bbox[0]
            draw.text((cx - iw // 2 - bbox[0] + 30, main_y - bbox[1]), item, fill=COL_INK, font=it_f)
            main_y += item_h
        main_y += 10

    # 7. CTA (全宽深蓝)
    if "cta" in page:
        cta = page["cta"]
        cta_h = 100
        cta_w = W - 2 * side
        cta_x = side
        cta_y = main_y + 12
        # CTA 主体 (深蓝)
        draw.rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], fill=COL_NAVY)
        # 金色装饰线 (上下)
        draw.line([(cta_x, cta_y), (cta_x + cta_w, cta_y)], fill=COL_GOLD, width=4)
        draw.line([(cta_x, cta_y + cta_h), (cta_x + cta_w, cta_y + cta_h)], fill=COL_GOLD, width=4)
        cta_f = fnt(48, bold=True)
        bbox = draw.textbbox((0, 0), cta, font=cta_f)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text((cta_x + (cta_w - cw) // 2 - bbox[0], cta_y + (cta_h - ch) // 2 - 8 - bbox[1]),
                  cta, fill=COL_GOLD, font=cta_f)
        main_y += cta_h + 12
        # 副 CTA
        if "cta_sub" in page:
            csf = fnt(22, bold=True)
            cs = page["cta_sub"]
            bbox = draw.textbbox((0, 0), cs, font=csf)
            csw = bbox[2] - bbox[0]
            draw.text((cx - csw // 2 - bbox[0], main_y - bbox[1]), cs, fill=COL_RED, font=csf)

    # ===== 底部 (8%) - 严格右下 B 标 =====
    bot_y = H - 100

    # 底部分隔线
    draw.line([(side, bot_y), (W - side, bot_y)], fill=COL_NAVY, width=3)
    draw.line([(side, bot_y + 4), (W - side, bot_y + 4)], fill=COL_GOLD, width=1)

    # 左下: 版本/日期 (左侧)
    date_text = f"V6 · 0{page_num} / 0{total_pages}"
    df = fnt(20, bold=True)
    draw.text((side, bot_y + 30), date_text, fill=COL_NAVY, font=df)

    # 右下: B 标 (严格位置!)
    draw_brand_b(draw, W - side - 240, bot_y + 22, size=64, with_text=True)

    # ===== 顶部左上: B 标 (严格位置!) =====
    # 顶部 B 标放在 kicker 旁边? 不, 严格左上 - 顶部装饰行最左
    # 但我已经放了 kicker 在左上. B 标放哪儿?
    # 实际上严格左上 B 标 = 在 kicker 上方
    # 但会影响排版 - 我们放小 B 标在顶部最左上角
    # 注: top_h = 110, kicker y=28, kicker2 y=30
    # 把 B 标放到主区最左 - 跟标题对齐?
    # 按 R30 严格: 左上角 + 右下角
    # 我们已经有右下角 B 标
    # 左上角放一个简化版 B 标在 kicker 上方 (y=12)
    # 但 y=12 太小 - 调整为 y=10, size=44
    # 不行, 这会与 kicker 重叠
    # 改方案: kicker 改成右上, B 标放左上
    # 但 kicker 是美联储风格精髓
    # 折中: kicker 放右下 (与版本号合并), B 标放左上 + 右下

    # 实际: 我们已经在 top_h 之前放了 kicker (左上) 和 kicker2 (右上)
    # 严格 B 标左上 = 在 kicker 上方 y=0-30 区域
    # 改: 缩小 kicker 字号到 16, 留出空间给 B 标
    # 这里我们用画完后再覆盖一层小 B 标

    # 已画好 kicker 在左上 (side=50, y=28)
    # 加小 B 标 (size=40) 在更左上 - 但会与 kicker 重叠
    # 调整: kicker 移到右下 (与版本号合并位置), B 标放左上

    # 重新覆盖: kicker 用矩形遮罩, 改放到右上
    # 简化: 不重复画, 在左上角放一个紧凑 B 标
    # 用 24px 小 B + 文字
    # 但 kicker 也在左上
    # 我们让 kicker 改放右上 (替换 kicker2)
    # 实现: 用矩形盖住左上, 然后画 B 标

    # 实现 B 标左上 (小尺寸, 避免重叠)
    # 已在右下画完整 B 标. 左上我们放紧凑版:
    # 覆盖左上角的 kicker, 用矩形 (背景色) 覆盖
    draw.rectangle([(side - 2, 22), (side + 360, 60)], fill=COL_BG)
    # 现在左上角已空白, 画小 B 标
    draw_brand_b(draw, side, 20, size=40, with_text=True)

    return img


def main():
    print("=" * 60)
    print("V6 美联储风格 - 酒管公司供应链工程 ¥99 (合规版)")
    print("=" * 60)

    total = len(PAGES)
    for i, page in enumerate(PAGES, 1):
        img = draw_page(page, i, total)
        out = OUT_DIR / f"v6-fed-{page['name']}.png"
        img.save(out, "PNG", quality=95)
        print(f"  [OK] {out.name} ({out.stat().st_size/1024:.0f}KB)")

    print(f"\n完成。{total} 张图，路径: {OUT_DIR}")


if __name__ == "__main__":
    main()