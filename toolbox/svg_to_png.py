"""SVG 转 PNG (高分辨率)"""
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.graphics import renderPM

# 切换 reportlab 渲染后端为 pypdf (避免 cairocffi 依赖)
from reportlab import rl_config
rl_config.renderPMBackend = 'rlPyCairo'

SVG_PATH = r"C:\Users\ericz\Desktop\酒店品牌市场指数_2026H2_思维导图.svg"
PNG_PATH = r"C:\Users\ericz\Desktop\酒店品牌市场指数_2026H2_思维导图.png"

# 加载 SVG
drawing = svg2rlg(SVG_PATH)

# 输出 PNG (使用 renderPM 但指定不用 cairocffi)
try:
    renderPM.drawToFile(drawing, PNG_PATH, fmt='PNG')
    print(f'OK: {PNG_PATH}')
except Exception as e:
    print(f'renderPM 失败: {e}')
    print('尝试替代方案...')