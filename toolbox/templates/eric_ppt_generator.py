# -*- coding: utf-8 -*-
"""Eric 风格 PPT 生成器(简化版)— 用 textbox + 背景色,避免 shape 问题"""
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

RED = RGBColor(0xC8, 0x10, 0x2E)
INK = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x5A, 0x5A, 0x5A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

def create(title, sections, out="output.pptx", logo_l="2026·国庆·中秋", logo_r="ERIC 出品"):
    prs = Presentation()
    prs.slide_width = Inches(10.8)
    prs.slide_height = Inches(19.2)
    blank = prs.slide_layouts[6]

    # ===== 顶部 logo 页 =====
    s = prs.slides.add_slide(blank)
    add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
    add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)

    # ===== 一句话总结页 =====
    if 'oneliner' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_section_title(s, "■ 一句话总结 · THE ONE-LINER", RED)
        add_oneliner(s, sections['oneliner']['key3'], sections['oneliner']['sub'])

    # ===== 三个数字页 =====
    if 'numbers' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_section_title(s, "■ 三个数字看清 · 3 NUMBERS", RED)
        add_three_numbers(s, sections['numbers'])

    # ===== 三个判断页 =====
    if 'judgments' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_section_title(s, "■ 三个判断 · 3 JUDGMENTS", RED)
        add_judgments(s, sections['judgments'])

    # ===== 来源方法页 =====
    if 'sources' in sections or 'method' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_section_title(s, "■ 来源 / 方法 · SOURCES + METHOD", RED)
        add_sources_method(s, sections.get('sources',''), sections.get('method',''))

    # ===== 预测矩阵页 =====
    if 'matrix' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_section_title(s, "■ 预测指标矩阵 · FORECAST MATRIX", RED)
        add_matrix(s, sections['matrix'])

    # ===== 结论页 =====
    if 'conclusion' in sections:
        s = prs.slides.add_slide(blank)
        add_text(s, Inches(0.3), Inches(0.2), Inches(4.5), Inches(0.5), logo_l, 20, INK, bold=True)
        add_text(s, Inches(6.0), Inches(0.2), Inches(4.5), Inches(0.5), logo_r, 20, INK, bold=True, align=PP_ALIGN.RIGHT)
        add_conclusion(s, sections['conclusion'])

    prs.save(out)
    print(f"OK: {out} ({len(prs.slides)} 页)")

def add_text(s, left, top, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT):
    """添加单段文字(textbox)"""
    tb = s.shapes.add_textbox(left, top, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    if bold: p.font.bold = True
    p.alignment = align
    return tb

def add_section_title(s, title, color):
    add_text(s, Inches(0.3), Inches(1.5), Inches(10.2), Inches(0.6), title, 22, color, bold=True)

def add_oneliner(s, key3, sub):
    # 左 3 行
    for i, (k, _) in enumerate(key3):
        y = Inches(2.5 + i * 2.5)
        add_text(s, Inches(0.5), y, Inches(3), Inches(2.3), k, 56, INK, bold=True)
    # 右 3 行
    for i, (_, v) in enumerate(key3):
        y = Inches(2.5 + i * 2.5)
        add_text(s, Inches(3.5), y, Inches(3), Inches(2.3), v, 56, RED, bold=True)
    # 副标
    add_text(s, Inches(0.5), Inches(14), Inches(10), Inches(0.6), "| " + sub, 20, INK)

def add_three_numbers(s, nums):
    card_w = Inches(3)
    gap = Inches(0.25)
    for i, n in enumerate(nums):
        x = Inches(0.4 + i * 3.25)
        # 用 textbox 表达卡片(背景靠填充)
        tb = s.shapes.add_textbox(x, Inches(3.5), card_w, Inches(3))
        tf = tb.text_frame
        tf.word_wrap = True
        # 标签
        p = tf.paragraphs[0]
        p.text = n['label']
        p.font.size = Pt(18); p.font.color.rgb = INK; p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        # 空行
        tf.add_paragraph()
        # 大数
        p2 = tf.add_paragraph()
        p2.text = n['big']
        p2.font.size = Pt(40); p2.font.color.rgb = RED; p2.font.bold = True
        p2.alignment = PP_ALIGN.CENTER
        # 副
        tf.add_paragraph()
        p3 = tf.add_paragraph()
        p3.text = n['sub']
        p3.font.size = Pt(14); p3.font.color.rgb = GRAY
        p3.alignment = PP_ALIGN.CENTER

def add_judgments(s, judgments):
    for i, j in enumerate(judgments):
        y = Inches(4 + i * 3)
        add_text(s, Inches(0.5), y, Inches(1.5), Inches(2), j['num'], 56, RED, bold=True)
        add_text(s, Inches(2.5), y + Inches(0.2), Inches(7), Inches(0.6), j['title'], 22, INK, bold=True)
        add_text(s, Inches(2.5), y + Inches(1), Inches(7), Inches(0.8), j['desc'], 16, GRAY)

def add_sources_method(s, sources, method):
    add_text(s, Inches(0.5), Inches(3), Inches(4.5), Inches(0.5), "■ SOURCES", 20, RED, bold=True)
    add_text(s, Inches(0.5), Inches(3.7), Inches(4.5), Inches(0.5), sources, 16, INK)
    add_text(s, Inches(0.5), Inches(4.5), Inches(4.5), Inches(0.5), "2026.09.15-09.28 口径", 14, GRAY)
    add_text(s, Inches(5.5), Inches(3), Inches(4.5), Inches(0.5), "★ METHOD", 20, RED, bold=True)
    add_text(s, Inches(5.5), Inches(3.7), Inches(4.5), Inches(0.5), method, 16, INK)

def add_matrix(s, matrix):
    """用 textbox + 背景填充(不依赖 shape)"""
    for i, m in enumerate(matrix):
        y = Inches(4 + i * 1.5)
        tb = s.shapes.add_textbox(Inches(0.4), y, Inches(10), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        # 背景色
        from pptx.oxml.ns import qn
        from pptx.dml.color import _Color
        # 简化为纯文字
        p = tf.paragraphs[0]
        p.text = m['label']
        p.font.size = Pt(18); p.font.color.rgb = INK; p.font.bold = True
        # 同一段加值与注释
        run = p.add_run()
        run.text = "   " + m['value'] + "   ·   " + m['note']
        run.font.size = Pt(16); run.font.color.rgb = GRAY

def add_conclusion(s, conclusion):
    # 黑色长条(textbox + 居中)
    tb = s.shapes.add_textbox(Inches(0.5), Inches(11), Inches(9.8), Inches(0.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = conclusion
    p.font.size = Pt(22); p.font.color.rgb = INK; p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # 版本
    add_text(s, Inches(0.5), Inches(13), Inches(10), Inches(0.4), "2026.09.30  v1.0   ·   © ERIC & B166ER · 2026", 12, GRAY)
    add_text(s, Inches(0.5), Inches(13.5), Inches(10), Inches(0.4), "合规声明:基于公开数据推算,实际以官方复盘为准。", 11, GRAY)
    add_text(s, Inches(0.5), Inches(13.9), Inches(10), Inches(0.4), "数据来源公开渠道,二次解读仅供内部讨论使用。", 11, GRAY)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="eric_ppt_demo.pptx")
    p.add_argument("--topic", default="国庆酒店预测")
    args = p.parse_args()

    sections = {
        "oneliner": {
            "key3": [("看似","下滑"),("实则","换轨"),("正在","质升")],
            "sub": "不是衰退,是 2025 高基数 + 2026 供给结构升级 的双重作用。"
        },
        "numbers": [
            {"label":"端午双节","big":"1.24 亿","sub":"+4.4% YoY"},
            {"label":"中端 OCC","big":"63.5%","sub":"-7.92pp 系数"},
            {"label":"前5 RevPAR","big":"+28-35%","sub":"春节 同口径"}
        ],
        "judgments": [
            {"num":"01","title":"成都 TOP 4 预订热度","desc":"演唱会 + 大熊猫,周边酒店 +260%。"},
            {"num":"02","title":"重庆 + 入境机票 +40%","desc":"俄+173% / 英马加+50%+,全国 TOP1。"},
            {"num":"03","title":"川西县城酒店 +40%","desc":"秋色长尾,九寨沟/稻城/新都桥。"}
        ],
        "sources": "同程 / 携程 / 去哪儿 / 华住 / STR / 飞猪",
        "method": "同比 2025 同期(避开 2024 特殊低谷);预测口径。",
        "matrix": [
            {"label":"酒店预订量","value":"+10~+22%","note":"OTA 同比"},
            {"label":"价格涨幅","value":"+20~+200%","note":"热门 2-3 倍"},
            {"label":"行业 RevPAR","value":"+5~+12%","note":"跑赢全国平均"},
            {"label":"县域游热度","value":"+42%","note":"长尾长线"}
        ],
        "conclusion": "川渝双核 · 全国增长极 · 双节最大红利承接者"
    }

    create(title=args.topic, sections=sections, out=args.out)