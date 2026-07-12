import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

p = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output/gen_v3_pillow.py")
s = p.read_text(encoding='utf-8')
print('Before:', len(s))

# 1. Add chapters_preview to p01_cover
old = '"stats": [("13", "章节"), ("5", "档版本"), ("5", "角色路径"), ("24", "年实战")],'
chapters_str = '"01 主报告", "02 实施方案", "03 体系架构", "04 供应商分级", "05 工具矩阵", "06 KPI", "07 应急 SOP", "08 成本 TCO", "09 实施清单", "10 数据经营", "11 决策树", "12 模板", "13 架构"'
new = '"stats": [("13", "章节"), ("5", "档版本"), ("5", "角色路径"), ("24", "年实战")],\n        "chapters_preview": [' + chapters_str + '],'
s = s.replace(old, new, 1)

# 2. Add price_anchor
old2 = '"cta": "立即购买 \u00a52980",'
new2 = old2 + '\n        "price_anchor": "咨询 1 天 \u00a55000+   招总监 \u00a530万/年   本包 \u00a52980",'
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
print('After:', len(s))
print('chapters_preview in file?', 'chapters_preview' in s)
print('price_anchor in file?', 'price_anchor' in s)