"""SimSun 各 index 测试"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1800, 600
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

text = "独立酒店境外市场拓展指南 ¥499 8月31日 · 第3个最致命"

x = 20
for idx in range(6):
    try:
        f = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', 32, index=idx)
        d.text((x, 20), f"SimSun idx={idx}:", fill=(180,0,0), font=f)
        d.text((x, 80), text, fill=(0,0,0), font=f)
        x += 290
    except Exception as e:
        d.text((x, 20), f"SimSun idx={idx}: FAIL", fill=(255,0,0), font=ImageFont.load_default())
        x += 290

# MS-YaHei 各 index
x = 20
y = 250
for idx in range(6):
    try:
        f = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 32, index=idx)
        d.text((x, y), f"MS-YaHei idx={idx}:", fill=(180,0,0), font=f)
        d.text((x, y+60), text, fill=(0,0,0), font=f)
        x += 290
    except Exception as e:
        d.text((x, y), f"MS-YaHei idx={idx}: FAIL", fill=(255,0,0), font=ImageFont.load_default())
        x += 290

img.save(r'D:\B166ER-OpenClaw\workspace\output\小红书商品图_独立酒店境外市场拓展指南\_font_test3.png')
print("OK")