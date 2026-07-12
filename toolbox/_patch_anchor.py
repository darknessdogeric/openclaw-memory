import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
p = Path(r"C:/Users/ericz/Desktop/新媒体产品线/酒管公司供应链工程-交付包-v1.0/XHS-output/gen_v3_pillow.py")
s = p.read_text(encoding='utf-8')
s = s.replace('"price_anchor": "咨询 1 天 \u00a55000+   招总监 \u00a530万/年   本包 \u00a52980",',
              '"price_anchor": "咨询 1 天 ¥5000+|招总监 ¥30万/年|本包 ¥2980",')
p.write_text(s, encoding='utf-8')
print('OK', len(s))