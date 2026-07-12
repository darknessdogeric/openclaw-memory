import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

p = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output/gen_v3_pillow.py")
s = p.read_text(encoding='utf-8')

# === FIX 1: 删除 PRIVATE PATH / 评论扣 1, 改为简单 sub box ===
old_cta = '''    # 7. CTA (仅 p01 和 p09)
    if "cta" in page:
        cta = page["cta"]
        cta_h = 80
        cta_w = W - 2 * side - 140
        cta_x = side
        cta_y = main_y
        # CTA 主按钮 (砖红)
        draw.rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], fill=COL_RED)
        cta_f = fnt(36, bold=True)
        bbox = draw.textbbox((0, 0), cta, font=cta_f)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text((cta_x + (cta_w - cw) // 2, cta_y + (cta_h - ch) // 2 - 6), cta, fill=COL_PAPER, font=cta_f)
        # 右侧 副 CTA
        sub_x = cta_x + cta_w + 12
        sub_w = 128
        sub_h = 80
        # 上 私域
        # 下 评论扣1
        # 双格
        draw.rectangle([(sub_x, cta_y), (sub_x + sub_w, cta_y + sub_h)], outline=COL_INK, width=3)
        sub_f = fnt(10, bold=False)
        draw.text((sub_x + 10, cta_y + 8), "PRIVATE PATH", fill=COL_INK, font=sub_f)
        sub_f2 = fnt(18, bold=True)
        draw.text((sub_x + 10, cta_y + 30), page.get("cta_sub", "评论扣 1"), fill=COL_INK, font=sub_f2)
        main_y += cta_h + 12'''

new_cta = '''    # 7. CTA (全宽, 无 sub box)
    if "cta" in page:
        cta = page["cta"]
        cta_h = 100
        cta_w = W - 2 * side
        cta_x = side
        cta_y = main_y
        # CTA 主按钮 (砖红)
        draw.rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], fill=COL_RED)
        # 内框装饰 (黑线)
        draw.rectangle([(cta_x + 8, cta_y + 8), (cta_x + cta_w - 8, cta_y + cta_h - 8)], outline=COL_PAPER, width=2)
        cta_f = fnt(44, bold=True)
        bbox = draw.textbbox((0, 0), cta, font=cta_f)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text((cta_x + (cta_w - cw) // 2, cta_y + (cta_h - ch) // 2 - 8), cta, fill=COL_PAPER, font=cta_f)
        main_y += cta_h + 16'''

s = s.replace(old_cta, new_cta, 1)
print('CTA replaced')

# === FIX 2: 13 章节改为 3 列 × 5 行 (空最后一格), 字大一些, 加价值描述 ===
old_chapters = '''    # 6.5 chapters_preview (13 章缩略图, 仅 p01)
    if "chapters_preview" in page:
        chs = page["chapters_preview"]
        # 4列网格 (13章 + 1空)
        cols = 4
        rows = (len(chs) + cols - 1) // cols
        cell_w = (W - 2 * side - 20) // cols
        cell_h = 56
        gap_x = 6
        gap_y = 6
        grid_top = main_y + 16
        # 标题
        sec_title = "13 章节 全维度体系"
        sf = fnt(18, bold=True)
        draw.text((side, grid_top - 32), sec_title, fill=COL_INK, font=sf)
        # 红点装饰
        draw.ellipse([(side + 200, grid_top - 22), (side + 208, grid_top - 14)], fill=COL_RED)
        for i, ch in enumerate(chs):
            r = i // cols
            c = i % cols
            x = side + c * (cell_w + gap_x)
            y = grid_top + r * (cell_h + gap_y)
            # 砖红底色
            draw.rectangle([(x, y), (x + cell_w, y + cell_h)], outline=COL_INK, width=2)
            draw.rectangle([(x + 2, y + 2), (x + cell_w - 2, y + cell_h - 2)], fill=COL_PAPER)
            # 编号 + 名称
            num_f = fnt(18, bold=True)
            draw.text((x + 10, y + 8), ch[:2], fill=COL_RED, font=num_f)
            name_f = fnt(14, bold=False)
            draw.text((x + 10, y + 28), ch[3:] if len(ch) > 3 else ch, fill=COL_INK, font=name_f)
        main_y = grid_top + rows * (cell_h + gap_y) + 8'''

new_chapters = '''    # 6.5 chapters_preview (13 章缩略图, 仅 p01)
    if "chapters_preview" in page:
        chs = page["chapters_preview"]
        # 3列 × 5行 (留 2 个空格)
        cols = 3
        rows = 5
        cell_w = (W - 2 * side - 24) // cols
        cell_h = 60
        gap_x = 12
        gap_y = 10
        grid_top = main_y + 36
        # 标题
        sec_title = "13 章节 全维度体系"
        sf = fnt(22, bold=True)
        draw.text((side, grid_top - 36), sec_title, fill=COL_INK, font=sf)
        # 红点装饰
        draw.ellipse([(side + 230, grid_top - 26), (side + 240, grid_top - 16)], fill=COL_RED)
        # 副标 (右侧)
        sub_title = "M.O.C"
        stf = fnt(14, bold=False)
        draw.text((W - side - 60, grid_top - 28), sub_title, fill=COL_GRAY, font=stf)
        for i, ch in enumerate(chs):
            r = i // cols
            c = i % cols
            x = side + c * (cell_w + gap_x)
            y = grid_top + r * (cell_h + gap_y)
            # 黑边
            draw.rectangle([(x, y), (x + cell_w, y + cell_h)], outline=COL_INK, width=2)
            # 内填
            draw.rectangle([(x + 3, y + 3), (x + cell_w - 3, y + cell_h - 3)], fill=COL_PAPER)
            # 编号大字 (砖红)
            num_f = fnt(24, bold=True)
            draw.text((x + 12, y + 8), ch[:2], fill=COL_RED, font=num_f)
            # 名称
            name_f = fnt(16, bold=True)
            draw.text((x + 12, y + 36), ch[3:] if len(ch) > 3 else ch, fill=COL_INK, font=name_f)
        # 留白格填充 (14, 15 索引 - 不存在所以留白)
        # 自动居中: 13章 + 2留白 = 15 / 3 = 5 行, 但 13 在 5×3 留 2 格 - 已自然分布
        main_y = grid_top + rows * (cell_h + gap_y) + 12'''

s = s.replace(old_chapters, new_chapters, 1)
print('Chapters replaced')

# === FIX 3: 价值锚点改为 3 列对照式 ===
old_anchor = '''    # 6.6 price_anchor (价值锚点条, 仅 p01)
    if "price_anchor" in page:
        anchor_text = page["price_anchor"]
        af = fnt(18, bold=False)
        # 黑底白字条
        ay = main_y + 8
        draw.rectangle([(side, ay), (W - side, ay + 44)], fill=COL_INK)
        # 两侧短装饰线 (砖红)
        draw.line([(side + 12, ay + 22), (side + 22, ay + 22)], fill=COL_RED, width=3)
        draw.line([(W - side - 22, ay + 22), (W - side - 12, ay + 22)], fill=COL_RED, width=3)
        bbox = draw.textbbox((0, 0), anchor_text, font=af)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, ay + 12), anchor_text, fill=COL_LIGHT, font=af)
        main_y = ay + 60'''

new_anchor = '''    # 6.6 price_anchor (3 列对照式锚点, 仅 p01)
    if "price_anchor" in page:
        anchor = page["price_anchor"]
        # 解析 3 列: 咨询 1 天 ¥5000+ | 招总监 ¥30万/年 | 本包 ¥2980
        # 简化: 用 3 段以 | 分割
        parts = anchor.split("|")
        if len(parts) == 3:
            ay = main_y + 16
            ah = 76
            col_w = (W - 2 * side - 24) // 3
            for i, p_text in enumerate(parts):
                x = side + i * (col_w + 12)
                # 中间那列砖红填充
                if i == 2:
                    draw.rectangle([(x, ay), (x + col_w, ay + ah)], fill=COL_RED)
                    txt_color = COL_PAPER
                else:
                    draw.rectangle([(x, ay), (x + col_w, ay + ah)], outline=COL_INK, width=2)
                    txt_color = COL_INK
                # 拆分 label / value
                tokens = p_text.strip().split(" ")
                # label 是第一个 token
                label = tokens[0]
                value = " ".join(tokens[1:]) if len(tokens) > 1 else ""
                lf = fnt(18, bold=False)
                draw.text((x + 16, ay + 14), label, fill=txt_color, font=lf)
                vf = fnt(22, bold=True)
                draw.text((x + 16, ay + 38), value, fill=txt_color, font=vf)
            main_y = ay + ah + 16'''

s = s.replace(old_anchor, new_anchor, 1)
print('Anchor replaced')

p.write_text(s, encoding='utf-8')
print('Done. Size:', len(s))