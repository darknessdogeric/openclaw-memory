"""Check slide layouts to find best B标 placement"""
from pptx import Presentation
from pptx.util import Emu

path = r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx'
prs = Presentation(path)

print(f'Slide size: {prs.slide_width} x {prs.slide_height} EMU')
print(f'         = {Emu(prs.slide_width).inches:.2f}" x {Emu(prs.slide_height).inches:.2f}"')
print()

for slide_idx, slide in enumerate(prs.slides):
    # Check top-right corner (x > 10000000, y < 1500000)
    top_right_shapes = []
    # Check bottom-right corner (x > 10000000, y > 5500000)
    bottom_right_shapes = []
    for shape in slide.shapes:
        if shape.left is None or shape.top is None:
            continue
        if shape.left > 10000000 and shape.top < 1500000:
            top_right_shapes.append((shape.name, shape.left, shape.top, shape.width, shape.height))
        if shape.left > 10000000 and shape.top > 5500000:
            bottom_right_shapes.append((shape.name, shape.left, shape.top, shape.width, shape.height))
    print(f'Slide {slide_idx+1}:')
    print(f'  Top-right ({len(top_right_shapes)} shapes): {top_right_shapes[:2]}')
    print(f'  Bottom-right ({len(bottom_right_shapes)} shapes): {bottom_right_shapes[:2]}')