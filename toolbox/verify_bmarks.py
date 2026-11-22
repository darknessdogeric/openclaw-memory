from pptx import Presentation
from pptx.util import Emu

prs = Presentation(r'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx')

# Check various slides
for idx in [1, 2, 5, 12]:
    slide = prs.slides[idx]
    print(f'--- Slide {idx+1} ---')
    for shape in slide.shapes:
        if shape.has_text_frame and 'B166ER' in shape.text_frame.text:
            txt = shape.text_frame.text.replace(chr(10), ' | ')
            left_in = Emu(shape.left).inches if shape.left else 0
            top_in = Emu(shape.top).inches if shape.top else 0
            w_in = Emu(shape.width).inches if shape.width else 0
            h_in = Emu(shape.height).inches if shape.height else 0
            print(f'  @ ({left_in:.2f}", {top_in:.2f}") size ({w_in:.2f}" x {h_in:.2f}"): {txt!r}')