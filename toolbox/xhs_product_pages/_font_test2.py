"""字体渲染测试 v2 - 系统字体全面测试"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1000
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# 测试字体（系统字体）
test_fonts = [
    ('SimHei',    r'C:\Windows\Fonts\simhei.ttf'),
    ('SimSun-0',  r'C:\Windows\Fonts\simsun.ttc', 0),
    ('SimSun-1',  r'C:\Windows\Fonts\simsun.ttc', 1),
    ('MS-YaHei-0', r'C:\Windows\Fonts\msyh.ttc', 0),
    ('MS-YaHei-1', r'C:\Windows\Fonts\msyh.ttc', 1),
    ('Dengb',     r'C:\Windows\Fonts\Dengb.ttf'),
    ('Deng',      r'C:\Windows\Fonts\Deng.ttf'),
]

# 测试字串
text = "独立酒店境外市场拓展指南 ¥499 8月31日"
text2 = "5大跨境拓展痛点 · 第3个最致命 → Booking Agoda Airbnb"
text3 = "「ERIC出品」小红书店铺 - \"22年酒店老兵\" 张实"

x = 20
loaded = []
for entry in test_fonts:
    name = entry[0]
    path = entry[1]
    idx = entry[2] if len(entry) > 2 else 0
    try:
        f = ImageFont.truetype(path, 22, index=idx)
        d.text((x, 20), f"{name}:", fill=(180,0,0), font=f)
        d.text((x, 60), text, fill=(0,0,0), font=f)
        d.text((x, 100), text2, fill=(0,0,0), font=f)
        d.text((x, 140), text3, fill=(0,0,0), font=f)
        x += 330
        loaded.append(name)
    except Exception as e:
        print(f"FAIL {name}: {e}")

img.save(r'D:\B166ER-OpenClaw\workspace\output\小红书商品图_独立酒店境外市场拓展指南\_font_test2.png')
print(f"OK 测试图保存 (loaded: {loaded})")