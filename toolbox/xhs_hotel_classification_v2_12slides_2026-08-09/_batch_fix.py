"""批量修正 HTML: 1. X -> B (logo)  2. tag-line 去重 (XX/12 ·)"""
import os, re

DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_classification_v2_12slides_2026-08-09"

for f in sorted(os.listdir(DIR)):
    if f.endswith('.html'):
        p = os.path.join(DIR, f)
        with open(p, 'r', encoding='utf-8') as fh:
            c = fh.read()
        # 1. B 标: X -> B (logo 内容)
        new_c = c.replace('b-logo">X</div>', 'b-logo">B</div>')
        # 2. 底部 tag-line 去重 (去掉 'NN / 12 · ' 前缀)
        new_c = re.sub(r'\d\d / 12 · ', '', new_c)
        if new_c != c:
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(new_c)
            print(f"Updated: {f}")
        else:
            print(f"No change: {f}")

print("Done.")