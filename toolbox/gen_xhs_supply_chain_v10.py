#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate xiaohongshu images for supply chain v1.0."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Output - using forward slashes for safety
OUT_DIR = Path("C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
FONT_HEI_B = "C:/Windows/Fonts/msyhbd.ttc"
FONT_HEI = "C:/Windows/Fonts/msyh.ttc"

# Colors
BG_DARK = (15, 23, 42)
BG_DEEP = (8, 13, 26)
TEXT_W = (255, 255, 255)
TEXT_G = (180, 200, 230)
RED = (220, 38, 38)
GOLD = (251, 191, 36)
BLUE = (59, 130, 246)
GREEN = (16, 185, 129)
PURPLE = (139, 92, 246)


def fnt(size, bold=True):
    if bold:
        return ImageFont.truetype(FONT_HEI_B, size)
    return ImageFont.truetype(FONT_HEI, size)


def gen_cover():
    W, H = 2160, 3840
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top gradient
    for y in range(H // 4):
        a = y / (H // 4)
        c = tuple(int(BG_DEEP[i] * (1-a) + BG_DARK[i] * a) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

    # Title row 1
    t1 = fnt(140, True)
    txt1 = "酒店供应链工程"
    bbox = draw.textbbox((0, 0), txt1, font=t1)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 250), txt1, fill=TEXT_W, font=t1)

    # Subtitle
    t2 = fnt(96, True)
    txt2 = "酒管公司交付包 v1.0"
    bbox = draw.textbbox((0, 0), txt2, font=t2)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 460), txt2, fill=GOLD, font=t2)

    # Sub subtitle
    ss = "24年酒店老炮 · 13章节全维度 · 24-36月导航图"
    s = fnt(48, False)
    bbox = draw.textbbox((0, 0), ss, font=s)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 620), ss, fill=TEXT_G, font=s)

    # Author
    au = "ERIC的B166ER出品"
    af = fnt(56, False)
    bbox = draw.textbbox((0, 0), au, font=af)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 720), au, fill=TEXT_W, font=af)

    # Price tag (red box)
    pby = 850
    pw, ph = 800, 200
    px = (W - pw) // 2
    draw.rounded_rectangle([(px, pby), (px+pw, pby+ph)], radius=30, fill=RED)
    pt = "RMB 2980 起"
    pf = fnt(120, True)
    bbox = draw.textbbox((0, 0), pt, font=pf)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((px + (pw - tw)//2, pby + (ph - th)//2 - 10), pt, fill=TEXT_W, font=pf)

    # 4 module cards
    cards = [
        ("13 章节 PDF", "综合主报告 · 分章节 · 工具清单", GOLD),
        ("5 大角色路径", "CEO · 项目组 · 采购总监 · 采购经理 · IT", BLUE),
        ("3 阶段实施", "基础 1-3月 · 体系 4-9月 · 智能化 10-24月", GREEN),
        ("5 档版本", "速赢 2980 / 标准 8980 / 完整 19800", PURPLE),
    ]
    cy0 = 1180
    ch, gap, cm = 300, 25, 100
    for i, (title, sub, color) in enumerate(cards):
        y = cy0 + i * (ch + gap)
        draw.rounded_rectangle([(cm, y), (W-cm, y+ch)], radius=20, fill=(30, 41, 60))
        draw.rectangle([(cm, y), (cm+30, y+ch)], fill=color)
        cf = fnt(60, True)
        draw.text((cm+100, y+50), title, fill=TEXT_W, font=cf)
        df = fnt(40, False)
        draw.text((cm+100, y+150), sub, fill=TEXT_G, font=df)

    # Anchor comparison
    bt = 2700
    at = "为什么选择这份交付包"
    atf = fnt(64, True)
    bbox = draw.textbbox((0, 0), at, font=atf)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, bt), at, fill=GOLD, font=atf)

    cy = bt + 130
    rows = [
        ("咨询公司 1 天", "RMB 5000+", RED),
        ("招供应链总监", "30万/年", RED),
        ("顾问项目 6 月", "50万起", RED),
        ("本交付包", "RMB 2980 起", GREEN),
    ]
    for i, (lbl, pr, col) in enumerate(rows):
        ly = cy + i * 90
        draw.text((200, ly), "* " + lbl, fill=TEXT_W, font=fnt(48))
        bbox = draw.textbbox((0, 0), pr, font=fnt(56, True))
        pw2 = bbox[2] - bbox[0]
        draw.text((W - 200 - pw2, ly - 5), pr, fill=col, font=fnt(56, True))

    # CTA
    cty = 3350
    ctw, cth = 1400, 220
    ctx = (W - ctw) // 2
    draw.rounded_rectangle([(ctx, cty), (ctx+ctw, cty+cth)], radius=50, fill=RED)
    ctt = "扫码加微信 · 5 分钟发资料"
    ctf = fnt(72, True)
    bbox = draw.textbbox((0, 0), ctt, font=ctf)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((ctx + (ctw - tw)//2, cty + (cth - th)//2 - 8), ctt, fill=TEXT_W, font=ctf)

    # Footer
    ft = "B166ER · ERIC出品 · 红绿灯合规"
    ff = fnt(40, False)
    bbox = draw.textbbox((0, 0), ft, font=ff)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 3720), ft, fill=TEXT_G, font=ff)

    out = OUT_DIR / "01-封面-9x16.png"
    img.save(out, "PNG", quality=95)
    print("[OK]", out)


def gen_pages():
    W, H = 1080, 1920
    pages = [
        ("痛点", RED, [
            "供应商管不住 · 报价乱品质差",
            "比价靠 Excel · 效率低留不下",
            "合同不专业 · 踩坑才后悔",
            "绩效考核缺 · 没人愿做好",
            "系统不会选 · SRM 报价乱",
            "账期压现金流 · 答不上来",
        ]),
        ("解决方案", GREEN, [
            "不是 PPT 也不仅是模板",
            "而是 24-36 月体系建设导航图",
            "5 大产品路径 · 角色精准",
            "3 阶段实施 · 节奏清晰",
            "13 章节 · 涵盖全维度",
        ]),
        ("13 章节体系", BLUE, [
            "01 主报告 全维度体系",
            "02 实施方案 · 03 体系架构",
            "04 供应商分级 · 05 工具矩阵",
            "06 KPI · 07 应急 SOP · 08 成本",
            "09 实施清单 · 10 产品矩阵",
            "11 数据经营 · 12 决策树 · 13 架构",
        ]),
        ("价格 · 价值", GOLD, [
            "速赢版 RMB 2980 (3 月)",
            "标准版 RMB 8980 (6-12 月) ★",
            "完整版 RMB 19800 (12-24 月)",
            "定制版 面议",
            "陪跑版 RMB 49800/年",
            "对比: 咨询 1 天 RMB 5000+",
        ]),
        ("CTA 行动", PURPLE, [
            "扫码加微信",
            "备注 供应链 v1.0",
            "5 分钟内发完整资料 + 选型建议",
            "适合: 酒管公司 · 集团供应链",
            "      单体酒店 · 数字化 GM",
        ]),
    ]

    for i, (title, color, lines) in enumerate(pages):
        img = Image.new("RGB", (W, H), BG_DARK)
        draw = ImageDraw.Draw(img)
        # Top color bar
        draw.rectangle([(0, 0), (W, 250)], fill=color)
        tf = fnt(80, True)
        bbox = draw.textbbox((0, 0), title, font=tf)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, 80), title, fill=TEXT_W, font=tf)

        # Subtitle page number
        st = "0" + str(i+2) + " / 06"
        sf = fnt(40, False)
        bbox = draw.textbbox((0, 0), st, font=sf)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, 320), st, fill=TEXT_G, font=sf)

        # Body
        y = 450
        for line in lines:
            draw.ellipse([(120, y+20), (140, y+40)], fill=color)
            draw.text((180, y), line, fill=TEXT_W, font=fnt(46))
            y += 90

        # Footer
        ft = "B166ER · 酒管公司供应链工程 v1.0"
        ff = fnt(36, False)
        bbox = draw.textbbox((0, 0), ft, font=ff)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, H-80), ft, fill=TEXT_G, font=ff)

        out = OUT_DIR / ("0" + str(i+2) + "-内页-" + title + "-9x16.png")
        img.save(out, "PNG", quality=95)
        print("[OK]", out)


if __name__ == "__main__":
    print("生成小红书详情图...")
    gen_cover()
    gen_pages()
    print("\n完成。位置:", OUT_DIR)
    print("图片数量: 6 张 (1 封面 + 5 内页)")
