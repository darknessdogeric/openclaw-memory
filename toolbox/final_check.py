from pptx import Presentation
import os

files = [
    ('实战案例·成功+失败', r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 实战案例：成功+失败.pptx'),
    ('酒店行业速查表', r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx'),
    ('酒店行业专业培训手册', r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业专业培训手册.pptx'),
    ('5大国际酒店集团品牌矩阵', r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 深度专题三：5 大国际酒店集团品牌矩阵.pptx'),
]
print('=' * 75)
print(f'{"文件名":32s} | {"页数":>5s} | {"B标页":>6s} | {"大小":>12s}')
print('=' * 75)
total_slides = 0
total_b = 0
for name, f in files:
    prs = Presentation(f)
    total = len(prs.slides)
    with_b = sum(1 for s in prs.slides if any('B166ER' in sh.text_frame.text for sh in s.shapes if sh.has_text_frame))
    sz = os.path.getsize(f)
    total_slides += total
    total_b += with_b
    print(f'{name:32s} | {total:>5d} | {with_b:>6d} | {sz:>12,}')
print('=' * 75)
print(f'{"合计":32s} | {total_slides:>5d} | {total_b:>6d}')
print('=' * 75)