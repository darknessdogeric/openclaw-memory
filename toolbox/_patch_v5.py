import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

p = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output/gen_v5_pillow.py")
s = p.read_text(encoding='utf-8')

# 1. 删除标题下方"¥99"小字 (title_em 改为不带价格的副标)
s = s.replace('"title_em": "全套资料 ¥99",', '"title_em": "全套 SOP 即拿即用",')

# 2. 5 分钟发资料 移到 CTA 下方独立行 (cta_sub 已经存在, 调整位置)
# 这个其实已经是独立的, 不改

# 3. 顶部 B 标增加 4-6px 间距 - 通过 draw_brand_b 内部 padding 调整
# 找到 "ERIC × B166ER" 那行
old_brand = '''    # 副文字 (右侧)
    if with_text:
        text_x = x + size + 12
        # ERIC × B166ER
        ef = fnt(int(size * 0.28), bold=True)
        draw.text((text_x, y + size // 4), "ERIC × B166ER", fill=COL_INK, font=ef)
        # 共研出品
        cf = fnt(int(size * 0.22), bold=False)
        draw.text((text_x, y + size // 2 + 4), "共研出品", fill=COL_GRAY, font=cf)'''

new_brand = '''    # 副文字 (右侧)
    if with_text:
        text_x = x + size + 16
        # ERIC × B166ER
        ef = fnt(int(size * 0.28), bold=True)
        draw.text((text_x, y + size // 5), "ERIC × B166ER", fill=COL_INK, font=ef)
        # 共研出品
        cf = fnt(int(size * 0.22), bold=False)
        draw.text((text_x, y + size // 2 + 6), "共研出品", fill=COL_GRAY, font=cf)'''

s = s.replace(old_brand, new_brand, 1)

# 4. 按钮文案改为 "¥99 立即领取完整资料"
s = s.replace('"cta": "¥99 立即领取",', '"cta": "¥99 立即领取完整资料",')

p.write_text(s, encoding='utf-8')
print('OK', len(s))