import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

p = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output/gen_v3_pillow.py")
s = p.read_text(encoding='utf-8')

# Find the draw_page_v3 function and add chapters_preview rendering + price_anchor
# Insert before "===== 底部 (8%) ====="

old_section = '''    # 6. items (痛点/内容/章节列表)
    if "items" in page:
        items = page["items"]
        for item in items:
            # 项目符号
            draw.ellipse([(side + 4, main_y + 12), (side + 14, main_y + 22)], fill=COL_RED)
            it_f = fnt(20, bold=False)
            draw.text((side + 24, main_y), item, fill=COL_INK, font=it_f)
            main_y += 32
        main_y += 8'''

new_section = old_section + '''

    # 6.5 chapters_preview (13 章缩略图, 仅 p01)
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
        main_y = grid_top + rows * (cell_h + gap_y) + 8

    # 6.6 price_anchor (价值锚点条, 仅 p01)
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

s = s.replace(old_section, new_section, 1)

p.write_text(s, encoding='utf-8')
print('After:', len(s))
print('chapters_preview render in file?', 'chapters_preview' in s and 'cell_w' in s)