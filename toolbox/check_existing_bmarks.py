"""Check existing B166ER marks in PPT files"""
from pptx import Presentation
import sys

path = r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx'

prs = Presentation(path)
print(f'Total slides: {len(prs.slides)}')
print(f'Slide size: {prs.slide_width} x {prs.slide_height} EMU')
print()

# Check existing text on each slide for "B166ER" or related marks
for slide_idx, slide in enumerate(prs.slides):
    found_b = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if 'B166ER' in txt or 'b166er' in txt.lower() or 'B16' in txt:
                found_b.append((shape.name, txt[:80]))
    if found_b:
        print(f'Slide {slide_idx+1}:')
        for name, txt in found_b:
            print(f'  [{name}] {txt!r}')
    else:
        print(f'Slide {slide_idx+1}: NO B166ER mark found')